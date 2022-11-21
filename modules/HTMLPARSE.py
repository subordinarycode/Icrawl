#! /bin/env python3
import requests
from bs4 import BeautifulSoup
import lxml
import re

class Parser:
	# Gets the HTML code of a given url
	def get_source(url):
		try:
			# Sending get request to given url
			get_request = requests.get(url)
		except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError, requests.exceptions.InvalidURL):
			return None

		# If the status code wasnt a 200 responce then there will be no interesting data in the html so just return
		if int(get_request.status_code) != 200:
			return None

		
		# Using BeautifulSoup  to parse to html of the page
		soup = BeautifulSoup(get_request.text, "lxml")
		return soup

	# Uses regex to find all the href links in given HTML
	def get_links(html_content, base_url, unscraped_url, scraped_url):
		try:
			html_content = BeautifulSoup(html_content, "lxml")
		except TypeError:
			return unscraped_url
		for _ in html_content:
			link_regex = ['href="https://.*?"','href="/.*?"','href="http://.*?"']
			for regex in link_regex:
				for re_match in re.finditer(regex, str(html_content)):
					weblink = re_match.group()
					
					# Cleaning up new link
					weblink = weblink.replace('href="', '')
					weblink = weblink.replace('"', '')
					
					# Making a new url with found links
					if weblink.startswith('/'):
						weblink = base_url + weblink
					elif not weblink.startswith('https'):
						weblink = weblink

					
					# Checking if link has been scraped before if not adding it to the list
					if weblink not in unscraped_url and weblink not in scraped_url:
						if base_url in weblink:
							unscraped_url.append(weblink)
						
		return unscraped_url
