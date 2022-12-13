#! /bin/env python3

from collections import deque
from urllib.parse import urlsplit
import pandas
from colorama import Fore
import logging 
from modules.sendRequest import sender
from modules.htmlParser import  Parser      


ROOT_LOGGER = logging.getLogger("Icrawl")

found_info = set()

# Use sets to make into a dataframe for nicer printing
# Returns a dict with key as URL and value as a dataframe
def make_dataframe(frame_name, emails,phone_numbers, addresses,  auth_tokens,  access_tokens,  hashes, api_keys, custom_matches,):
	dframes = {}
	df = pandas.DataFrame()

		# Emails
	if len(emails) != 0:
		df["Emails"] = pandas.Series(list(emails))
		ROOT_LOGGER.debug(f"Adding {len(emails)} possible emails to datafame")
	
	# Phone numbers
	if len(phone_numbers) != 0:
		df["Phone Numbers"] = pandas.Series(list(phone_numbers))
		ROOT_LOGGER.debug(f"Adding {len(phone_numbers)} possible phone numbers to dataframe")

	
	# Addresses
	if len(addresses) != 0:
		df["Possable Addresses"] = pandas.Series(list(addresses))
		ROOT_LOGGER.debug(f"Adding {len(addresses)} possible street addresses to dataframe")

	# auth tokens
	if len(auth_tokens) != 0: 
		df["Possible Auth Tokens"] = pandas.Series(list(auth_tokens))
		ROOT_LOGGER.debug(f"Adding {len(auth_tokens)} possible auth tokens to dataframe")
	
	# Api keys
	if len(api_keys) != 0: 
		df["Possible Api Keys"] = pandas.Series(list(api_keys))
		ROOT_LOGGER.debug(f"Adding {len(api_keys)} possible API keys to dataframe")

	# Access tokens
	if len(access_tokens) != 0: 
		df["Possible Access Tokens"] = pandas.Series(list(access_tokens))
		ROOT_LOGGER.debug(f"Adding {len(access_tokens)} possible access tokens to dataframe")
		
	# Password hashes
	if len(hashes) != 0: 
		df["Possible Password Hash"] = pandas.Series(list(access_tokens))
		ROOT_LOGGER.debug(f"Adding {len(access_tokens)} possible password hash to dataframe")
		
	# Custom regex
	if len(custom_matches) != 0: 
		df["Custom Resaults"] = pandas.Series(list(custom_matches))
		ROOT_LOGGER.debug(f"Adding {len(custom_matches)} possible custom matches to dataframe")

	# Adding dataframe to dict of with the frame name as the key 
	if len(df) > 0:
		ROOT_LOGGER.debug(f"Final number of dataframe elements : {len(df)}")
		df = df.fillna("")
				
		dframes[frame_name] = df
		return dframes

	else:	
		ROOT_LOGGER.error("No infomation was added to the dataframe")
		return None
	
	
def crawler(args, spider):
    scraped_url = set()

    # Colors		
    yellow = Fore.YELLOW
    blue = Fore.BLUE
    red = Fore.RED
    green = Fore.GREEN
    norm = Fore.RESET

	# Boxes
    ibox = f"{yellow}[+]{norm}"
    fbox = f"{green}[+]{norm}"
    error = f"{red}[!]{norm}"
    returned_resaults = []

	# Breaking up the given url into 3 parts scheme=https:// netloc=domainName path=subDirectorys
    unscraped_url = deque([args.url])
    parts = urlsplit(args.url)
    base_url = f"{parts.scheme}://{parts.netloc}"
    ROOT_LOGGER.debug(f"crawler has started")
    ROOT_LOGGER.debug(f"Base url URL : {base_url}")

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
			
            request = sender(URL)
            request.get_user_agent()
            ROOT_LOGGER.debug(f"User agent set User-Agent : {request.user_agent}")
            request.get_headers()
            ROOT_LOGGER.debug(f"Headers set Headers : {request.headers}")
            request.get_proxy()
            ROOT_LOGGER.debug(f"Proxy set Proxy : {request.proxy}")
            soup = request.get_request()
	    
            # No html was returned so continue onto the next url
            if soup == None:
                ROOT_LOGGER.error(f"No HTML was returned from the request URL : {URL}")
                continue

            if spider:
                ROOT_LOGGER.debug(f"Spidering  URL : {URL}")
                # Searching the html for regex matches
                p = Parser(
                        html_content=soup,
                        phone_numbers=args.phone,
                        emails=args.emails,
                        hashes=args.hash,
                        auth=args.auth,
                        api=args.api,
                        addresses=args.address, 
                        access_tokens=args.access, 
                        custom_match=args.reg,
                        links=True,
                        scraped_url=scraped_url,
                        unscraped=unscraped_url,
                        base_url=base_url,
                        all=args.all,
                    )
                regex_resaults = p.parse_html()
                # Getting all the new links found in the html and adding them to the unscraped list
                unscraped_url = regex_resaults["links"]
                ROOT_LOGGER.debug(f"Regex resaults emails={len(regex_resaults['emails'])} phone_numbers={len(regex_resaults['phone'])} addresses={len(regex_resaults['addresses'])} hashes={len(regex_resaults['hash'])} access_tokens={len(regex_resaults['tokens'])} api_keys={len(regex_resaults['api'])} auth_tokens={len(regex_resaults['auth'])} custom_matches={len(regex_resaults['custom'])}")
                ROOT_LOGGER.debug(f"Number of links left to scrape {len(unscraped_url) - len(scraped_url)}")
            else:
                # Searching the html for regex matches
                p = Parser(
                        html_content=soup,
                        phone_numbers=args.phone,
                        emails=args.emails,
                        hashes=args.hash,
                        auth=args.auth,
                        api=args.api,
                        addresses=args.address, 
                        access_tokens=args.access, 
                        custom_match=args.reg,
                        all=args.all,

                    )
                regex_resaults = p.parse_html()
                ROOT_LOGGER.debug(f"Regex resaults emails={len(regex_resaults['emails'])} phone_numbers={len(regex_resaults['phone'])} addresses={len(regex_resaults['addresses'])} hashes={len(regex_resaults['hash'])} access_tokens={len(regex_resaults['tokens'])} api_keys={len(regex_resaults['api'])} auth_tokens={len(regex_resaults['auth'])} custom_matches={len(regex_resaults['custom'])}")

	    
            dframes = make_dataframe(frame_name=URL, emails=regex_resaults["emails"],phone_numbers=regex_resaults["phone"],addresses=regex_resaults["addresses"],access_tokens=regex_resaults["tokens"],hashes=regex_resaults["hash"],api_keys=regex_resaults["api"],custom_matches=regex_resaults["custom"],auth_tokens=regex_resaults["auth"])
			
            if dframes == None:	
                ROOT_LOGGER.debug("Dataframe came back empty moving on to next url")
                continue
            
            if args.verbose:    
              for key in dframes:
                    print(f"{fbox} {blue}{key}{norm}")
                    print(dframes[key])

			
            returned_resaults.append(dframes)

    except KeyboardInterrupt:
        ROOT_LOGGER.debug("Keyboard interrupt stopping crawler")
        print(f"{error} Keyboard interrupt stopping crawler")
        return returned_resaults, list(scraped_url)

    return returned_resaults ,list(scraped_url)


