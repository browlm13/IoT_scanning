#python 2.4

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

#import requests
import sys
#import json
import datetime

#settings
database_url = 'http://lyle.smu.edu/~lmbrown/iot_data/index.php?endpoint=inet_scan_csv'
json_fname = "scan_HUD_data.json"
csv_fname = "nmap_scan.csv"


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

# read csv data into string
f = open(csv_fname, 'r')
csv_string = f.read()
f.close()

# collect HUD info
scan_HUD_data = extract_HUD_data(csv_string)

#write dictionary to json file
f = open(json_fname, 'w')
f.write(str(scan_HUD_data))
f.close()







