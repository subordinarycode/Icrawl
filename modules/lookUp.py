#! /bin/env python3
import ipinfo
import whois
from colorama import Fore
from modules.sendRequest import sender
import logging 
import re 


ROOT_LOGGER = logging.getLogger("Icrawl")


cyan = Fore.CYAN
white = Fore.RESET
green = Fore.GREEN
red = Fore.RED

box = f"{green}[+]{white}"
error = f"{red}[!]{white}"

# access token for ipinfo.io
access_token = '<access token>'
# Proforms an ip geolocation look up using ipinfo.io
def ip_lookup(ip_address=None):
	try:
		# Create a client object with the access token
		handler = ipinfo.getHandler(access_token)
		# Receve details about ip address as a dict
		details = handler.getDetails(ip_address, None)

		return details.all.items()
	except:
		return []

# Checks if the given domain is registered or not 
def is_registered(domain_name):
	try:
		w = whois.whois(domain_name)
	except Exception as e:
		return False
	else:
		return bool(w.domain_name)

# Proforms a whois look up a domain
def domain_infomation(domain_name):
	if  is_registered(domain_name):
		whois_info = whois.whois(domain_name)
		domain_info = []
		# Is registered
		domain_info.append(f"{box} {cyan}Registrar:{white} {whois_info.registrar}")
		# WHOIS server
		domain_info.append(f"{box} {cyan}WHOIS server:{white}{whois_info.whois_server}")
		# Dns security
		domain_info.append(f"{box} {cyan}Dns security: {white}{whois_info.dnssec}")
		# Organization
		domain_info.append(f"{box} {cyan}Organization: {white}{whois_info.org}")
		# Emails
		domain_info.append(f"{box} {cyan}Emails:{white}{whois_info.emails}")
			
		# Updated date
		update_date =  str(whois_info.updated_date)
			
		update_date = update_date.split("-")
		if len(update_date) >= 3:
			UpdateDate = f"{update_date[1]}-{update_date[2]}-{update_date[0]}"
		else:
			UpdateDate = ""

				
		domain_info.append(f"{box} {cyan}Updated date: {white}{UpdateDate}")


		# Get the creation time
		Creation_Date = str(whois_info.creation_date)

		Creation_Date = Creation_Date.replace("[datetime.datetime(", "")
		Creation_Date = Creation_Date.split(",")
		if len(Creation_Date) >= 3:
			CreationDate = f"{Creation_Date[1].strip()}-{Creation_Date[2].strip()}-{Creation_Date[0].strip()}"
		else:
			CreationDate = ""
				
		domain_info.append(f"{box} {cyan}Creation date: {white}{CreationDate}")


			# Get expiration date
		Experation_Date = str(whois_info.expiration_date)

		Experation_Date = Experation_Date.replace("[datetime.datetime(", "")
		Experation_Date = Experation_Date.replace("[datetime.datetime(", "")
		Experation_Date = Experation_Date.replace(")]", "")
		Experation_Date = Experation_Date.split(",")
		if len(Experation_Date) >= 3:
			ExperationDate = f"{Experation_Date[1].strip()}-{Experation_Date[2].strip()}-{Experation_Date[0].strip()}"
		else:
			ExperationDate = ""
		domain_info.append(f"{box} {cyan}Expiration date: {white}{ExperationDate}")


		# Country 
		domain_info.append(f"{box} {cyan}Country: {white}{whois_info.country}")
		# State
		domain_info.append(f"{box} {cyan}State: {white}{whois_info.state}")
		# Address 
		domain_info.append(f"{box} {cyan}Address:{white}{whois_info.address}")
		# Postal code
		domain_info.append(f"{box} {cyan}Postal code: {white}{whois_info.registrant_postal_code}")
			
	
		return domain_info

# Takes in an ip address and send a request to shodan.io
# Reads the HTML of the page and extracts all the usefull information
# Returns general info as a dict and port details as a dict
def shodan_lookup(ip,):

    url = f"https://www.shodan.io/host/{ip}"
	
    request = sender()
    request.get_user_agent()
    request.get_headers()
    request.get_proxy
    request.url = url
    soup = request.get_request()
    if soup == None:
        return {f"{error}Error" : "Request timeout"},{f"{error}Error" : "Request timeout"}

	# Grabbing all the "Genereral information" from the shodan search
    general_info = {}
    for tag in soup.find_all("a", href=True):
        if str(tag["href"]).startswith("/search"):
            for match in re.finditer("/search\?query=.*?%3A%", tag["href"]):
                info_name = str(match.group()).replace("%3A%", "").replace("/search?query=", "")
				
            for match in re.finditer("%3A%22.*?%", tag["href"]):
                info_details = str(match.group()).replace("%3A%22", "")[:-1]
				
            if info_name not in general_info:
                general_info[info_name] = info_details


    # Grabbing the resaults from the port scan that shodan proforms				
    port_details = {}		
    for tag in soup.find_all("pre"):
        if not '<pre clas' in str(tag):
            full_details = tag.contents[0].split(":", 1)
            name = full_details[0]
            details = full_details[1]
            port_details[name] = details


        
    if len(general_info) == 0 and len(port_details) == 0:
        ROOT_LOGGER.error(f"Wasnt able to find any resaults for IP : {ip}")
    else:
        ROOT_LOGGER.error(f"Returning {len(general_info)} general info details and {len(port_details)} port details")

    return general_info, port_details

