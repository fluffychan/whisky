#/usr/bin/python3

import requests # http requests
import re       # regular expressions
import time

html_link_re = 'href[ \t]*="(.+?)"' # matches 'href = "<link>"'

remote_link_re = '^http.*' # string starts with 'http'


#
# TODO: visited queue, user input (max_jumps, delay, first url, etc..)
#


max_jumps = 30

delay_between_requests = 0.1 # seconds


jump_counter = 0

queue = ['']

while ((jump_counter < max_jumps) and (len(queue) > 0)):
	
	# pop from queue
	current_request = queue.pop()
	
	try:
		# http request
		print ('sending request for ' + current_request)
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

			# add link to queue
			print ('+ adding ' + hit)
			queue.append(hit)

		# increment jump counter
		max_jumps = max_jumps + 1
		
		break
	except error:
		print ('error:' + error)
		
	# delay
	time.sleep(delay_between_requests)

