#python 3

#external libraries
import os
import requests
import sys

#internal libraries
import ip_generation as ip_generator
import nmapXML_to_CSV

"""

	1. run nmap scan
	2. convert output to csv with nmapXML_to_CSV.py
	3. push to remote server
	4. repete

		[todo]:	add command line flags for diffrent types of ip generation (sequential scan code in large_scan.py file)
"""

#settings
xml_fname = "data/nmap_scan.xml"
csv_fname = "data/nmap_scan.csv"
database_url = 'http://lyle.smu.edu/~lmbrown/iot_data/index.php'
post_keyname = 'nmap_scan_data_csv'

#push file to remote database endpoint
def push_file(file, post_keyname):
	# Read data in from new xml data file provided
	with open(file, 'r') as f:
	    data=f.read()

	#set payload
	payload={post_keyname: data}

	# POST with form-encoded data
	r = requests.post(database_url, data=payload)

	#TMP
	# Response, status etc
	print (r.text)
	print (r.status_code)


"""
									run program
"""
while True:
	### smart generation based on country codes
	#generate random ip, with range 0-255  (ex: 192.168.1.0-255) 
	ip_range = ip_generator.add_range(ip_generator.gen_rand_ipv4())

	#run scan   # --max-retries 10
	os.system('sudo nmap -p22,23 ' + ip_range + ' -O --osscan-limit --osscan-guess -oX ' + xml_fname)

	#convert nmap scan to csv file
	#os.system('python nmapXML_to_CSV.py ' + xml_fname + ' ' + csv_fname)
	if nmapXML_to_CSV.xmlf_to_csvf(xml_fname,csv_fname) == 0:
		#push to remote datafile server
		#os.system('python push_nmap_csv_to_server.py ' + csv_fname)
		push_file(csv_fname, post_keyname)


