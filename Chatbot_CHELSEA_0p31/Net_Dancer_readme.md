Net_Dancer is a completely optional feature that allows CHELSEA to explore her current network environment a bit, letting you ask questions about what she finds.
If you choose not to use this feature, you can just ignore the following instructions, CHELSEA will still work without these.
Otherwise:

To install the dependencies for Net_Dancer, run this: 
bash net_dancer_installations.sh

To use this feature, add the argument 'netdancer' to the command line call to 'python3 chatbotCHELSEA.py'.

The initial scan runs this nmap command: 
nmap -T4 -sV -oX - target_subnet

asking to listen to a specific host for N minutes runs this tshark command: 
tshark -a fduration:{CAPTURE_DURATION_SECS} -f BPF_FILTER -T fields -e frame.time_relative -e eth.src -e eth.dst -e ip.src -e ip.dst -e frame.protocols -E separator=/t

Here are some sample messages/questions you can say once the initial scan is complete:

192.168.0.123 is your home

how many hosts scanned were active?

which devices had the most number of open ports?

which devices had the least number of open ports?

what is all the info of all hosts with the open port 80?

what are the ips of all active hosts?

what are the names of all active devices?

what are the nicknames of all up buildings?

what is the name of the active host with the ip 192.168.0.123?

what is the nickname of the active host with the ip 192.168.0.123?

what is the ip address of the device with the nickname your home?

what is the nickname of the active host with ip 192.168.0.123?

what is the ip and name of the host with nickname your home?

what is the name and nickname of the host with ip 192.168.0.123?

what is the nickname and ip of the device with name bobs-computer?

can you listen to the ip 192.168.0.123 for 5 minutes?

what is the mac of the host with the nickname your home?

what is the ip address of the host with mac aa:bb:cc:dd:ee:ff?
