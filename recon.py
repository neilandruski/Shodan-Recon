#!/usr/bin/python3

import argparse, os, sys, logging
try:
	import shodan
except ImportError as e:
	print("{} not imported. Please install before running".format(e))
	#sys.exit(1)

'''
TODO:
-Test shodan functionality
-Building logging functions for normal, verbose, and quiet
-Build out arguement parser more
'''
__version__ = "0.1"

IP_LIST=[]
FACETS=[]
SHODAN_API_KEY = "insert your API key here"
CWD=os.getcwd() + "/" #Current Working Directory

def check_ip_file(fname):
	#If single IP append and return from function
	if(not os.path.isfile( CWD + fname )):
		IP_LIST.append(fname)
		return
	with open(fname,"r") as file:
		for line in file:
			IP_LIST.append(line.rstrip('\n'))

def shodan_scan(IP):
	api = shodan.Shodan(args.key)
	try:
		results = api.host(IP)
		return results
	except shodan.APIError as e:
		return 'Error: {}'.format(e)

"""
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
TODO: 
Build out face to take sets not lists for formatting
"""
def load_facet(fname):
	if(not os.path.isfile( CWD + fname )):
		return "Error"
	with open(fname, "r") as file:
		for line in file:
			FACETS.append(line.rstrip('\n'))

"""
Main function for running the script.
After args have been evaluated loop through given IPs and use Shodan to scan 
"""
def main():
	if(args.quiet):
		logger.info("quiet log")
		return
	print(IP_LIST)

	if(args.verbose):
		print(args.key)
		print(args.verbose)
		print(args.quiet)
		print(args.output)
'''
	for ipaddr in IP_LIST:
		result = shodan_scan(ipaddr)
'''

if __name__ == '__main__':
	"""
	Argument parser to build clarity for future users
	Only runs if the file is run as a scripit and not as an immport into another script
	!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
	TODO: 
	build out all arguments , descriptions, 
	Build out facet load
	"""
	parser = argparse.ArgumentParser(
		prog='recon',
		description='''Script to parse through given urls/IPs and run scan through Shodan api
		''',
		epilog='''
		''')
	parser.add_argument("-i", "--ip",  help="Single IP or multiple from file[one IP per line]", required=True, type=check_ip_file)
	parser.add_argument("-k", "--key", help="Set Shodan API key", type=str) #add required true when done building
	parser.add_argument("-o", "--output", help="File to save to(appends to existing or makes a file)", type=str)
	parser.add_argument("-f", "--facet", help="Select specific properties from Shoda results[one facet per line]", type=load_facet)

	print_method = parser.add_mutually_exclusive_group()
	print_method.add_argument("-v", "--verbose",  help="Prints results while running", action="store_true")
	print_method.add_argument("-q", "--quiet",  help="Script runs without printing", action="store_true")

	args = parser.parse_args()

	'''
	Logger used to write to file and console
	Verbose will print out all findings as they are returned
	Normal will print out updates but not details
	Quiet will not print - must have output chosen!
	'''
	# create logger with 'spam_application'
	logger = logging.getLogger('Recon.py')
	logger.setLevel(logging.DEBUG)
	# create file handler which logs even debug messages
	fh = logging.FileHandler('spam.log')
	fh.setLevel(logging.DEBUG)
	# create console handler with a higher log level
	ch = logging.StreamHandler()
	ch.setLevel(logging.DEBUG)
	# create formatter and add it to the handlers
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	fh.setFormatter(formatter)
	ch.setFormatter(formatter)
	# add the handlers to the logger
	logger.addHandler(fh)
	logger.addHandler(ch)

	main()
