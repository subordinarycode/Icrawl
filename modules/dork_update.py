#! /bin/env python3
import logging 
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm 
import lxml



ROOT_LOGGER = logging.getLogger("Icrawl")

def update_google_dorks():
	url = ["https://www.exploit-db.com/google-hacking-database"]

	headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.5",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0",
            "X-Requested-With": "XMLHttpRequest",
    }
	
	try:
		print(f"[+] Sending requests to : {url[0]}")
		ROOT_LOGGER.info(f"Sending request to URL : {url}")
		for req in tqdm(url):			
			response = requests.get(req, headers=headers)
	
	except:
		ROOT_LOGGER.error(f"Request failed URL : {req}")
		print(f"[!] Error : {req} wasnt reachable")
		return None
	
	if response.status_code != 200: 
		ROOT_LOGGER.error(f"Status code error Status URL : {url} Staus Code : {response.status_code}")       
		return None

	
	
	Json = response.json()

    # Getting the number of dorks and the google dork
	num_of_dorks = Json["recordsTotal"]
	dorks = Json["data"]

    # List to track found dorks 
	found_dorks = []

    # Dict to organize the dorks
	sorted_dorks = {}

	# Search the html of the page for the dork catorgory and name
	print("\n[+] Grabbing latest google dorks")
	for dork in tqdm(dorks):

		soup = BeautifulSoup(dork["url_title"], "lxml")    		
		found_dork = soup.find("a").contents[0].strip()
		found_dorks.append(found_dork)

		# Making a dict with the key as a number for easyer sorting later
		num_id = int(dork["category"]["cat_id"])
		name = dork["category"]["cat_title"]

        # Adding catorgory name and an empty list to the sorted_dorks dict
		if num_id not in sorted_dorks:
			sorted_dorks[num_id] = {"category_name": name, "dorks": []}

		# Adding the dork to the list associated with its number id 
		dork["url_title"] = dork["url_title"].replace("\t", "")
		sorted_dorks[num_id]["dorks"].append(dork)


	# Sorting all the found dorks by there number id
	sorted_dorks = dict(sorted(sorted_dorks.items()))

	# Wrighting all the found dorks to a file with the category name
	print("\n[+] Saving latest google dorks")
	for key, value in tqdm(sorted_dorks.items()):

		dork_file = value["category_name"].lower().replace(" ", "_")
		dork_path = f"modules/dorks/{dork_file}.dorks"


		with open(dork_path, "w", encoding="utf-8") as f:
			for dork in value["dorks"]:
				soup = BeautifulSoup(dork["url_title"], "html.parser")
				new_dork = soup.find("a").contents[0].strip()
				f.write(f"{new_dork}\n")


	return num_of_dorks



