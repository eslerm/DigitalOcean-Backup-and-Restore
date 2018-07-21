#!/usr/env/python
import os
import sys
import digitalocean
from datetime import datetime

####################
# Helper Functions #
####################


def get_do_id():
    return input("Droplets ID: ")

def get_api_key():
    return input("DigitalOcean API Key: ")


def help_menu():
    print("""
    At this time, no additional parameters for the following are 
    taken.
    
    ======
    Backup
    ======

    --backup
        This will create a snapshot of all droplets of the given ID.

    --destroy
        This will destroy the Droplet after the snapshot is taken.
        This is the primary cost-savings measure.

    =======
    Restore
    =======

    --restore
        This will create a new Droplet with the given ID from the 
        snapshot taken previously. By default it will be located in NYC1,
        use all SSH Keys associated with your account, and be a 2GB instance.
    """)
    exit()


def backup_droplet(droplets, target_name, destroy=False):
    # Iterate over droplets, snapshotting all "target_name" droplets.
    for droplet in droplets:
        time_now = datetime.now().strftime("%Y-%m-%d--%H:%M:%S")

        if droplet.name == target_name:

            if droplet.status != 'off':
                print("Droplet {} Online, powering off.".format(droplet.name))
                droplet.power_off(return_dict=False).wait()

            print("Attempting to Snapshot Droplet {} with an ID of {}".format(droplet.name, droplet.id))
            droplet.take_snapshot('{}_{}'.format(time_now, droplet.name), return_dict=False, power_off=False).wait()

            if destroy:
                droplet.destroy()


# variable assignment for restore_droplet()
do_id = None

def restore_droplet(
        
        snapshot, keys, api_key, region='sfo2', 
        size_slug='s-1vcpu-1gb', name=do_id, 
        backups=False):

    print("Pushing snapshot {} to a fresh droplet".format(snapshot))

    droplet = digitalocean.Droplet(token=api_key,
                                   name=do_id,
                                   ssh_keys=keys,
                                   region=region,
                                   image=snapshot,
                                   size_slug=size_slug,
                                   backups=backups)
    print(droplet.name)
    print("foo do_id:"+do_id+" "+str(type(do_id)))
    # Create the Droplet and wait for it to complete
    droplet.create()
    action = digitalocean.Action(id=droplet.action_ids[0], token=droplet.token, droplet_id=droplet.id)
    action.load()
    action.wait()

    created = droplet.load()

    print("Droplet Created at {}".format(droplet.ip_address))


########
# Main #
########

if __name__ == '__main__':

    backup = False
    destroy = False
    restore = False

    # Get CLI Options
    for opt in sys.argv[1:]:
        if opt in ("-b", "--backup"):
            backup = True
        elif opt in ("-d", "--destroy"):
            destroy = True
        elif opt in ("-r", "--restore"):
            restore = True
        elif opt in ("-h", "--help"):
            help_menu()
    # Show if no Arguments supplied
    if not backup and not restore:
        print("No Options selected, please run with --help to view all")
        exit()

    # Show if attempting to run Backup and Restore options simultaneously
    if backup and restore or destroy and restore:
        print("These Arguments cannot be used together, please reference --help")
        exit()

    # Set Droplet ID
    do_id = os.getenv('DO_ID')
    while not do_id:
        do_id = get_do_id()
    print("do_id: "+do_id)

    # Set API Key
    api_key = os.getenv('DO_API_KEY')
    while not api_key:
        api_key = get_api_key()

    # Get DigitalOcean Info
    manager = digitalocean.Manager(token=api_key)
    ssh_keys = manager.get_all_sshkeys()
    droplets = manager.get_all_droplets()
    snapshots = manager.get_my_images()
    newest_snapshot = ''

    # Get Newest Snapshot
    for snapshot in snapshots:
        if do_id in snapshot.name:
            if newest_snapshot == '' or newest_snapshot.created_at < snapshot.created_at:
                newest_snapshot = snapshot


    if backup:
        backup_droplet(droplets, do_id, destroy)

    if restore and newest_snapshot != '':
        restore_droplet(newest_snapshot.id, ssh_keys, api_key)
