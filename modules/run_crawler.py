#! /bin/env python3

from collections import deque
from urllib.parse import urlsplit
import pandas
from colorama import Fore
import logging 
from modules import htmlParser


ROOT_LOGGER = logging.getLogger("Icrawl")

# Sets of found interesting data
emails = set()
phone_numbers = set()
addresses = set()
api_keys = set()
access_tokens = set()
auth_tokens = set()
Hashes = set()
custom_matches = set()
scraped_url = set()

# Colors		
green = Fore.GREEN
yellow = Fore.YELLOW
blue = Fore.BLUE
red = Fore.RED
norm = Fore.RESET


# Boxes
fbox = f"{green}[+]{norm}"
box = "[+]"
ibox = f"{yellow}[+]{norm}"
error = f"{red}[!]{norm}"

# Use sets to make into a dataframe for nicer printing
# Returns a dict with key as URL and value as a dataframe
def make_dataframe(frame_name, emails,phone_numbers, addresses,  auth_tokens,  access_tokens,  hashes, api_keys, custom_matches,):
	dframes = {}
	df = pandas.DataFrame()

		# Emails
	if len(emails) != 0:
		df["Emails"] = pandas.Series(list(emails))
		ROOT_LOGGER.info(f"Adding {len(emails)} possible emails to datafame")
	
	# Phone numbers
	if len(phone_numbers) != 0:
		df["Phone Numbers"] = pandas.Series(list(phone_numbers))
		ROOT_LOGGER.info(f"Adding {len(phone_numbers)} possible phone numbers to dataframe")

		# Addresses
	if len(addresses) != 0:
		df["Possable Addresses"] = pandas.Series(list(addresses))
		ROOT_LOGGER.info(f"Adding {len(addresses)} possible street addresses to dataframe")

	# auth tokens
	if len(auth_tokens) != 0: 
		df["Possible Auth Tokens"] = pandas.Series(list(auth_tokens))
		ROOT_LOGGER.info(f"Adding {len(auth_tokens)} possible auth tokens to dataframe")
	
	# Api keys
	if len(api_keys) != 0: 
		df["Possible Api Keys"] = pandas.Series(list(api_keys))
		ROOT_LOGGER.info(f"Adding {len(api_keys)} possible API keys to dataframe")

	# Access tokens
	if len(access_tokens) != 0: 
		df["Possible Access Tokens"] = pandas.Series(list(access_tokens))
		ROOT_LOGGER.info(f"Adding {len(access_tokens)} possible access tokens to dataframe")
		
	# Password hashes
	if len(hashes) != 0: 
		df["Possible Password Hash"] = pandas.Series(list(access_tokens))
		ROOT_LOGGER.info(f"Adding {len(access_tokens)} possible password hash to dataframe")
		
	# Custom regex
	if len(custom_matches) != 0: 
		df["Custom Resaults"] = pandas.Series(list(custom_matches))
		ROOT_LOGGER.info(f"Adding {len(custom_matches)} possible custom matches to dataframe")

	# Adding dataframe to list of dataframes
	if len(df) > 0:
		ROOT_LOGGER.info(f"Final number of dataframe elements : {len(df)}")
		df = df.fillna("")
				
		dframes[frame_name] = df
		return dframes

	else:
		ROOT_LOGGER.error("No data was added to the dataframe")		
		return None
	

	
def crawler(args, spider):
	# Sets of found interesting data
	emails = set()
	phone_numbers = set()
	addresses = set()
	api_keys = set()
	access_tokens = set()
	auth_tokens = set()
	Hashes = set()
	custom_matches = set()
	scraped_url = set()

	# Colors		
	green = Fore.GREEN
	yellow = Fore.YELLOW
	blue = Fore.BLUE
	red = Fore.RED
	norm = Fore.RESET


	# Boxes
	fbox = f"{green}[+]{norm}"
	box = "[+]"
	ibox = f"{yellow}[+]{norm}"
	error = f"{red}[!]{norm}"
	
	returned_resaults = []


	# Breaking up the given url into 3 parts scheme=https:// netloc=domainName path=subDirectorys
	unscraped_url = deque([args.url])
	parts = urlsplit(args.url)
	base_url = f"{parts.scheme}://{parts.netloc}"
	ROOT_LOGGER.info(f"Crawler has started")
	
	
	# Run the loop until all urls are scraped or until max count is reached
	try:
		while len(unscraped_url) and len(scraped_url) <= args.count -1:
			dframes = {}
			# Grabbing new url from the list
			URL = unscraped_url.popleft()
			scraped_url.add(URL)
			
			if args.verbose:
				print(f"{ibox} Crawling {blue}{URL}{norm}")
			
			ROOT_LOGGER.info(f"Crawling URL : {base_url}")
			
			# Getting the html of the url
			soup = htmlParser.get_source(URL)

			# No html was returned so continue onto the next url
			if soup == None:
				ROOT_LOGGER.error(f"No HTML was returned for URL : {URL}")
				continue
						
			# Formatting the html (not needed but here we are)
			content = soup.prettify()

			# Searching the html for regex matches
			emails, phone_numbers, addresses, auth_tokens, Hashes, access_tokens, api_keys, custom_matches = htmlParser.search_html(args, content,emails, phone_numbers, addresses, auth_tokens, Hashes, access_tokens, api_keys, custom_matches,)
			
			ROOT_LOGGER.info(f"Regex resaults emails={len(emails)} phone_numbers={len(phone_numbers)} addresses={len(addresses)} auth_tokens={len(auth_tokens)} hashes={len(Hashes)} access_tokens={len(access_tokens)} api_keys={len(api_keys)} custom_matches={len(custom_matches)}")
			
			# Getting all the new links found in the html and adding them to the unscraped list
			if spider:
				ROOT_LOGGER.info(f"Spidering  URL : {URL}")
				details = htmlParser.Regex(html_content=soup,base_url=base_url, unscraped_url=unscraped_url,scraped_url=scraped_url,custom_regexs=custom_matches,)
				unscraped_url = htmlParser.Regex.get_links(details)
				ROOT_LOGGER.info(f"Number of unscraped_urls={len(unscraped_url)}")

			# Taking found resaults and making them into a dataframe
			dframes = make_dataframe(URL, emails,phone_numbers,addresses, auth_tokens, access_tokens, Hashes, api_keys, custom_matches)
			
			if dframes == None:	
				continue
			
			returned_resaults.append(dframes)

			
			# Clearing found resaults for next iteration in the loop
			emails.clear()
			phone_numbers.clear()
			addresses.clear()
			api_keys.clear()
			access_tokens.clear()
			auth_tokens.clear()
			Hashes.clear()
			custom_matches.clear()

	except KeyboardInterrupt:
		if args.verbose:
			print(f"{error} Keyboard interrupt stopping crawler")
		return returned_resaults, list(scraped_url)

	return returned_resaults ,list(scraped_url)
