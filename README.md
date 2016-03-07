# [WIP] DigitalOcean Starbound Server Snapshot/Destroy and Restore.

**The Problem:**
I only need the Starbound server to run *maybe* 8 hours a month. Paying $40 a month for 
this usage level is a waste of resources. I have considered merging this into my Docker host but for now
I will keep them separate. Because of this I require a method to backup and destroy my Droplets, then 
restore them when they are needed.

**Solution:**
In order to solve this, I'm leveraging DigitalOceans snapshots and destroying the server when the snapshot
is complete. This will reduce my usage charges to what I actually use, and provide a versioned history 
of the server should something go wrong.