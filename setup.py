#! /bin/env python3

import os 


def main():
	print("[+] Please enter your access token for ipinfo.io")
	api_key = input("[+] Press enter to skip: ")
	if api_key != "":
		path = __file__
		lookup_path = path.replace("setup.py", "modules/lookUp.py")

		with open(lookup_path) as f:
			content = f.readlines()

		content[21] = f"access_token = '{api_key}'\n"

		with open(lookup_path, "w") as f:
			for line in content:
				f.write(line)

	print("[+] Do you want to add a proxy to the proxies.txt file?")
	proxy = input("[+] Press enter to skip: ")
	if proxy != "":
		if " " in proxy:
			proxies = proxy.split()
			path = __file__
			proxy_path = path.replace("setup.py", "modules/proxies.txt")
			with open(proxy_path, "w") as f:
				for proxy in proxies:
					f.write(f"{proxy.strip()}\n")

		else:
			path = __file__
			proxy_path = path.replace("setup.py", "modules/proxies.txt")
			with open(proxy_path, "w") as f:
					f.write(f"{proxy.strip()}\n")
				
	print("[+] Installing requirements")
	print("[+] This may take a couple of seconds")
	os.system("pip3 install -r requirements.txt")
	print("[+] Updating google dorks")
	print("[+] This may take a couple of seconds")
	os.system("python3 Icrawl --update")
	print("[+] Setup complete")
	print("Goodbye")
	
	


if __name__ == '__main__':
	main()
