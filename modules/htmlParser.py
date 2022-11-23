#! /bin/env python3
import logging
from bs4 import BeautifulSoup
import requests
import re
from colorama import Fore

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

ROOT_LOGGER = logging.getLogger("Icrawl")

class Regex:
	def __init__(self, html_content, base_url="", unscraped_url="", scraped_url="", custom_regexs=""):
		self = self
		self.html_content = html_content
		self.custom_matches = custom_regexs
		self.base_url = base_url
		self.unscraped_url = unscraped_url
		self.scraped_url = scraped_url

		
	def phone_number(self):
		phone_number_regexs = [
		  	"[0-9]{4} [0-9]{3} [0-9]{3}",
			"[0-9]{4}-[0-9]{3}-[0-9]{3}",
		   	"[0-9]{3} [0-9]{3} [0-9]{4}",
			"[0-9]{3}-[0-9]{3}-[0-9]{4}",
			"\+[0-9]{2} [0-9]{2} [0-9]{3} [0-9]{3}",
			"\+[0-9]{2}-[0-9]{2}-[0-9]{3}-[0-9]{3}",
			"[0-9]{2} [0-9]{2} [0-9]{3} [0-9]{3}",
			"[0-9]{2}-[0-9]{2}-[0-9]{3}-[0-9]{3}",
		    "\([0-9]{3}\) [0-9]{3} [0-9]{4}",
			"\+[0-9]{2} [0-9]{3} [0-9]{3} [0-9]{3}", 
			"\+[0-9]{2}-[0-9]{3}-[0-9]{3}-[0-9]{3}",
			"\+[0-9]{1} [0-9]{3} [0-9]{3} [0-9]{4}", 
			"\+[0-9]{1}-[0-9]{3}-[0-9]{3}-[0-9]{4}", 
			"\+[0-9]{2} [0-9]{4} [0-9]{3} [0-9]{3}",
			"\+[0-9]{2}-[0-9]{4}-[0-9]{3}-[0-9]{3}"
			]

		phone_numbers = set()
		# Iterating throught phone_number_regexs and checking for any matches in the given html and adding all found matches to the set
		for regex in phone_number_regexs:
			for re_match in re.finditer(regex, str(self.html_content)):
				ADD = True
				for number in phone_numbers:
					if re_match.group() in str(number):
						ADD = False
				
				if ADD:	
					phone_numbers.add(re_match.group())

		return phone_numbers

	# Uses regular expressions to search for email addresses 
	def email(self):
		email_regex = r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""
		emails = set()
		
		# Searching the html for emails using the email_regex and addes found resaults to the set
		for re_match in re.finditer(email_regex, str(self.html_content)):
			emails.add(re_match.group())

		return emails

	# Uses regular expression to search for street addresses
	def addresses(self):
		address_regexs = [
			"[0-9]{1,5} [a-zA-Z]{1,20} [a-zA-Z]{1,6} [a-zA-Z]{1,20}",
			"[0-9]{1,5} [a-zA-Z]{1,20} [a-zA-Z]{1,6}",
			"[0-9]{1,5} [a-zA-Z]{1,20} [a-zA-Z]{1,20} [a-zA-Z]{1,20} [a-zA-Z]{1,20}",
			"[0-9]{1,5}( [a-zA-Z.]*){1,4},?( [a-zA-Z]*){1,3},? [a-zA-Z]{2},? [0-9]{5}",
			"/[0-9]+[ |[a-zà-ú.,-]* ((highway)|(autoroute)|(north)|(nord)|(south)|(sud)|(east)|(est)|(west)|(ouest)|(avenue)|(lane)|(voie)|(ruelle)|(road)|(rue)|(route)|(drive)|(boulevard)|(circle)|(cercle)|(street)|(cer\.)|(cir\.)|(blvd\.)|(hway\.)|(st\.)|(aut\.)|(ave\.)|(ln\.)|(rd\.)|(hw\.)|(dr\.)|(a\.))([ .,-]*[a-zà-ú0-9]*)*/i", 
			]

		addresses = set()

		# Iterating throught address_regexs and checking for any matches in the given html and adding all found matches to the set
		for regex in address_regexs:
			for re_match in re.finditer(regex, str(self.html_content)):
				ADD = True
				for address in addresses:
					if str(re_match) in address:
						ADD = False
						print("already there ")
					else:
						ADD = True
				
				if ADD:
					addresses.add(re_match.group())

		return addresses

	# Uses regular expression to search for api keys
	def api_keys(self):
		api_regexs = [
			"AIza[0-9A-Za-z-_]{35}",
			"sk_live_[0-9a-z]{32}",
			"55[0-9a-fA-F]{32}",
			"key-[0-9a-zA-Z]{32}",
			"[0-9a-f]{32}-us[0-9]{1,2}",
			"[A-Za-z0-9_]{21}--[A-Za-z0-9_]{8}",
			"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}",
			]

		api_keys = set()

		# Iterating throught api_regexs and checking for any matches in the given html and adding all found matches to the set
		for regex in api_regexs:
			for re_match in re.finditer(regex, self.html_content):
				api_keys.add(re_match.group())

		return api_keys

	# Uses regular expression to search for access tokens
	def acces_tokens(self):
		token_regexs = [
			"EAACEdEose0cBA[0-9A-Za-z]+",
			"[1-9][ 0-9]+-[0-9a-zA-Z]{40}",
			"EAACEdEose0cBA[0-9A-Za-z]+",
			"sqOatp-[0-9A-Za-z-_]{22}",
			"access_token,production$[0-9a-z]{161[0-9a,]{32}",
			"amzn.mws.[0-9a-f]{8}-[0-9a-f]{4}-10-9a-f1{4}-[0-9a,]{4}-[0-9a-f]{12}",
			"xoxb-[0-9]{11}-[0-9]{11}-[0-9a-zA-Z]{24}"
			]

		access_tokens = set()

		# Iterating throught token_regexs and checking for any matches in the given html and adding all found matches to the set
		for regex in token_regexs:
			for re_match in re.finditer(regex, str(self.html_content)):
				access_tokens.add(re_match.group())
		
		return access_tokens

	# Uses regular expression to search for authentication tokens 
	def auth_token(self):
		auth_regex = [
			"[A-Za-z0-9]{125} (counting letters [2])",
			"[0-9a-fA-F]{7}.[0-9a-fA-F]{32",
			"4/[0-9A-Za-z-_]{6,43}",
			"1/[0-9A-Za-z-]{43}|1/[0-9A-Za-z-]{64",
			"ya29.[0-9A-Za-z-_]+",
			"[A-Za-z0-9_]{255}",
			"q0csp-[ 0-9A-Za-z-_]{43}",
			"amzn.mws.[0-9a-f]{8}-[0-9a-f]{4}-10-9a-f1{4}-[0-9a,]{4}-[0-9a-f]{12}",
			"xoxb-[0-9]{11}-[0-9]{11}-[0-9a-zA-Z]{24}",
			"xoxp-[0-9]{11}-[0-9]{11}-[0-9a-zA-Z]{24}",
			"xoxe.xoxp-1-[0-9a-zA-Z]{166}",
			"xoxe-1-[0-9a-zA-Z]{147}"
			"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}",
			"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}",
			]

		auth_tokens = set()
		# Iterating throught address_regexs and checking for any matches in the given html and adding all found matches to the set
		for regex in auth_regex:

			for re_match in re.finditer(regex, str(self.html_content)):
				auth_tokens.add(re_match.group())

		return auth_tokens
	
	# Uses regular expression to search for password hashes
	def hashes(self):
		hash_regex = [
			"\$1\$.*?\$.{22}",
			"\$y\$.*?\$.{85}",
			"\$6\$.*?\$.{86}",
			"\$5\$.*?\$.{43}",
			"\$6\$.{1,53}",
			"\$y\$.{1,53}",
			"\$1\$.{1,53}",
			"\$2a\$.{1,53}",
			"\$5\$.{1,53}",
			]

		hashes = set()
		# Iterating throught hash_regexs and checking for any matches in the given html and adding all found matches to the set
		for regex in hash_regex:

			for re_match in re.finditer(regex, str(self.html_content)):
				hashes.add(re_match.group())

		return hashes

	# Use user given regular expressions to find pattern matches
	def custom_regex(self):
		custom_matches = set()
		# Iterating throught custom_regexs and checking for any matches in the given html and adding all found matches to the set
		for regex in self.custom_regexs:
			for re_match in re.finditer(regex, str(self.html_content)):
				custom_matches.add(re_match.group())

		return custom_matches

	# Uses regex to find all the href links in given HTML
	def get_links(self):
		for _ in self.html_content:
			link_regex = [
				'href="https://.*?"',
				'href="/.*?"',
				'href="http://.*?"',
				]
				
			for regex in link_regex:
				# Searching for regex matches
				for re_match in re.finditer(regex, str(self.html_content)):
					weblink = re_match.group()
						
					# Cleaning up new link
					weblink = weblink.replace('href="', '')
					weblink = weblink.replace('"', '')
						
					# Making a new url with found links
					if weblink.startswith('/'):
						weblink = self.base_url + weblink
					elif not weblink.startswith('https'):
						weblink = weblink

						
					# Checking if link has been scraped before if not adding it to the list
					if self.base_url in weblink:
						if weblink not in self.unscraped_url and weblink not in self.scraped_url:
							self.unscraped_url.append(weblink)

		ROOT_LOGGER.info(f"URLS returned : {len(self.unscraped_url)} ")

		return self.unscraped_url

# Gets the HTML code of a given url
def get_source(url, user_agent=""):		
	try:
		if user_agent != "":
			user_agent = user_agent
		else:
			user_agent = 'Mozilla/5.0 (Linux; U; Android 4.1.1; en-gb; Build/KLP) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Safari/534.30'
		
		headers = {
			'User-Agent': user_agent,
			"Accept-Language":"en-US,en;q=0.5"
		}

		# Sending get request to given url
		get_request = requests.get(url, headers=headers)
	
	except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError, requests.exceptions.InvalidURL) as e:
		ROOT_LOGGER.error(f"Failed request {e}")
		return None

	# If the status code wasnt a 200 responce then there will be no interesting data in the html so just return None
	if int(get_request.status_code) != 200:
		ROOT_LOGGER.error(f"Status code error  Status : {get_request.status_code}")
		return None

	ROOT_LOGGER.info(f"Returned HTML for {url}")
	# Using BeautifulSoup to parse to html of the page
	try:
		soup = BeautifulSoup(get_request.text, "lxml")
	except Exception as e:
		print(f"[!] Oops something went wrong\n Error : {e}")
		ROOT_LOGGER.error(f"something went wrong parsing html to beautifulsoup Error : {e}")
		return None
	
	return soup

def shodan_get_info(ip):
	url = f"https://www.shodan.io/host/{ip}"
	soup = get_source(url)

	name = []
	value = []
	for tag in soup.find_all("td"):
		string = str(tag.contents)
		string = string.replace("['")
		string = string.replace("']")
		if " " in string:
			if "href=" in str(tag.contents):
				for i in re.finditer('href=".*?>*?<', str(tag.contents)):
					string = i.group()
					string_list = string.split(">")
					string = string_list[1]
					string_list = string.split("<")
					string = string_list[0]
					value.append(string)
		else:
			name.append(string)

	num = 0
	resaults = {}
	for i in name:
		try :
			resaults[i] = value[i]
		except IndexError:
			value = "None"
			resaults[i] = value
		num += 1

	return resaults

			
# Parses throught given html using regex and looks for string matches
def search_html(args, 
		html_content,
		emails, 
		phone_numbers, 
		addresses, 
		auth_tokens, 
		Hashes, 
		access_tokens, 
		api_keys, 
		custom_match,
		):

		regex_search = Regex(html_content, custom_match)

		if args.emails:
			found_emails = regex_search.email()
			for email in found_emails:
				if args.verbose:
					print(f"{fbox} Possible email : {email}")
				ROOT_LOGGER.info(f"Possible email : {email}")
				emails.add(email)

		if args.secrets:
			found_hash = regex_search.hashes()	
			for hash in found_hash:
				if args.verbose:
					print(f"{fbox} Possible password hash : {hash}")
				ROOT_LOGGER.info(f"Possible password hash : {hash}")
				Hashes.add(hash)

			found_api = regex_search.api_keys()
			for api in found_api:
				if args.verbose:
					print(f"{fbox} Possible API Key : {api}")
				ROOT_LOGGER.info(f"Possible API Key : {api}")
				api_keys.add(api)


			found_auth_token = regex_search.auth_token()	
			for auth in found_auth_token:
				if args.verbose:
					print(f"{fbox} Possible authentication token : {auth}")
				ROOT_LOGGER.info(f"Possible authentication token : {auth}")

				auth_tokens.add(auth)

			found_access_token = regex_search.acces_tokens()
			for token in found_access_token:
				if args.verbose:
					print(f"{fbox} Possible access token : {token}")
				ROOT_LOGGER.info(f"Possible access token : {token}")
				access_tokens.add(token)

		if args.phone:
			found_phone_numbers = regex_search.phone_number()
			for number in found_phone_numbers:
				if args.verbose:
					print(f"{fbox} Possible phone number : {number}")
				ROOT_LOGGER.info(f"Possible phone number : {number}")
				phone_numbers.add(number)
		
		if args.address:
			found_addresses = regex_search.addresses()
			for address in found_addresses:
				if args.verbose:
					print(f"{fbox} Possible street address : {address}")
				ROOT_LOGGER.info(f"Possible street address : {address}")
				addresses.add(address)
		
		if args.api:
			found_api = regex_search.api_keys()
			for api in found_addresses:
				if args.verbose:
					print(f"{fbox} Possible API Key : {api}")
				ROOT_LOGGER.info(f"Possible API Key : {api}")
				api_keys.add(api)
		
		if args.access:
			found_access = regex_search.acces_tokens()
			for access in found_access:
				if args.verbose:
					print(f"{fbox} Possible access token : {access}")
				ROOT_LOGGER.info(f"Possible access token : {access}")
				access_tokens.add(access)
		
		if args.auth:
			found_auth = regex_search.auth_token()
			for auth in found_auth:
				if args.verbose:
					print(f"{fbox} Possible authentication token : {auth}")
				ROOT_LOGGER.info(f"Possible authentication token : {auth}")
				auth_tokens.add(auth)
		
		if args.hash:
			found_hash = regex_search.hashes()
			for hash in found_hash:
				if args.verbose:
					print(f"{fbox} Possible password hash token : {hash}")
				ROOT_LOGGER.info(f"Possible password hash token : {hash}")
				Hashes.add(hash)
		
		if args.reg:
			custom_match = regex_search.custom_regex()
			for match in custom_match:
				if args.verbose:
					print(f"{fbox} Possible custom match : {match}")
				ROOT_LOGGER.info(f"Possible custom match : {match}")
				custom_match.add(match)

		if args.all:
			found_addresses = regex_search.addresses()
			for address in found_addresses:
				if args.verbose:
					print(f"{fbox} Possible street address : {address}")
				ROOT_LOGGER.info(f"Possible street address : {address}")

				addresses.add(address)
			
			found_hash = regex_search.hashes()
			for hash in found_hash:
				if args.verbose:
					print(f"{fbox} Possible password hash token : {hash}")
				ROOT_LOGGER.info(f"Possible password hash token : {hash}")
				Hashes.add(hash)
			
			found_auth = regex_search.auth_token()
			for auth in found_auth:
				if args.verbose:
					print(f"{fbox} Possible authentication token : {auth}")
				ROOT_LOGGER.info(f"Possible authentication token : {auth}")
				auth_tokens.add(auth)
			
			found_access = regex_search.acces_tokens()
			for access in found_access:
				if args.verbose:
					print(f"{fbox} Possible access token : {access}")
				ROOT_LOGGER.info(f"Possible access token : {access}")
				access_tokens.add(access)
			
			found_api = regex_search.api_keys()
			for api in found_addresses:
				if args.verbose:
					print(f"{fbox} Possible API Key : {api}")
				ROOT_LOGGER.info(f"Possible API Key : {api}")
				api_keys.add(api)
			
			found_addresses = regex_search.addresses()
			for address in found_addresses:
				if args.verbose:
					print(f"{fbox} Possible street address : {address}")
				ROOT_LOGGER.info(f"Possible street address : {address}")
				addresses.add(address)

			found_phone_numbers = regex_search.phone_number()
			for number in found_phone_numbers:
				if args.verbose:
					print(f"{fbox} Possible phone number : {number}")
				ROOT_LOGGER.info(f"Possible phone number : {number}")
				phone_numbers.add(number)
			
			
			found_emails = regex_search.email()
			for email in found_emails:
				if args.verbose:
					print(f"{fbox} Possible email : {email}")
				ROOT_LOGGER.info(f"Possible email : {email}")
				emails.add(email)

		return 	emails, phone_numbers, addresses, auth_tokens, Hashes, access_tokens, api_keys, custom_match

