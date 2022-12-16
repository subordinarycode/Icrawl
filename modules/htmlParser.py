#! /bin/env python3 

import re 
from bs4 import BeautifulSoup
import lxml

# To-Do
# Add verbose output 
# Add logging 
# 


class Parser:

    def __init__(self,
        html_content,
        phone_numbers=False,
        emails=False,
        hashes=False,
        auth=False,
        api=False,
        addresses=False, 
		access_tokens=False, 
		custom_match=[],
        links=False,
        scraped_url=[],
        base_url="",
        unscraped=[],
        google=False,
        all=False,
        ):
        self.html_content = html_content
        self.phone_numbers = phone_numbers
        self.emails = emails
        self.hash = hashes
        self.auth = auth
        self.api = api
        self.addresses = addresses 
        self.access_tokens = access_tokens 
        self.custom_match = custom_match
        self.links = links
        self.scraped = scraped_url
        self.base_url = base_url
        self.unscraped = unscraped
        self.google = google
        self.all = all


    def parse_html(self):
        resaults = {}

        if self.phone_numbers or self.all:
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

            resaults["phone"] = list(phone_numbers)
        else:
            resaults["phone"] = []

        if self.emails or self.all:
            email_regex = r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""
            emails = set()
            for re_match in re.finditer(email_regex, str(self.html_content)):
                emails.add(re_match.group())

            resaults["emails"] = list(emails)
        else:
            resaults["emails"] = []

	    # Uses regular expression to search for street addresses
        if self.addresses or self.all:
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

                        if ADD:
                            addresses.add(re_match.group())

            resaults["addresses"] = list(addresses)
        else:
            resaults["addresses"] = []

	    # Uses regular expression to search for api keys
        if self.api or self.all:
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
                for re_match in re.finditer(regex, str(self.html_content)):
                    api_keys.add(re_match.group())

            resaults["api"] = list(api_keys)
        else:
            resaults["api"] = []

	    # Uses regular expression to search for access tokens
        if self.access_tokens or self.all:
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
		
            resaults["tokens"] = list(access_tokens)
        else:
            resaults["tokens"] = []
	
        # Uses regular expression to search for authentication tokens 
        if self.auth or self.all:
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

            resaults["auth"] = list(auth_tokens)
        else:
            resaults["auth"] = []

	    # Uses regular expression to search for password hashes
        if self.hash or self.all:
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

            resaults["hash"] = list(hashes)
        else:
            resaults["hash"] = []

	    # Use custom regular expressions to find pattern matches
        if self.custom_match != []:
            custom_matches = set()
		# Iterating throught custom_regexs and checking for any matches in the given html and adding all found matches to the set
            for regex in self.custom_regexs:
                for re_match in re.finditer(regex, str(self.html_content)):
                    custom_matches.add(re_match.group())

            resaults["custom"] = list(custom_matches)
        else:
            resaults["custom"] = []

	    # Use BeautifulSoup to extract all the hrefs links from the html
        # If looking for links in the html of a google seach 
        # filter out the google links so only the search resault links are returned 
        if self.links:
            if self.google:
                found_links = set()
                bad_links = [
                        "https://support.google.com","https://policies.google.com", "https://translate.google.com",
			            "https://m.facebook.com","https://ads.google.com","https://shopping.google.com", "https://marketingplatform.google.com",
			            "https://maps.google.com", "https://www.google.nl/maps","https://ads.google.com", "https://news.google.nl"
                        ]
                for link in self.html_content.find_all('a', href=True):
			
                    if str(link["href"]).startswith("http"):
                        ADD = True
                        for blink in bad_links:
                            if str(link["href"]).startswith(blink) or str(link["href"]) in found_links:
                                ADD = False
				
                        if ADD:
                            found_links.add(link["href"])
                
                resaults["links"] = list(found_links)

            else:
                for tag in self.html_content.find_all("a", href=True):
                    if self.base_url in tag["href"] and tag["href"] not in self.scraped and tag["href"] not in self.unscraped:
                        self.unscraped.append(tag["href"])

                resaults["links"] = self.unscraped
        else:
            resaults["links"] = []


        return resaults

		

