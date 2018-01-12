#!/usr/bin/python3

import argparse # argv
import requests # http requests
import re       # regular expressions
import time     # delay

# regular expressions
html_link_re = 'href[ \t]*="(.+?)"' # matches 'href = "<link>"'
remote_link_re = '^http.*' # string starts with 'http'

#
# TODO: filter for extensions (.ico, .jpg, etc..), parse robot.txt
#

# parse arguments
parser = argparse.ArgumentParser(description='whisky - a curious spider')
parser.add_argument('max_req', metavar='max-req', type=int, help='max number of requests')
parser.add_argument('delay', metavar='delay', type=float, help='delay between requests (seconds)')
parser.add_argument('url_list', metavar='url', type=str, nargs='+', help='list of URLs')

args = parser.parse_args()
max_jumps = args.max_req
delay_between_requests = args.delay # seconds
queue = args.url_list

# set of visited URLs
visited_urls = set()

jump_counter = 0
while ((jump_counter < max_jumps) and (len(queue) > 0)):
	
	# pop from queue
	current_request = queue.pop()
	
	try:
		# http request
		print ('> sending request for ' + current_request)
		page = requests.get(current_request);

		# match links
		links = re.findall(html_link_re, page.text);

		# examine links, add prefix if needed
		for hit in links:
			if (re.match(remote_link_re, hit) == None):
				# local link
				hit = current_request + hit;

			# remove multiple backslashes
			hit = re.sub('/+','/',hit)
			# restore http:// and https://
			hit = re.sub('http:/','http://',hit)
			hit = re.sub('https:/','https://',hit)

			# add new URL to queue
			if (not hit in visited_urls):
				print ('+ adding ' + hit)
				queue.append(hit)
				visited_urls.add(hit)

		# increment jump counter
		jump_counter = jump_counter + 1
		
	except:
		print ('*** request error for ' + current_request)
		
	# delay
	time.sleep(delay_between_requests)

