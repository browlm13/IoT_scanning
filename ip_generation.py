import socket
import random
import struct
import csv
import os
import sys

"""
	IP Generation Modual

	If run by command line...
		Generate random list of ipv4 addresses
		pass number of ips in list as command line argument
"""

#files and path
COUNTRY_RANGES_FNAME = "ip_lists/ipv4_country_masks.csv"
OUTPUT_IP_LIST_FNMAE = "ip_lists/ipv4_list.txt"
#exceptions
#ERROR_STRING = "-1"

def ip_2_dec(ip):
	packedIP = socket.inet_aton(ip)
	return struct.unpack("!L", packedIP)[0]

def dec_ip_2_ip(dec_ip):
	return socket.inet_ntoa(struct.pack('!L', dec_ip))

#need a function that pics random ip and change 0's in ip mask to random number
def gen_rand_ipv4():

	r = random.randrange
	random_int = r(0,len(ip_masks))
	ip_mask_bottom = ip_masks[random_int][0]
	ip_mask_top = ip_masks[random_int][1]

	#ip that will be eventually returned
	#random_ip_list = ['1','1','1','1']
	random_ip_list = [str(r(1,255)) for x in range(0,4)]

	#break upper and lower limits up by '.'
	#compare strings for common numbers
	broken_bottom = ip_mask_bottom.split('.')
	broken_top = ip_mask_top.split('.')

	for i in range (0,3):

		if broken_bottom[i] == broken_top[i]:
			random_ip_list[i] = broken_bottom[i]
		elif int(broken_bottom[i]) < int(broken_top[i]):
			r = random.randrange
			random_int = r(int(broken_bottom[i]),int(broken_top[i]))
			random_ip_list[i] = str(random_int)
		elif int(broken_bottom[i]) > int(broken_top[i]):
			r = random.randrange
			random_int = r(int(broken_top[i]),int(broken_bottom[i]))
			random_ip_list[i] = str(random_int)
		else:
			print ("not always upper lower")

	return '.'.join(random_ip_list)

def ip_check_ping(ip):
    response = os.system("ping -c 1 " + ip)
    # and then check the response...
    if response == 0: return True
    return False

#add range to ip address
def add_range(ip):
	ip = ip.split('.')
	ip[3] = '0/24'
	ip = '.'.join(ip)
	return ip

"""
				start program
"""
#import all country code masks
ip_masks = []
with open(COUNTRY_RANGES_FNAME, mode='r') as infile:
	reader = csv.reader(infile)
	for row in reader:
		#ip_masks.append(dec_ip_2_ip(int(row[0])))
		#print (dec_ip_2_ip(int(row[0])) + "   --   " + dec_ip_2_ip(int(row[1])))
		ip_masks.append([dec_ip_2_ip(int(row[0])), dec_ip_2_ip(int(row[1]))])
		#print (" -> " + str(gen_rand_ipv4(ip_masks[-1][0], ip_masks[-1][1])))


if __name__ == '__main__':
	#settings
	NUM_IPS = int(sys.argv[1])		#num ips specified as command line argument

	# write list of random ips to specified file path
	with open(OUTPUT_IP_LIST_FNMAE, 'w') as f:
		for i in range(0, NUM_IPS):
			f.write(gen_rand_ipv4())
			f.write("\n")


