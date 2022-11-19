# Discription
Icrawl is a web scrapper/spider that uses regex to look for spercific strings in the HTML of the website


# Searches 
* Emails
* Phone numbers
* Street addresses (Note: returns false positives)
* API keys
* Access tokens
* Authenticaion tokens
* Password hashes 
* IP geolocation
* Whois information

Installation
----
    
    pip3 install -r requirements.txt
    
    
Usage
----
  
    python3 Icrawl -u <url> -A -v -c 10 -o output.txt  

# Note
To perform an IP Address geolocation look up an API key is required

# To Do
* Add feature to use Google dorks
* Add more refined regexs for more accurate results
* Add output to CSV 
* Add ASCII art because it's fun
* Add setup.py because doing installs suck
* Add option for multi threaded process
* Update help menu




# Disclaimer
This script was designed to be used for ethical and educational purposes only
