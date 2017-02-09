#python 3

"""
	nmap XML output -> C,S,V file format

		#### SQL formatting ###
		####-scan primary key = starttime
		####-host primary key = compostite primary key, scan starttime and a seqence number

		type(scan),#_hosts_scanned,#_hosts_up,starttime,elsapsedtime					#scan info
		

		type(host),ipv4,ipv6,mac,vendor,telnet,ssh,os  								#host info
		type(host),ipv4,ipv6,mac,vendor,telnet,ssh,os
		.
		.
		.
		type(host),ipv4,ipv6,mac,vendor,telnet,ssh,os

	takes nmap XML output file as first command line argument
	takes desired csv output file as second argument
"""
import sys
#import xml.etree.ElementTree as ET
import csv
from libnmap.parser import NmapParser
from xml.parsers import expat

#settings
NOT_FOUND_STRING = "NULL"

#functions
def format(raw):
	raw = raw.replace(',', '')
	raw = raw.replace('\n', '')
	raw = raw.replace('|', '')
	raw = raw.replace('_', '')
	raw = raw.replace('\t', '')
	raw = raw.replace('\r', '')
	if len(raw) == 0:
		raw = NOT_FOUND_STRING
	return raw

# variables
#xml_fname = sys.argv[1]
#csv_fname = sys.argv[2]

def xmlf_to_csvf(xml_fname, csv_fname):

	try:
		#	parse data
		report = NmapParser.parse_fromfile(xml_fname) #NmapParse module is opening the XML file

		csv_string = ""

		### scan information
		nmapscan_hosts_scanned = str(report.hosts_total)
		nmapscan_hosts_up = str(report.hosts_up)
		nmapscan_started = str(report.started)
		nmapscan_elapsed = str(report.elapsed)

		csv_string += "scan," + nmapscan_hosts_scanned + ',' + nmapscan_hosts_up + ',' + nmapscan_started + ',' + nmapscan_elapsed + "\n"

		### host information
		for _host in report.hosts:
			#hostnames = _host.hostnames		#array
			#hostnames = [format(str(x)) for x in hostnames]
			ipv4 = format(_host.ipv4)
			ipv6 = format(_host.ipv6)
			mac = format(_host.mac)
			vendor = _host.vendor
			vendor = format(str(vendor))
			os = _host.os.osmatches			#array
			if len(os) == 0:
				os = NOT_FOUND_STRING
			else:
				os = [format(str(x)) for x in os]

			#telnet and ssh (22, 23)
			ports = _host.get_ports()
			telnet = 0
			ssh = 0
			if 22 in ports: telnet = 1
			if 23 in ports: ssh = 1

			#distance_hops = str(_host.distance)
			#starttime = str(_host.starttime)
			#endtime = str(_host.endtime)
			#print ("\n\nhostnames: %s\nipv4:%s, ipv6:%s\nmac:%s, vendor:%s\nos:%s\nports:%s\nhops:%s\nstartt:%s, endt:%s" % (hostnames, ipv4, ipv6, mac, vendor, os, ports, distance_hops, starttime, endtime))

			csv_line = "host," + ipv4 + ',' + ipv6 + ',' + mac + ',' + vendor + ',' + str(telnet) + ',' + str(ssh) + ',' + ''.join(os) + '\n'
			csv_string += csv_line

		# write to csv file
		with open (csv_fname, 'w') as file:
			file.write(csv_string)

		return 0
	except: 
		print ("error nmap xml format")
		return -1

