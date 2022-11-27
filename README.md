# Discription
Icrawl is an OSINT Information gathering, web scraping, and spidering tool that can use regular expressions 
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
* IP geolocation lookup
* Whois information lookup
* Shodan lookup
* Google dorks


Installation
----
    
    python3 setup.py
    
    
Usage
----
  
    python3 Icrawl -u <url> -A -c 10


Proxy info
---
To use a list of proxies with Icrawl add your list of proxies to the modules/proxies.txt file.
At run time, Icrawl will read the file and load all the proxies from the file into a list. If 
during run time a proxy returns a 429 status code, the proxy is considered burned and then 
added to a list of burned proxies. Icrawl will return all the results found before the 429 status
code was given. Then grab a new proxie from the list and continue.

Proxie format example: socks5://127.0.0.1:9050
.


Google dork info
---
To add your own list of custom google dorks create a file with all the google dorks you want to use 
and add the file to the modules/docks/ directory. At run time, Icrawl will load the files in this 
directory in as options for the payload to use.

By default, Icrawl goes out to https://www.exploit-db.com/google-hacking-database and downloads 
all the latest google dorks and saves them in the modules/dorks directory.



Notes
---
To perform an IP Address geolocation, lookup a API key is required

By default, the delay between requests for google dorks is 10 seconds. In testing 
I was able to drop this down to about 5 seconds but when running google dorks with such
a short delay period you are more likely to be blocked by a captcha. Icrawl tries it mitigate
this by asigning a cookie to every request sent but it can still resault in being blocked by a captcha.
For the best resaults i recommend sticking between 7-12 seconds between requests

To Do
---
* Add more refined regexs for more accurate results
* Add output to CSV 
* Add setup.py because doing installs suck
* Add a way to scrape social media sites i.e., Twitter




Acknowledgments
---
While I didn't just copy and paste. Whenever i'd run into a problem while writing the sendRequest.py file and the
updater.py file I would go to https://github.com/opsdisk/ as they have some good documentation for there projects 
and the comments in there code make it really easy to understand what is going on. 

They have some awesome projects and i would recommend you give it a look over.


Known bugs
---
There is a bug when adding a custom goole dork file to the modules/dorks directory
because Icrawl reads and displays these files two files at a time unless you add two new files 
there is a chance the file you added wont be displayed in the payload setup.

This is something I am actively looking for a solution to but for the meantime if you add a new custom dork file 
to to modules./dorks directory and it doesnt appear in the payload setup just add an extra blank file to the modules/dorks directory
and everything should show up when setting up the paylaod

Disclaimer
---
This script was designed to be used for ethical and educational purposes only
