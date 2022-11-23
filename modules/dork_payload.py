#! /bin/env python3

import os
import logging
from sys import platform
from time import sleep
from colorama import Fore



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

# Gets the path of the modules/dorks directory 
# Adds all files in the dorks directory to a list
# Adds 2 filenames from the list and adds them as the value for a dict 
# returns a list of filenames and a dict of key=number value=filename
def get_dorks():
	try:
		path = __file__
		dorks_path = path.replace("dork_payload.py", "dorks")
		dork_files = os.listdir(dorks_path)
			
		dork_dict =	{}
		gDorks = []
		spaces = " "
		num = 0
		num1 = 0
		num2 = 1
		max_string_length = 45

		# Making a dict of files and there index number  key=number value=filename
		for file in dork_files:
			dork_dict[num] = file
			num += 1

		# Iterating through the dork_files list two elements at a time
		# Making a string to pring to the user with both elements
		# adding new string to a list 
		for v, w in zip(dork_files[::2],dork_files[1::2]):
			string = f"[{num1}] {v}"
			string_length  = len(string)
			space = max_string_length - string_length
			string = f"[{num1}] {v}{spaces*space}[{num2}] {w}"
			num1 += 2
			num2 += 2
			gDorks.append(string)
	except Exception as e:
		ROOT_LOGGER.error(f"Get dorks failed because {e}")
		
	return gDorks, dork_dict
	
# Clears the screan based on the operating system
def clear_screan():
	if platform == "win32":
		os.system("cls")
	else:
		os.system("clear")

# Main
# Asking the user what google dorks to use and the setting to use	
def get_payload():
	list_of_dorks = set()
	dork_list, dork_dict = get_dorks()

	try:
		# Asking what google dork file to use
		while True:	
			clear_screan()		
			for dork in dork_list:
				print(dork)
			try:
				dork_search = input(f"\n{ibox} What type of google dorks would you like to run: ")
				if int(dork_search) not in dork_dict:
					ROOT_LOGGER.error(f"Invalid input for dork selection : {dork_search}")
					print(f"{error} Invalid option")
					sleep(0.8)
					continue
					
			except ValueError:
				ROOT_LOGGER.error(f"Invalid input for dork selection : {dork_search}")
				print(f"{error} Invalid option")
				sleep(0.8)
				continue
			except KeyboardInterrupt:
				ROOT_LOGGER.error("Keyboard Interrupt exiting payload setup")
				print(f"\n{error} Keyboard interrupt quitting dorks")
				print("Goodbye")
				exit()
			ROOT_LOGGER.debug(f"Dork file selected : {dork_dict[int(dork_search)]}")
			break

		# Getting the dork files full path
		dorks_path = os.path.abspath("modules/dorks/" + dork_dict[int(dork_search)])
		ROOT_LOGGER.debug(f"Dork file full path : {dorks_path}")

		# Reading the dork file and adding content to a list
		with open(dorks_path, "r") as f:
			content = f.readlines()

		# Asking how much quearys to run		
		while True:
			clear_screan()
			try:
				num_of_dorks = input(f"{ibox} How many dorks would you like to run?          (Default : 10): ")
				if num_of_dorks == "":
					num_of_dorks = 10
				else:
					num_of_dorks = int(num_of_dorks)
					
				ROOT_LOGGER.debug(f"Number of dorks to use : {num_of_dorks}")
				break
			except ValueError:
				ROOT_LOGGER.error(f"Invalid input for number of dorks : {num_of_dorks}")
				print(f"{error} Number of searches must be a number")
			except KeyboardInterrupt:
				ROOT_LOGGER.error("Keyboard Interrupt exiting payload setup")
				print(f"\n{error} Keyboard interrupt quitting dorks")
				print("Goodbye")
				exit()

		# Asking how many links to recive
		while True:
			num_of_links = input(f"{ibox} How many links do you want to recive per dork? (Default : 10): ")
			try:
				if num_of_links == "":
					num_of_links = 10
					break

				num_of_links = int(num_of_links)
				ROOT_LOGGER.debug(f"Number of links to recive : {num_of_links}")
				break
			except ValueError:
				ROOT_LOGGER.error(f"Invalid input for number of links : {num_of_links}")
				print(f"{error} number of links must be a number")
			except KeyboardInterrupt:
				ROOT_LOGGER.error("Keyboard Interrupt exiting payload setup")
				print(f"\n{error} Keyboard interrupt quitting dorks")
				print("Goodbye")
				exit()
			
		# Asking for the delay between request 
		# Defaults to 30 seconds
		timeout = input(f"{ibox} Set timeout between requests                   (Default : 10): ")
		try:				
			timeout = int(timeout)
		except ValueError:
			timeout = 10

		ROOT_LOGGER.debug(f"Timeout between searches : {timeout}")

		#  Loading dorks into a set so there is no repeats
		num = 0
		for i in range(len(content)):
			if num == num_of_dorks:
				break
			list_of_dorks.add(content[i].strip())
			num += 1
			
		# Showing the user the current set settings
		clear_screan()
		print(f"{ibox} Number of urls to recive  : {num_of_links}")
		print(f"{ibox} Number of dorks to use    : {len(list_of_dorks)}")
		print(f"{ibox} Timeout between requests  : {timeout}")
		print(f"{ibox} Dork filename             : {dork_dict[int(dork_search)]}")


		pdorks = input(f"\n{ibox} Use current settings?: ")
		if pdorks.lower() == "n":
			get_payload()
			
	
		clear_screan()
		ROOT_LOGGER.debug(f"Final settings : numOfLinks={num_of_links}, NumOfDorks={len(list_of_dorks)}, Timeout={timeout}, DorkFile={dork_dict[int(dork_search)]}")
		

		return list(list_of_dorks), num_of_links, timeout
		
	except KeyboardInterrupt:
		ROOT_LOGGER.error("Keyboard Interrupt exiting payload setup")
		print(f"\n{error} Keyboard interrupt quitting dorks")
		print("Goodbye")
		exit()

