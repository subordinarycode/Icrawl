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
  
    python3 Icrawl -w <url> -A -v -c 10 -o output.txt  

# Note
To perform an IP Address geolocation look up an API key is required

# Disclaimer
This script was designed to be used for ethical hacking and educational purposes only
