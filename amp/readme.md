RuneAudio (Arch) extra steps

copy amp.service to /usr/lib/systemd/system/
ln /usr/lib/systemd/system/amp.service /etc/systemd/system/multi-user.target.wants/amp.service
ln /usr/lib/systemd/system/upmpdcli.service /etc/systemd/system/multi-user.target.wants/upmpdcli.service
