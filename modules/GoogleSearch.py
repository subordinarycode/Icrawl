#! /bin/env python3



import requests 
from bs4 import BeautifulSoup
import time 
from random import choice 
import lxml
import logging 
from colorama import Fore

ROOT_LOGGER = logging.getLogger("Icrawl")
#logging.basicConfig(filename="Icrawl.log", level=5)

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


class googleSearch:

	def __init__(
			self, 
			user_agent="", 
			proxy="", 
			timeout_between_requests=10, 
			timeout_between_new_page=10, 
			num_of_links_to_return=10, 
			timeout=15,
			):
		
		self = self
		self.queary = ""
		self.user_agent = user_agent
		self.proxy = proxy
		self.timeout_between_requests = timeout_between_requests
		self.timeout_between_new_page = timeout_between_new_page
		self.num_of_links_to_return = num_of_links_to_return
		self.lan = "en-US,en;q=0.5"
		self.timeout = timeout
		self.cookie_set = False
		self.lang = "en"
		self.country = ""
		self.tld = "com"
		self.num = 100
		self.safe = "off"
		self.tbs = "0"

		
	# Send search request to google
	# Exctracts all the links in the HTML from the request and add them to a set so theres no doubles
	# Returns the links found as a list
	def start_google_connection(self):
		if self.queary == "":
			ROOT_LOGGER.critical("Query was empty")
			return []
		
		# Asigning the proxy
		if self.proxy != "":
			self.Proxy = {"http" : self.proxy,"https": self.proxy,}	
			ROOT_LOGGER.debug(f"Proxy has been set PROXY : {self.Proxy}")
		else: 
			ROOT_LOGGER.debug("No proxy hasnt been set")
			self.Proxy = ""

		# Google inital search url
		url = f"https://www.google.com/search?q={self.queary}"#"https://toscrape.com/"
		found_links = set()

		# If a cookie has been set use the cookie in the request
		if self.cookie_set:	
			# Asigning the headers to the request			
			header = {
			"Accept"          : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
			"Accept-Encoding" : "gzip, deflate, br",
			"Accept-Language" : self.lan,
			"Alt-Used"        : "www.google.com",
			"Connection"      : "keep-alive",			
			"User-Agent"      : self.user_agent,
			}
			ROOT_LOGGER.debug(f"Headers for the request are set HEADERS : {header}")
			# Making a request session
			connection = requests.session()
			connection.headers = header
			connection.proxies = self.Proxy
			ROOT_LOGGER.debug(f"Proxy for the request are set PROXY : {self.Proxy}")
			responce = connection.get(url, cookies=self.cookie, timeout=self.timeout)
			
			# Making sure the responce code was an okay responce
			if googleSearch.check_responce(self, responce):
				ROOT_LOGGER.debug(f"Status code {responce.status_code} URL : {url}")
				self.soup = BeautifulSoup(responce.text, "lxml")
				links = googleSearch.get_links(self)
				ROOT_LOGGER.debug(f"Number of links returned {len(links)}")
				for link in links:
					found_links.add(link)
				ROOT_LOGGER.debug(f"Number of links returned {len(links)}")
				
				# Adding as many links to the set as the user specifed 
				# If less then 10 then google couldnt find more then that on the inital request
				# Or my parsing sucks one of the two
				while len(links) >= 10:
					ROOT_LOGGER.debug(f"Grabbing more links for query QUERY : {self.queary}")
					# Search requesting for number of urls to recive i.e 100
					url = (
						f"https://www.google.{self.tld}/search?hl={self.lang}&"
						f"q={self.queary}&num={self.num}&btnG=Google+Search&tbs={self.tbs}&"
						f"safe={self.safe}&cr={self.country}&filter=0"
					)
					ROOT_LOGGER.debug(f"New Url for query URL : {url}")
					# Trying to make it look "normal"
					ROOT_LOGGER.debug(f"Sleeping for {self.timeout_between_new_page} Before going to next page")
					time.sleep(self.timeout_between_new_page)
					responce = connection.get(url, cookies=self.cookie, timeout=self.timeout)
					
					if googleSearch.check_responce(self, responce):
						ROOT_LOGGER.debug(f"Status code {responce.status_code} URL : {url}")
						self.soup = BeautifulSoup(responce.text, "lxml")
						links = googleSearch.get_links(self)
						ROOT_LOGGER.debug(f"Number of links returned {len(links)}")
						if len(links) > self.num_of_links_to_return:
							for i in links:
								if len(found_links) < self.num_of_links_to_return:
									found_links.add(i)
							
							if len(links) == self.num_of_links_to_return:
								ROOT_LOGGER.debug(f"{len(links)} out of {len(self.num_of_links_to_return)} Have been found returning")
								break
							else:
								if len(links) < self.num:
									ROOT_LOGGER.error(f"Not enough resaults to return {self.num_of_links_to_return} urls")
									break

								self.num = self.num + 100	
								

						elif len(links) < self.num_of_links_to_return:		
							for i in links:
								found_links.add(i)
							ROOT_LOGGER.error(f"Only {len(links)} out of {self.num_of_links_to_return} where found")
							break

					else:
						if responce.status_code == 429:
							found_links.add("Blocked ip")
						break
			else:
				if responce.status_code == 429:
					found_links.add("Blocked ip")
					return list(found_links)
				
		# The first request send before cookies are assigned
		else:
			ROOT_LOGGER.warning(f"No cookie has been asigned on request for URL : {url}")
			header = {
				"Accept"          : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
				"Accept-Encoding" : "gzip, deflate, br",
				"Accept-Language" :  self.lan,
				"Alt-Used"        : "www.google.com",
				"Connection"      : "keep-alive",
				"User-Agent"      : self.user_agent,
			}
			ROOT_LOGGER.debug(f"Headers for the request are set HEADERS : {header}")
			connection = requests.session()
			connection.headers = header
			connection.proxies = self.Proxy
			ROOT_LOGGER.debug(f"Proxy for the request are set PROXY : {self.Proxy}")
			responce = connection.get(url, timeout=self.timeout)

			if googleSearch.check_responce(self, responce):
				ROOT_LOGGER.debug(f"Status code {responce.status_code} URL : {url}")
				self.soup = BeautifulSoup(responce.text, "lxml")
				links = googleSearch.get_links(self)
				ROOT_LOGGER.debug(f"Number of links returned {len(links)}")
				for link in links:
					found_links.add(link)
				ROOT_LOGGER.debug(f"Current number of new links : {len(links)}")
			else:
				ROOT_LOGGER.critical("Inital request did not return with okay status")
				if responce.status_code == 429:
					found_links.add("Blocked ip")
					return list(found_links)

		
		return list(found_links)


	# Grab a random user agent and add it to self
	def get_user_agent(self):
		try:
			path = __file__
			user_agent_path = path.replace("GoogleSearch.py", "user_agents.txt")
		
			with open(user_agent_path) as f:
				content = f.readlines()
			
			self.user_agent = choice(content)
			if self.user_agent.strip() == "":
				googleSearch.get_user_agent(self)
			
			ROOT_LOGGER.info(f"User agent has been set USER-AGENT : {self.user_agent}")
			self.user_agent = self.user_agent.replace("\n", "")
		except:
			ROOT_LOGGER.critical(f"Wasnt able to locate {path}")
			exit()		
	
		ROOT_LOGGER.info(f"User agent set USER AGENT : {self.user_agent}")
		return self.user_agent
	

	# Parses through all the html from the google search
	# If the href link contains http and no other "bad links" adds the link to a set so theres no doubles
	# Returns the set
	def get_links(self):
		found_links = set()
		bad_links = ["https://support.google","https://policies.google", "https://www.google.com", "https://translate.google.com",
			"https://m.facebook.com","https://ads.google.com","https://shopping.google", "https://marketingplatform.google.com",
			"https://maps.google.com", "https://www.google.nl/maps","https://ads.google.com", "https://news.google.nl"]
		for link in self.soup.find_all('a', href=True):
			
			if str(link["href"]).startswith("http"):
				ADD = True
				for blink in bad_links:
					if str(link["href"]).startswith(blink):
						ADD = False
				
				if ADD:
					found_links.add(link["href"])
		
		return found_links


	# Checks the responce code from the request 
	# On the inital google search it will asign the cookie from the search to self
	# If a 429 responce is given the user is prompted to compete the capcha with the current assigned cookie
	def check_responce(self, responce):
		# Checking is responce code is okay and setting cookies
		if responce.ok:
			Cookie = responce.cookies.get_dict()
			ROOT_LOGGER.debug(f"Request returned Status code : {responce.status_code}")
			if len(Cookie) > 1:
				cookie_names = dict(Cookie).keys()
				cookie_names = list(cookie_names)
				self.cookie_name = cookie_names[-1]
				self.cookie_hash = Cookie[self.cookie_name]
				self.cookie = {self.cookie_name : self.cookie_hash}
				ROOT_LOGGER.debug(f"Cookie has been set COOKIE : {self.cookie}")
				self.cookie_set = True
			return True
		
		if responce.status_code == 429:
			try:
				ROOT_LOGGER.critical(f"Oops it looks like your IP has been blocked by google Status code : {responce.status_code}\n")
				ROOT_LOGGER.info(f"Status code 429 a captca is avaliab at URL : {responce.url}\n\n")				
				if self.cookie_set:
					print(f"{error} Oops looks like we are being blocked by a capcha")
					print(f"{ibox} A captca is avaliab at URL : {responce.url}\n\n")
					print(f"{ibox} Use this cookie and navigate to the url and complete the capcha")				
					print(f"\n{ibox} Cookie: {self.cookie_name}={self.cookie_hash}\n")		
					input(f"{ibox} Press Enter to coninue \n{ibox} Press CTRL-C to return with the current list: ")
					googleSearch.start_google_connection(self)

				return False
			except KeyboardInterrupt:
				ROOT_LOGGER.error(f"Keyboard Interrupt returning current list")
				ROOT_LOGGER.info(f"Returned current list after Status code : {responce.status_code}\n")
				return False

		else:
			ROOT_LOGGER.error(f"unexpected responce {responce.status_code}")
			return False

			



######################### For testing #########################
	
#test = googleSearch()
#test.get_user_agent()

#with open ("dorks/files_containing_passwords.dorks") as f:
#	content = f.readlines()

#for dork in content:
#	test.queary = dork
#	x = test.start_google_connection()
#	try:
#		for i in x:
#			print(i)
#	except ValueError:
#		pass




