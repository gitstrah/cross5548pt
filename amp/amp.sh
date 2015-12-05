#!/bin/sh -e
##########################################################
## don't forget to call this script from /etc/rc.local  ##
##########################################################
# set volume down just in case
mpc volume 15
# initialize the hardware
python /root/cr/ctest.py 2>&1 > /root/cr/logs/logfile.log
# start MPD watcher
nice node /root/cr/amp/amp.js 2>&1 > /root/cr/logs/logfile.log &
