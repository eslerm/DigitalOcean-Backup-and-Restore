#!/usr/bin/python
import os
import sys
import digitalocean
from datetime import datetime

####################
# Helper Functions #
####################

def get_api_key():

    return raw_input("DigitalOcean API Key: ")

def help_menu():
    print "Help Menu"
    exit()


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
        print "No Options selected, please run with --help to view all"
        exit()

    # Show if attempting to run Backup and Restore options simultaneously
    if backup and restore or destroy and restore:
        print "Nope"
        exit()
    exit()
    
    # Set API Key
    api_key = os.getenv('DO_API_KEY')
    while not api_key:
        api_key = get_api_key()

    # Pull all Droplets into a list
    manager = digitalocean.Manager(token=api_key)
    droplets = manager.get_all_droplets()

    # Iterate over droplets, snapshotting all "starbound-server" droplets.
    for droplet in droplets:

        time_now = datetime.now().strftime("%Y-%m-%d--%H:%M:%S")

        if droplet.name == 'starbound-server':

            if droplet.status != 'off':
                print "Droplet {} Online, powering off.".format(droplet.name)
                droplet.power_off(return_dict=False).wait()

            print "Attempting to Snapshot Droplet {} with an ID of {}".format(droplet.name, droplet.id)
            droplet.take_snapshot('{}_{}'.format(time_now, droplet.name), return_dict=False, power_off=False).wait()