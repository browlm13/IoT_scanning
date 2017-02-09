#python 3

"""
		inet scanning heads up display,
		csv data extractor to json

		(should be server side eventually)
		get request to endpoint for csv file


		current HUD data:

			last_scan_time:
			num_scanned_ips:
			num_hosts_found:
			open_telnet:
			open_ssh:
			os_found:
			vendor_found:
			num_complete: #os, open tel, open ssh
"""

import requests
import sys
import json
import datetime

#settings
database_url = 'http://lyle.smu.edu/~lmbrown/iot_data/index.php?endpoint=inet_scan_csv'
json_fname = "data/scan_HUD_data.json"


#GET reuest to remote database, return csv string
def get_inet_csv_string():
	r = requests.get(database_url)
	if (r.status_code == 200): return r.text
	else: return -1

#convert unix timestampt to date time
def timestamp_to_datetime(timestamp):
    return datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')


#extracts scan HUD data from csv string and returns dictionary
def extract_HUD_data(csv_string):

	#HUD data
	HUD_data = {
		'last_scan_time' : -1,
		'num_scanned_ips' : 0,
		'num_hosts_found' : 0,
		'open_telnet' : 0,
		'open_ssh' : 0,
		'os_found' : 0,
		'mac_found' : 0,
		'vendor_found' : 0,
		'num_complete' : 0
	}

	for line in csv_string.splitlines():
		#extract scan information
		if (line[:4] == "scan"):
			scan_data = line.split(',')
			HUD_data['num_scanned_ips'] += int(scan_data[1])
			HUD_data['num_hosts_found'] += int(scan_data[2])
			HUD_data['last_scan_time'] = scan_data[3]

		#extract host information
		if (line[:4] == "host"):
			host_data = line.split(',')

			telnet = int(host_data[5])
			ssh = int(host_data[6])

			HUD_data['open_telnet'] += telnet
			HUD_data['open_telnet'] += ssh

			if host_data[3] != "NULL": HUD_data['mac_found'] += 1
			if host_data[4] != "NULL": HUD_data['vendor_found'] += 1
			if host_data[7] != "NULL": HUD_data['os_found'] += 1
			if (telnet or ssh) and (host_data[7] != "NULL"):	HUD_data['num_complete'] += 1

	#convert unix time stamp to datetime
	HUD_data['last_scan_time'] = timestamp_to_datetime(HUD_data['last_scan_time'])

	return HUD_data


"""
	run program
"""
# pull csv data into string
csv_string = get_inet_csv_string()

# [todo]: add exception handling
if csv_string != -1: 

	# collect HUD info
	scan_HUD_data = extract_HUD_data(csv_string)

	#write dictionary to json file
	with open(json_fname, 'w') as f:
		json.dump(scan_HUD_data, f)

else:
	print ("scan_HUD_data.py: Error GET request")








