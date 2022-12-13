#! /bin/env python3 

import requests
import os
from bs4 import BeautifulSoup
import lxml 
import logging 
from random import choice


ROOT_LOGGER = logging.getLogger("Icrawl")

# Can be used to set Headers, User-agent and proxy
# Sends the request with all options set 
# returns the request as a beautiful soup object
class sender:
    def __init__(
            self,
            url="",
            timeout=20,
            user_agent="",
            proxy="",
            lang="en-US,en;q=0.5",
            tld="com",
            safe="off",
            tabs=0,
            update=False,
            cookie="",
            burned_proxys=[],
            google=False
            ):
        self = self
        self.url = url
        self.timeout = timeout
        self.user_agent = user_agent
        self.proxy = proxy
        self.lang = lang
        self.tld = tld
        self.safe = safe
        self.tabs = tabs
        self.update = update
        self.cookie = cookie
        self.burned = burned_proxys
        self.google = google


    # Sends a get request and returns a beautifulsoup object
    def get_request(self):
        if self.google:
            pass
        else:
            # Making sure the url isnt empty (not needed but here we are)
            if self.url == "":
                ROOT_LOGGER.critical("No url was supplied")
                return None

            # Asigning the proxy
            if self.proxy != "":
                self.proxy = {"http" : self.proxy,"https": self.proxy,}	
                ROOT_LOGGER.debug(f"Proxy has been set PROXY : {self.proxy}")
            else: 
                ROOT_LOGGER.debug("No proxy hasnt been set")

            # Sending the request
            try:
                responce = requests.get(
                        self.url,
                        headers=self.headers,
                        cookies=self.cookie,
                        proxies=self.proxy,
                        timeout=self.timeout
                    )

            except TimeoutError:
                return None
            except requests.ConnectionError:
                return None
            except Exception as e:
                print(e)
                return None


            soup = BeautifulSoup(responce.text, "lxml")
            return soup

    # Asigns the header for the request and adds it to self
    def get_headers(self):
        self.headers = {
			"Accept"          : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
			"Accept-Encoding" : "gzip, deflate, br",
			"Accept-Language" : self.lang,
			"Connection"      : "keep-alive",			
			"User-Agent"      : self.user_agent,
		}
        # Trying to get a json format responce
        if self.update:
            self.headers = {
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": self.lang,
                "User-Agent": self.user_agent,
                "X-Requested-With": "XMLHttpRequest",
            }

        # Trying to make the google request look like it come from the browser
        if self.google:
            self.headers = {
			"Accept"          : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
			"Accept-Encoding" : "gzip, deflate, br",
			"Accept-Language" : self.lang,
			"Alt-Used"        : "www.google.com",
			"Connection"      : "keep-alive",			
			"User-Agent"      : self.user_agent,
			}

        return self

    # Read proxies.txt file and add all proxies in the file to a list		
    def get_proxy(self):
        proxies = []
        file_path = os.path.abspath(__file__)
        proxy_path = file_path.replace("sendRequest.py", "proxies.txt")

        try:
            with open(proxy_path, "r") as f:
                content = f.readlines()
        except:
            ROOT_LOGGER.critical(f"Wasnt able to locate {proxy_path}")   
            exit(1)

        for line in content:
            if line.strip() != "" and line.strip() not in self.burned:
                proxies.append(line.strip())

        if len(proxies) >= 1:
            self.proxy = choice(proxies)
        else:
            ROOT_LOGGER.debug("No proxys left in the proxy list")
            self.proxy = ""


        return self.proxy

    # Grab a random user agent and add it to self
    def get_user_agent(self):
        try:
            # Getting the files full path
            path = os.path.abspath(__file__)
            user_agent_path = path.replace("sendRequest.py", "user_agents.txt")

            # Adding the content of the file to a list
            with open(user_agent_path) as f:
                content = f.readlines()

            # randomly choose a user agent from the list
            self.user_agent = choice(content)
            self.user_agent = self.user_agent.replace("\n", "").strip()

            # if the user agent came back empty try again
            if self.user_agent == "":
                ROOT_LOGGER.debug(f"User agent come back empty trying again")
                sender.get_user_agent(self)

        except:
            ROOT_LOGGER.critical(f"Wasnt able to locate {user_agent_path}")
            exit(1)


        return self.user_agent

    # Starts a request connection sends the request and parsed the request responce
    # If a cookie is found in the reponce the cookie is asigned to self for the next request
    def google_connection(self):

		# Making a request session
        connection = requests.session()
        connection.headers = self.headers
        ROOT_LOGGER.debug(f"Headers for the request are set Headers : {self.proxy}")
        connection.proxies = self.proxy
        ROOT_LOGGER.debug(f"Proxy for the request are set Proxy : {self.proxy}")
        try:
            if self.cookie != "":
                responce = connection.get(self.url, cookies=self.cookie)
            else:
                responce = connection.get(self.url)
        except TimeoutError:
            return "Timeout"
        except requests.ConnectionError:
            return "Connection error"


        # Making sure the responce code was an okay responce and setting the cookie
        if responce.ok:
            # making the beautiful soup object and loging the status code and url
            ROOT_LOGGER.debug(f"Status code {responce.status_code} URL : {self.url}")
            soup = BeautifulSoup(responce.text, "lxml")
            Cookie = responce.cookies.get_dict()

            # Setting the cookie for the next request
            # If the cookie isnt set after each request 
            # The following request has a higher change of being blocked
            if len(Cookie) > 1:
                cookie_names = dict(Cookie).keys()
                cookie_names = list(cookie_names)
                cookie_name = cookie_names[-1]
                cookie_hash = Cookie[cookie_name]
                self.cookie = {cookie_name : cookie_hash}
                ROOT_LOGGER.debug(f"Cookie has been set COOKIE : {self.cookie}")
            else:
                ROOT_LOGGER.debug("No cookie was found cooke has not been set")

            return soup
        # If responce = a 429 status code we are being blocked by a captcha
        elif responce.status_code == 429:
            ROOT_LOGGER.error(f"Looks like google is blocking Icawl with a captcha")
            return responce.status_code
        # If it wasnt an okay responce return the status code
        else:
            ROOT_LOGGER.error(f"Status code error Staus Code : {responce.status_code}")
            return responce.status_code

