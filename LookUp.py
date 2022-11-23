#! /bin/env python3
import ipinfo
import whois
from colorama import Fore

cyan = Fore.CYAN
white = Fore.RESET
green = Fore.GREEN

box = f"{green}[+]{white}"

# access token for ipinfo.io
access_token = '<access token>'

class Lookup:
	global is_registered

	def ip_lookup(ip_address=None):
		try:
			# Create a client object with the access token
			handler = ipinfo.getHandler(access_token)
			# Receve details about ip address as a dict
			details = handler.getDetails(ip_address, None)

			return details.all.items()
		except:
			return []

	def is_registered(domain_name):
		try:
			w = whois.whois(domain_name)
		except Exception as e:
			return False
		else:
			return bool(w.domain_name)


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




