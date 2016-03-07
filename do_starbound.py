#!/usr/bin/python
import os
import digitalocean
from datetime import datetime

####################
# Helper Functions #
####################

def get_api_key():

    return raw_input("DigitalOcean API Key: ")


########
# Main #
########

if __name__ == '__main__':

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