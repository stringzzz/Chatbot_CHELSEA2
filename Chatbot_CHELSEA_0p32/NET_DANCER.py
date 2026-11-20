import subprocess
import json
import xml.etree.ElementTree as ET
import asyncio
from datetime import datetime
import math
import re
import random
import time
import os
import signal
import socket

class Net_Dancer:

	def __init__(self, file_path=''):

		self.synonym_lists = {
			'hosts': ['hosts', 'devices', 'buildings'],
			'host': ['host', 'device', 'building'],
			'active': ['up', 'active', 'alive', 'running'],
			'open': ['open', 'listening', 'active'],
			'scanned': ['you see', 'saw', 'witness', 'witnessed', 'view', 'viewed', 'scan', 'scanned'],
			'most': ['most', 'largest', 'highest', 'greatest'],
			'least': ['least', 'smallest', 'lowest', 'littlest']
		}

		self.reverse_pronoun_map = {
			r"\byou\b": "i",
			r"\byou're\b": "i'm",
			r"\byou\b": "me",
			r"\byour\b": "my",
			r"\byours\b": "mine"
		}

		self.active_scan_task = None

		self.file_path = file_path

	def get_synonym_list(self, list_type):

		return "|".join(self.synonym_lists[list_type])
	
	def get_random_synonym(self, list_type):

		return random.choice(self.synonym_lists[list_type])

	def reverse_pronouns(self, input_message):

		#Replace each pronoun with its inverted form
		for pattern, replacement in self.reverse_pronoun_map.items():
		
			input_message = re.sub(pattern, replacement, input_message, flags=re.IGNORECASE)

		return input_message

	async def run_network_scan(self, target_subnet="192.168.1.0/24"):
		
		# Using -T3 for normal speed scanning and -sV for service versions
		# Outputting to XML (-oX) makes parsing incredibly reliable
		
		cmd = ["nmap", "-T4", "-sV", "-oX", "-", target_subnet]
		
		proc = await asyncio.create_subprocess_exec(
			*cmd,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE
		)
		stdout, _ = await proc.communicate()
		
		return stdout.decode('utf-8')

	def parse_nmap_xml(self, xml_data):
		
		root = ET.fromstring(xml_data)
		network_map = {}
		
		for host in root.findall('host'):
		
			status = host.find('status').get('state')
			if status != 'up':
				continue
				
			ip = host.find('address').get('addr')
			network_map[ip] = {"ports": []}
			
			# Try to grab hostnames if available
			hostnames = host.find('hostnames')
		
			if hostnames is not None:
		
				name_node = hostnames.find('hostname')
		
				if name_node is not None:
					network_map[ip]["name"] = name_node.get('name')

			
				else:

					network_map[ip]["name"] = ""

			else:

				network_map[ip]["name"] = ""	

			# Gather open ports and services
			ports = host.find('ports')
		
			if ports is not None:
		
				for port in ports.findall('port'):
		
					port_id = port.get('portid')
					state = port.find('state').get('state')
		
					if state == 'open':
		
						service = port.find('service')
						service_name = service.get('name') if service is not None else "unknown"
						product = service.get('product') if service is not None else ""
						
						network_map[ip]["ports"].append({
							"port": port_id,
							"service": service_name,
							"product": product
						})

			#Leave empty, can tell CHELSEA what to call each device by referencing it's IP address (192.168.1._ is your home)
			network_map[ip]['mac_address'] = ''
			network_map[ip]['nickname'] = ''
		
		return network_map

	async def observe_network(self):

		start_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
	
		raw_xml = await self.run_network_scan()
		current_map = self.parse_nmap_xml(raw_xml)

		#Check if net_map file already exists, if not use empty list
		net_map_log = []
		try:
			with open(f"{self.file_path}net_map.json", 'r') as net_map_file:
				net_map_log = json.load(net_map_file)

		except(FileNotFoundError):
			pass

		#Get the time elapsed for this scan
		end_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

		start_time_object = datetime.strptime(start_time, "%m/%d/%Y, %H:%M:%S")
		end_time_object = datetime.strptime(end_time, "%m/%d/%Y, %H:%M:%S")

		scan_time = math.ceil((end_time_object - start_time_object).total_seconds() / 60)

		#Append the current net_map to the general net_map log
		net_map_log.append({
			'date': datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
			'scan_time': scan_time,
			'net_map': current_map
		})

		#Output the net_map log
		with open(f"{self.file_path}net_map.json", "w") as net_map_file:
			json.dump(net_map_log, net_map_file, indent=4)

	def load_net_map_log(self):

		try:

			with open(f"{self.file_path}net_map.json", "r") as net_map_file:
				net_map_log = json.load(net_map_file)

			return net_map_log

		except FileNotFoundError:

			return None #"Local network environment map is currently empty or compiling."
		
	def save_net_map_log(self, net_map_log):

		original_net_map_log = self.load_net_map_log()
		original_net_map_log[-1]['net_map'] = net_map_log

		with open(f"{self.file_path}net_map.json", "w") as net_map_file:
			json.dump(original_net_map_log, net_map_file, indent = 4)

	async def listen_to_environment(self, source1='', source2='', duration_minutes=1):

		source2 = '' if source2 == "''" else source2

		# Configuration
		CAPTURE_DURATION_SECS = int(int(duration_minutes) * 60)
		OUTPUT_FILE = f"{self.file_path}network_chatter.json"
		
		BPF_FILTER = ''
		if source1 != '' and source2 != '':
			BPF_FILTER = f"host {source1} and host {source2}"
		elif source1 != '':
			BPF_FILTER = f"host {source1}"

		# -a duration:X stops tshark automatically after X seconds
		# -T ek outputs a stream of newline-delimited JSON (NDJSON) fields
		# -e selections specify exactly what packet data we care about to keep it light
		cmd = [
			"tshark",
			"-l",
			"-a", f"duration:{CAPTURE_DURATION_SECS}",
			"-f", BPF_FILTER,
			"-T", "fields",
			"-e", "frame.time_relative",
			"-e", "eth.src",
			"-e", "eth.dst",
			"-e", "ip.src",
			"-e", "ip.dst",
			"-e", "frame.protocols",
			"-E", "separator=/t"  # Separate extracted fields with tabs
		]
		
		try:

			# Run tshark as an async subprocess
			process = await asyncio.create_subprocess_exec(
				*cmd,
				stdout=asyncio.subprocess.PIPE,
				stderr=asyncio.subprocess.DEVNULL,  # Silence tshark's counter overlay
				preexec_fn=os.setsid
			)

			allowed_execution_time = int(CAPTURE_DURATION_SECS) + 2
			start_time = time.monotonic()
			deadline = start_time + allowed_execution_time
			
			captured_data = []
			
			# Read the stream line by line as tshark captures packets
			try:

				while True:

					current_time = time.monotonic()
					if current_time >= deadline:
						break

					remaining_budget = deadline - current_time

					try:
						line = await asyncio.wait_for(process.stdout.readline(), timeout=remaining_budget)
			
					except asyncio.TimeoutError:
						break

					if not line:
						break
											
					decoded_line = line.decode('utf-8').strip()
					
					if not decoded_line:
						continue
						
					# Parse the tab-separated fields
					parts = decoded_line.split('\t')

					if len(parts) >= 6:
					
						packet_entry = {
							"timestamp_rel": parts[0],
							"mac_source": parts[1],
							"mac_destination": parts[2],
							"ip_source": parts[3] if parts[3] else "N/A",
							"ip_destination": parts[4] if parts[4] else "N/A",
							"protocols": parts[5]
						}
					
						captured_data.append(packet_entry)

			finally:

				#Terminate all tshark processes

				if process.returncode is None:

					try:
						
						os.killpg(os.getpgid(process.pid), signal.SIGKILL)

						await asyncio.wait_for(process.wait(), timeout = 1.0)

					except Exception:
						pass
					
			#Close the stdout stream reader explicitly to prevent resource leaks
			try:

				process.stdout.feed_data(b'')

			except Exception:
				pass
			
			# Compile metadata snapshot
			snapshot = {
				"snapshot_metadata": {
					"timestamp": datetime.now().isoformat(),
					"duration_seconds": CAPTURE_DURATION_SECS,
					"total_packets_captured": len(captured_data)
				},
				"packets": captured_data
			}
			
			#Append new data to JSON file
			tshark_file_contents = []
			try:

				with open(OUTPUT_FILE, 'r') as tshark_file:
					tshark_file_contents = json.load(tshark_file)

			except(FileNotFoundError):

				pass
			
			tshark_file_contents.append(snapshot)

			with open(OUTPUT_FILE, "w") as tshark_file:
				json.dump(tshark_file_contents, tshark_file, indent=4)
			
		except Exception as e:
			print(f"Error executing tshark: {e}")

	def analyze_network_snapshot(self):

		filepath = f"{self.file_path}network_chatter.json"

		discovered_mac = 0

		try:

			with open(filepath, "r") as tshark_file:
				data = json.load(tshark_file)[-1]
				
			packets = data["packets"]

			#Try to find all unknown MAC addresses for all known devices

			net_map_log = self.load_net_map_log()[-1]['net_map']

			for device in net_map_log:
				
				if net_map_log[device]['mac_address'] != '':
					continue

				for packet in packets:

					if packet["ip_source"] == device and packet["mac_source"] != "N/A":

						net_map_log[device]['mac_address'] = packet["mac_source"]
						discovered_mac += 1
						break

					elif packet["ip_destination"] == device and packet["mac_destination"] != "N/A":

						net_map_log[device]['mac_address'] = packet["mac_destination"]
						discovered_mac += 1
						break

			self.save_net_map_log(net_map_log)

				
		except FileNotFoundError:

			print(f"Error: '{filepath}' not found.")
		
		finally:

			with open(f"{self.file_path}temp_tshark_mac_count.txt", 'w') as temp_tshark_file:
				temp_tshark_file.write(str(discovered_mac))

	def CHELSEA_server_initialize(self, port):

		#Create a socket object 
		s = socket.socket()         
		print ("netdancer-server socket successfully created")            
		
		#Next bind to the port 
		s.bind(('', int(port)))         
		print (f"netdancer-server socket binded to {port}") 
		
		#Put the socket into listening mode 
		s.listen(5)     
		print("netdancer-server socket is listening")

		self.c = None
		addr = None
		while True: 
 
			#Establish connection with client. 
			self.c, addr = s.accept()

			if self.c and addr:    
			
				print(f"got connection from client-CHELSEA at {addr}")

				#Send a message to the client-CHELSEA to check if connection valid (Will be orocessed on that side), encoding it to send byte type. 
				self.c.send('thank you for connecting'.encode())

				break

	def CHELSEA_server_accept_message(self):

		recieved_part = False
		client_message = ""
		while not recieved_part:
		
			#Recieve client-CHELSEA message
			client_message = self.c.recv(1024).decode()

			if re.match(r'^messageflag', client_message):

				client_message = client_message.replace('messageflag', '')
				recieved_part = True				
		
		if client_message == "exit the chat":

			#Exit message detected, close down connection

			#Close the connection with the client 
			self.c.close()
			print("server-chelsea closed the connection with client-chelsea")

			return "exit the chat"

		else:

			#Else receive client-CHELSEA message like normal
			return client_message

	def CHELSEA_server_send_message(self, message):

		#Send message to client-CHELSEA
		message = f"messageflag{message}"
		self.c.send(message.encode())

	def CHELSEA_client_initialize(self, port, ip, message_limit):

		#######################################################################################
		# Need error handling if connection cannot be established, otherwise can create mess  #
		#######################################################################################

		#Create a socket object 
		self.s = socket.socket()         

		#Bind socket to port
		self.s.bind(('', int(port)))                  
		
		#Connect to the server on local computer 
		self.s.connect((ip, int(port)))

		#Receive initial message from server-CHELSEA
		server_message = self.s.recv(1024).decode()
		if server_message == "thank you for connecting":

			#Connection with server-CHELSEA officially established
			print("netdancer-client connected to netdancer-server")

			#Count needed to know when to end connection
			self.message_count = 0
			self.message_limit = message_limit

		else:

			print("error connecting to netdancer-server") #Need better error describing exactly what went wrong

	def CHELSEA_client_accept_message(self):

		server_message = ""
		recieved_flag = False
		while not recieved_flag:

			#Get the message from server-CHELSEA
			server_message = self.s.recv(1024).decode()

			if re.match(r'^messageflag', server_message):

				server_message = server_message.replace('messageflag', '')
				recieved_flag = True

		#Normal message, increase message count and see if at limit
		self.message_count += 1

		if self.message_count == self.message_limit:

			#Message limit reached, initiate connection shutdown process

			client_message = "messageflagexit the chat"
			self.s.send(client_message.encode()) 

			self.s.close()

			return "exit the chat"

		return server_message

	def CHELSEA_client_send_message(self, message):

		message = f"messageflag{message}"

		#Send message to server-CHELSEA
		self.s.send(message.encode())
