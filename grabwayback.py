try:
	import sys
	import os
	import time
	import json
	import requests
	from termcolor import colored

except ModuleNotFoundError:
	print("""Make sure you have the following module installed!
		\n 1. requests [ pip3 install requests ]
		\n 2. termcolor [ pip3 install termcolor ]""")
	sys.exit()


def grab_urls(url):
	try:
		r = requests.get(f"https://web.archive.org/cdx/search/cdx?url=*.{url}&output=json&fl=original&collapse=urlkey")

		json_content = r.json()

		if len(json_content) !=0:
			json_content.pop(0)

			total_links = 0
			links_with_param = 0
			total_domains = []

			for links in json_content:
				links = str(links)
				starting_link = links[2:]
				ending_link = starting_link.index("]")
				main_link = links[2:ending_link+1]
				total_links += 1
				with open("links.txt", "a") as link_file:
						link_file.write(main_link)
						link_file.write("\n")
				
				if "?" in main_link:
					links_with_param += 1
					with open("links_with_param.txt", "a") as param_file:
						param_file.write(main_link)
						param_file.write("\n")

				end_domain = main_link.find("/", 8)
				domain = main_link[0:end_domain]
				dot_count = domain.count(".")

				if dot_count >=2:
					if domain not in total_domains:
						total_domains.append(domain)

				print(main_link)

			print("\n")
			print(colored(f"Total Links : {total_links}", "green"))
			print(colored(f"Total Links With Parameter: {links_with_param}", "green"))
			print(colored(f"Total Domains : {len(total_domains)}", "green"))
		else:
			print(colored(f"Invalid Domain!!!", "red"))
			sys.exit()

	except KeyboardInterrupt:
		print(colored(f"Quitting...", "yellow"))
		sys.exit()
	except requests.exceptions.ConnectionError:
		print(colored(f"\nConnection Error! Please check your internet connection.", "yellow"))
		sys.exit()


try:
	os.system("clear")

	words = "Starting....\n"

	for c in words:
		time.sleep(0.2)
		sys.stdout.write(c)
		sys.stdout.flush()

	url = sys.argv[1]

	if len(sys.argv) !=2:
		print(colored("Usages : python3 main.py domain-name", "yellow"))
		sys.exit()

	grab_urls(url)

except KeyboardInterrupt:
	print(colored(f"\nQuitting...", "yellow"))
	sys.exit()
