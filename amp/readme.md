#MPD client

A simple NodeJS app listening for MPD events to mute or unmute an amplifier depending on playing state
Hard muting a class D amplifier is literally shutting it down (power stage is off) 
so it helps to save some (a lot) electricity when no music is playing 
and lets a user to keep it 'on' constantly.

The app is listening for MPD 'system-player', 'system', 'mixer' events and queries its status.
When state is 'play' it executes an external unmute command
When stat is either 'stop' or 'pause' it executes an external mute command after a delay 
(delay must be at least 2 seconds because when MPD changes tracks it changes its state from 'play' to 'stop' and back)

###RuneAudio (Arch) setup
*tested on BeagleBone Black RuneAudio*
To autostart MPD client on Arch boot 
1. Copy provided amp.service file to /usr/lib/systemd/system/ folder and create
```cp amp.service /usr/lib/systemd/system/```
2. Create a symlink to systemd folder
```ln /usr/lib/systemd/system/amp.service /etc/systemd/system/multi-user.target.wants/amp.service```
3. Make amp.sh executable
```chmod +x amp.sh```
4. When using upmpdcli double check /usr/lib/systemd/system folder for its presence and create a symlink if it is missing
```ln /usr/lib/systemd/system/upmpdcli.service /etc/systemd/system/multi-user.target.wants/upmpdcli.service```
5. Make python scripts executable
```chmod +x ../*.py```
6. Install dependencies
```npm install```
7. Reboot
