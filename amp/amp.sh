#!/usr/bin/bash
##########################################################
## don't forget to call this script from /etc/rc.local  ##
##########################################################
# set volume down just in case
/usr/bin/mpc volume 10
# initialize the hardware
python /opt/amp/init.py 2>&1 > /opt/amp/logfile.log
# start MPD watcher
nice node /opt/amp/amp/mpdclient.js 2>&1 > /opt/amp/logfile.log
