sudo apt update;
sudo apt install nmap -y;
sudo apt install wireshark tshark -y;
sudo dpkg-reconfigure wireshark-common;
sudo usermod -aG wireshark $USER;
newgrp wireshark;
sudo setcap cap_net_raw,cap_net_admin=eip /usr/bin/dumpcap;

#Running this afterward should show you the list of interfaces if setup was done correctly
#If it gives you a permission error or says "No interfaces found", a full system reboot will firmly force the group updates to take effect.

#tshark -D