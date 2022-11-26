#! /bin/env python3


import os 
from colorama import Fore
import logging 
from sys import platform
from time import sleep
from modules.sendRequest import sender
from modules.htmlParser import Parser


ROOT_LOGGER = logging.getLogger("Icrawl")

# Colors
green = Fore.GREEN
blue = Fore.BLUE
yellow = Fore.YELLOW
red = Fore.RED
norm = Fore.RESET
cyan = Fore.CYAN

# Boxes
fbox = f"{green}[+]{norm}"
ibox = f"{yellow}[+]{norm}"
error = f"{red}[!]{norm}"



# Print the current stats of the running script
def dork_stats(num_of_links, payload, returned_links, num, timeout, Proxy, queary):
	if platform == "win32":
		os.system("cls")
	else:
		os.system("clear")

	print(f"{ibox} Number of links to return per dork  : {num_of_links}")
	print(f"{ibox} Number of searches remaining        : {len(payload) - num}")
	print(f"{ibox} Number of urls to recive            : {num_of_links * len(payload)}")
	print(f"{ibox} Number of dorks to use              : {len(payload)}")
	print(f"{ibox} Number of found links               : {len(returned_links)}")
	print(f"{ibox} Completed searches                  : {num}/{len(payload)}")
	print(f"{ibox} Request timeout                     : {timeout} seconds")
	print(f"{ibox} Current Proxy                       : {Proxy}")
	print(f"{ibox} Current dork                        : {queary}")
	print(f"{ibox} Press CTRL-C to stop the search")


# Main
# Loops through a list of google dorks and sends the dorks as google searches
# Grabs a new proxy with every new google dork
# Prints the current stats to the screen
# Returns a set of links returned from the google searches
def run_search(payload, num_of_links=5, timeout=30):
	counter = 0
	returned_links = set()
	burned_proxies = []
	
	client = sender(google=True, burned_proxys=burned_proxies)
	client.get_user_agent()
	client.get_proxy()
	client.get_headers()
	try:
		# looping through the list of google dorks and sending a request with every new dork
		for queary in payload:
			ROOT_LOGGER.debug(f"Current google dork : {queary}")

			client.url = (
							f"https://www.google.{client.tld}/search?hl={client.lang}&"
							f"q={queary}&num={num_of_links}&btnG=Google+Search&tbs={client.tabs}&"
							f"safe={client.safe}&cr={''}&filter=0"
						)
			dork_stats(num_of_links, payload, returned_links, counter, timeout, client.proxy, queary)
			soup = client.google_connection()
			counter += 1
			
			if soup == 429:
				burned_proxies.append(client.proxy)		
				print(f"\n{error} Oops it looks like the current proxie has been blocked by google : {client.proxy}")
				ROOT_LOGGER.debug(f"Proxie has been burned : {client.proxy}")
				print(f"{ibox} Adding proxy to burned proxy list")
				client.burned = burned_proxies
				print(f"{ibox} Grabbing new proxie")
				client.get_proxy()
				if client.proxy == "":
					print(f"{error} Oops it looks like theres no other proxies to use")
					print(f"{ibox} Returning with current resaults")
					return returned_links
				else:
					client.get_user_agent()
					client.get_headers()
					print(f"{ibox} New proxie : {client.proxy}")
					ROOT_LOGGER.debug(f"New proxy {client.proxy}")
					sleep(timeout)
					continue
			elif soup in range(206, 450):
				ROOT_LOGGER.error(f"Reviced un expected status code Status code : {soup}")
				dork_stats(num_of_links, payload, returned_links, counter, timeout, client.proxy, queary)
				sleep(timeout)
				continue
			elif soup == "Timeout":
				ROOT_LOGGER.debug(f"Request timed out on query : {queary}")
				dork_stats(num_of_links, payload, returned_links, counter, timeout, client.proxy, queary)
				sleep(timeout)
			elif soup == "Connection error":
				ROOT_LOGGER.error(f"There was a connection error with the query : {queary}")
				dork_stats(num_of_links, payload, returned_links, counter, timeout, client.proxy, queary)
				sleep(timeout)
			else:
				
				p = Parser(soup, links=True, google=True)
				new_links = p.parse_html()
				num = 0 
				for link in new_links["links"]:
					returned_links.add(link)
					num += 1
					if num == num_of_links:
						break
				dork_stats(num_of_links, payload, returned_links, counter, timeout, client.proxy, queary)
				sleep(timeout)
	except KeyboardInterrupt:
		ROOT_LOGGER.debug(f"Keyboard interrupt returning {len(returned_links)} found links")
		return returned_links	

	return returned_links


