# Discription
Icrawl is an OSINT web scraping and spidering tool that can use regular expressions 
to look for specific strings in the HTML of the website, As well as a feature to use google 
dorking to return the URLs from the google search and an option to crawl the returned links
and display any matching results.


Searches 
---
* Emails
* Phone numbers
* Street addresses (Note: returns false positives)
* API keys
* Access tokens
* Authentication tokens
* Password hashes 
* IP geolocation
* Whois information
* Google dorks


Installation
----
    
    pip3 install -r requirements.txt
    
    
Usage
----
  
    python3 Icrawl -u <url> -A -c 10


Proxie info
---
To use a list of proxies with Icrawl add your list of proxies to the modules/proxys.txt file.
At run time, Icrawl will read the file and load all the proxies from the file into a list 
of proxies to use during run time. 

If during run time a proxy returns a 429 status code, the proxy is considered burned and then 
removed from the list of proxies. Icrawl will return all the results found before the 429 status
code was given. Then grab a new proxy from the list and continue.

Proxie format example: socks5://127.0.0.1:9050


Google dork info
---
To add your own list of custom google dorks create a file with all the google dorks you want to use 
and add the file to the modules/docks/ directory. At run time, Icrawl will load the files in this 
directory in as options for the payload to use.

By default, Icrawl goes out to https://www.exploit-db.com/google-hacking-database and downloads 
all the latest google dorks and saves them in the modules/dorks directory.




Acknowledgments
---
While I didn't just copy and paste. Whenever i'd run into a problem while writing the googlesearch.py file I
would go to https://github.com/opsdisk/yagooglesearch as they have some good documentation for that project 
and the comments in the code made it really easy to understand what was going on. 

They have done an awesome job on this project, and I would recommend that you give it a look over




Notes
---
To perform an IP Address geolocation, lookup a API key is required

By default, the delay between requests for google dorks is 10 seconds. In testing 
I was able to drop this down to about 5 seconds and I would get about 50 different
requests off requesting for multiple pages from google before needing to complete a 
Captcha. The longer the delay between requests, the less likely you are to come across a 
Captcha



To Do
---
* Add more refined regexs for more accurate results
* Add output to CSV 
* Add setup.py because doing installs suck
* Add a way to scrape social media sites i.e., Twitter, Facebook
* Add an option to turn logging on/off



Disclaimer
---
This script was designed to be used for ethical and educational purposes only
