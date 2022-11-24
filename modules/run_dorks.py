#! /bin/env python3

import os 
from colorama import Fore
import logging 
from modules.GoogleSearch import googleSearch
from sys import platform
from random import choice



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
box = f"[+]"
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
	print(f"{ibox} Request timeout                     : {timeout}")
	print(f"{ibox} Current Proxy                       : {Proxy}")
	print(f"{ibox} Current dork                        : {queary}")


# Read proxies.txt file and add all proxies in the file to a list		
def get_proxy_list():
	proxys = []
	file_path = __file__
	proxy_path = file_path.replace("run_dorks.py", "proxies.txt")

	with open(proxy_path, "r") as f:
		content = f.readlines()
					
	for line in content:
		if line.strip() != "":
			proxys.append(line.strip())
		
	return proxys


# Main
# Loops through a list of google dorks and sends the dorks as google searches
# Grabs a new proxy with every new google dork
# Prints the current stats to the screen
# Returns a set of links returned from the google searches
def run_search(payload, num_of_links=5, timeout=30):
	num = 0
	returned_links = set()
	list_of_proxys = get_proxy_list()


	print(f"{ibox} Starting google dork search")
	print(f"{ibox} Press CTRL-C to stop the search")
	

	client = googleSearch(
		timeout_between_requests=timeout,
		timeout_between_new_page=timeout,
	)		
	

	# Grabbing a proxie if there are proxies in the list
	if len(list_of_proxys) != 0:
		Proxy = list_of_proxys[0]
	else:
		Proxy = ""

	client.get_user_agent()

	# looping through the list of google dorks and sending a request with every new dork
	for queary in payload:
		ROOT_LOGGER.info(f"Current google dork : {queary}")


		client.proxy = Proxy
		client.queary = queary
		client.num_of_links_to_return = num_of_links
		dork_stats(num_of_links, payload, returned_links, num, timeout, Proxy, queary)		
		new_links = client.start_google_connection()

		try:			
			for i in new_links:
				returned_links.add(i)
		except TypeError:
			pass
		
		if "Blocked ip" in returned_links:
			
			if len(list_of_proxys) > 1:
				print(f"\n{error} Oops it looks like the current proxie has been blocked by google : {Proxy}")
				ROOT_LOGGER.error(f"Proxie has been burned : {Proxy}")
				print(f"{ibox} Romoving burned proxie from proxie list")
				list_of_proxys.remove(Proxy)
				ROOT_LOGGER.info(f"Removing burned proxie from proxie list PROXIE : {Proxy}")
				print(f"{ibox} Grabbing new proxie")
				Proxy = list_of_proxys[0]
				client.get_user_agent()
				print(f"{ibox} New proxie : {Proxy}")


			else:
				print(f"{error} No other proxies to use returning current resaults")
				ROOT_LOGGER.error(f"No other proxies to use returning current resaults")
				break

		if queary == payload[-1]:
			break
		
		num += 1
	
		
	return list(returned_links)


