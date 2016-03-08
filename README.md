# DigitalOcean Starbound Server Snapshot/Destroy and Restore.

**The Problem:**
I only need the Starbound server to run *maybe* 8 hours a month. Paying $40 a month for 
this usage level is a waste of resources. I have considered merging this into my Docker host but for now
I will keep them separate. Because of this I require a method to backup and destroy my Droplets, then 
restore them when they are needed.

**Solution:**
In order to solve this, I'm leveraging DigitalOceans snapshots and destroying the server when the snapshot
is complete. This will reduce my usage charges to what I actually use, and provide a versioned history 
of the server should something go wrong.


### Usage:

It should be noted that this script only targets Droplets named `starbound-server`.

* **Environment Variables:**
  You may supply a DigitalOcean API Key at runtime or set it to an environment variable accessible to the script.
  Something like `export DO_API_KEY=mykey` in `~/.bashrc` should allow the script to autoload the key for usage.

* **Command line:**
  There are currently 3 Command line options. `--backup`, `--destroy`, and `--restore`.
  * `--backup`: Run the snapshot against the `starbound-server` Droplet.
  * `--destroy`: This should be used along with `--backup`. If provided, 
    the droplet will be destroyed after it is backed up (This provides the cost savings).
  * `--restore`: Run this one on its own, It will use the latest starbound-server snapshot to 
      create a new `starbound-server` droplet.


### Dependencies:
  * [Koalalorenzo's python-digitalocean](https://github.com/koalalorenzo/python-digitalocean)