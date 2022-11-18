#! /bin/env python3
import re

class Regex:
	
	# Uses regular expressions to search for phone numbers 
	def phone_number(html_content):
		phone_number_regexs = ["[0-9]-[0-9]-[0-9]{7,14}", "[0-9]{2}-[0-9]{3}-[0-9]{4}", "[0-9]{4} [0-9]{3} [0-9]{3}", "[0-9]{3} [0-9]{3} [0-9]{4}", "\([0-9]{3}\) [0-9]{3} [0-9]{4}", "\+[0-9]{2} [0-9]{3} [0-9]{3} [0-9]{3}", "\+[0-9]{1} [0-9]{3} [0-9]{3} [0-9]{4}", "\+[0-9]{1}-[0-9]{3}-[0-9]{3}-[0-9]{4}", ]
		phone_numbers = set()
		# Iterating throught phone_number_regexs and checking for any matches in the given html and adding all found matches to the set
		for regex in phone_number_regexs:
			for re_match in re.finditer(regex, str(html_content)):
				phone_numbers.add(re_match.group())

		return phone_numbers

	# Uses regular expressions to search for email addresses 
	def email(html_content):
		email_regex = r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""
		emails = set()
		
		# Searching the html for emails using the email_regex and addes found resaults to the set
		for re_match in re.finditer(email_regex, str(html_content)):
			emails.add(re_match.group())

		return emails

	# Uses regular expression to search for street addresses
	def addresses(html_content):
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
			for re_match in re.finditer(regex, str(html_content)):
				ADD = True
				for address in addresses:
					if str(re_match) in address:
						ADD = False
						print("already there ")
					else:
						ADD = True
				
				if ADD:
					addresses.add(re_match.group())

		return addresses

	# Uses regular expression to search for api keys
	def api_keys(html_content):
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
		for r in api_regexs:

			for re_match in re.finditer(r, html_content):
				api_keys.add(re_match.group())

		return api_keys

	# Uses regular expression to search for access tokens
	def acces_tokens(html_content):
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
			for re_match in re.finditer(regex, str(html_content)):
				access_tokens.add(re_match.group())
		
		return access_tokens

	# Uses regular expression to search for authentication tokens 
	def auth_token(html_content):
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

			for re_match in re.finditer(regex, str(html_content)):
				auth_tokens.add(re_match.group())

		return auth_tokens
	
	# Uses regular expression to search for password hashes
	def hashes(html_content):
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

			for re_match in re.finditer(regex, str(html_content)):
				hashes.add(re_match.group())

		return hashes

