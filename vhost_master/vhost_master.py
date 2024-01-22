import socket
import sys
import argparse
import requests
import os
from time import sleep
import threading
import tldextract

from colorama import init, Fore, Style

init(autoreset=True)

from .bruteforce import vhost_exists
from .utility import Utility

# disable python requests warning
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class BruteForcer:
    def __init__(self, wordlist, domain, max_threads) -> None:
        self.wordlist = wordlist
        self.domain = domain
        self.max_threads = max_threads
    
    def start(self, host, port, protocol):
        target_url = f"{protocol}://{host}:{port}/"

        # print(f"[i] Starting bruteforce on {target_url}\n    Domain: {self.domain}")
        
        threads = []
        with open(self.wordlist, 'r') as file:
            for line in file:
                line = line.replace('\n', '')
                vhost = f"{line}.{self.domain}"

                # wait for active thread count to be less than max_threads
                while True:
                    if threading.active_count() > self.max_threads:
                        pass
                    else:
                        thread = threading.Thread(target=vhost_exists, args=(target_url, vhost, conditions))
                        thread.start()
                        threads.append(thread)
                        break
        for thread in threads:
            thread.join()

version = "0.0.3"

def get_ip_address(host):
    try:
        ip_address = socket.gethostbyname(host)
        return ip_address
    except socket.error as e:
        return None
    
def process_pipe(pipe_data):
    parts = pipe_data.split("\n")
    parts.remove('')
    return parts

def print_output(multiple_hostnames_ips, silent):
    """Print final result"""
    if not silent:
        print(f"Total IPs: {len(multiple_hostnames_ips)}\n")

        # data structure for multiple_hostnames_ips:-
        # [{ip: []}, {ip: []}]
        print("IP Addresses:-")
        for ip_dict in multiple_hostnames_ips:
            print(list(ip_dict.keys())[0])
    else:
        for ip_dict in multiple_hostnames_ips:
            print(list(ip_dict.keys())[0])

def banner():
    latest_version = (requests.get("https://raw.githubusercontent.com/shriyanss/vhost-master/main/.info/version").text).replace('\n', '')
    # https://raw.githubusercontent.com/shriyanss/vhost-master/main/.info/version
    if latest_version != version:
        status = f"{Fore.RED}Outdated. Latest: v{latest_version}{Style.RESET_ALL}"
    else:
        status = f"{Fore.GREEN}Latest{Style.RESET_ALL}"
    print(f"""__     ___   _           _        __  __           _            
\ \   / / | | | ___  ___| |_     |  \/  | __ _ ___| |_ ___ _ __ 
 \ \ / /| |_| |/ _ \/ __| __|____| |\/| |/ _` / __| __/ _ \ '__|
  \ V / |  _  | (_) \__ \ ||_____| |  | | (_| \__ \ ||  __/ |   
   \_/  |_| |_|\___/|___/\__|    |_|  |_|\__,_|___/\__\___|_|   \n

By {Fore.CYAN}@shriyanss{Style.RESET_ALL}
https://github.com/shriyanss/vhost-master
v{Fore.YELLOW}{version}{Style.RESET_ALL} ({status})
""")

def main():
    # argparser
    parser = argparse.ArgumentParser()

    parser.add_argument('-s', '--silent', action='store_true', help='Silent mode (boolean flag)')
    parser.add_argument('-b', '--bruteforce', action="store_true", help='Bruteforce using the given wordlist', default=False)
    parser.add_argument('-c', '--conditions', type=str, help='Conditions to consider if a valid VHost exists. See https://github.com/shriyanss/vhost-master/match_conditions.md', default="status!=404")
    parser.add_argument('-w', '--wordlist', type=str, help='Wordlist to use (required with -b/--bruteforce)')
    parser.add_argument('-t', "--threads", type=int, help='Number of threads (default=30)', default=30)
    parser.add_argument('-p', '--protocol', type=str, help='Protocol to use (default="http:80,https:443"', default="http:80,https:443")
    parser.add_argument('--force-all-ports', action="store_true", default=False, help='If both http:80 & https:443 are open, tool will skip http:80 and show results for https:443. Use this flag to disable it')
    args = parser.parse_args()
    targets = None

    global silent
    silent = args.silent

    global conditions
    conditions = ((args.conditions).replace(' ', '')).split(',')

    # print banner if not silent
    if not args.silent:
        banner()
    
    # check if the -b flag is specified, then the wordlist (-w) should be also specified
    if args.bruteforce:
        if not args.wordlist:
            print("No wordlist specified... ")
            exit(1)
        else:
            # if the wordlist is specified, check if the wordlist exists
            if os.path.exists(args.wordlist):
                empty_wordlist = True
                # if the wordlist exists, check it is not empty
                with open(args.wordlist, 'r') as file:
                    for line in file:
                        if line.startswith("#"):
                            pass
                        else:
                            empty_wordlist = False
                            break
                if empty_wordlist == True:
                    print("Wordlist is empty (or just have comments, i.e. those starting with #)")
                    exit(1)
            else:
                print("Wordlist doesn't exist: " + args.wordlist)
                exit(1)

    if not sys.stdin.isatty():
        # Read from pipe
        pipe_data = sys.stdin.read()
        targets = process_pipe(pipe_data)
    if targets == None:
        print("Usage: cat subdomains.txt | vhost_master <options>")
        exit(1)
    
    # get the IP addresses
    ip_info = {}
    # loop through hostnames
    for hostname in targets:
        ip = get_ip_address(hostname)
        try:
            ip_info[ip].append(hostname) if ip is not None else None
        except:
            ip_info[ip] = []
            ip_info[ip].append(hostname) if ip is not None else None
    
    # get the IP addresses who have more than 1 hostname
    multiple_hostnames_ips = []
    for key in ip_info:
        if len(ip_info[key]) > 1:
            multiple_hostnames_ips.append({key: ip_info[key]})
    
    # print IP addresses which have more than one hostname
    print_output(multiple_hostnames_ips, args.silent)
    print()

    if args.bruteforce == True:

        if args.force_all_ports == False:
            print(f"{Fore.YELLOW}[i] Will prioritize https:443 over http:80 if both are open. Test both with --force-all-ports{Style.RESET_ALL}")
        wordlist_list = []
        # bruteforcer = BruteForcer(wordlist=args.wordlist, domain=domain, max_threads=args.threads)

        # read the wordlist and append to an array
        with open(args.wordlist, 'r') as file:
            for line in file:
                if line.startswith("#"):
                    pass
                else:
                    wordlist_list.append(line.replace('\n', ''))

        # loop through multiple_hostname_ips
        # data structure for multiple_hostnames_ips:-
        # [{ip: []}, {ip: []}]
        for ip in multiple_hostnames_ips:
            ip_address = (list(ip.keys())[0])
            protocols = (args.protocol).split(",")
            # get the domain for the target
            domain = Utility.get_domain_from_subdomain(ip[ip_address][0])

            # check if scanning for both port 80 and 443 is enabled
            # creates 2 vars, both_major_ports_enabled and both_major_ports_open
            if "http:80" in protocols and "https:443" in protocols:
                both_major_ports_enabled = True

                # check is port 80 and 443 are open on IP address
                try:
                    r_http = requests.get(f"http://{ip_address}:80/", verify=False)
                    r_https = requests.get(f"https://{ip_address}:443/", verify=False)
                    both_major_ports_open = True
                except:
                    # print(e)
                    both_major_ports_open = False
            else:
                both_major_ports_enabled = False
            
            # test for port 80 and 443 initially and remove them
            # given condition it is to be tested, they are open and force all port is enabled
            if both_major_ports_enabled == True and both_major_ports_open == True and args.force_all_ports == True:
                protocols.remove("http:80")
                protocols.remove("https:443")

                # initiate bruteforce on port 80 and 443
                bruteforcer = BruteForcer(wordlist=args.wordlist, domain=domain, max_threads=args.threads)

                # start bruteforce on port 80 and 443
                # print(f"--force-all-ports enabled. Starting bruteforce on port 80 and 443")
                bruteforcer.start(host=ip_address, port=80, protocol="http")
                bruteforcer.start(host=ip_address, port=443, protocol="https")

            # remove port 80 and 443 if both are open and enabled for testing
            # this is to reduce scan time
            # or simply prioritize port 443 over port 80
                

            elif both_major_ports_enabled == True and both_major_ports_open == True and args.force_all_ports == False:
                # pass
                protocols.remove("http:80")
                # protocols.remove("https:443")
            
            if len(protocols) > 0:
                for pp in protocols:
                    protocol, port = pp.split(":")[0], pp.split(":")[1]
                    # print(f"\n[i] Testing {protocol}:{port} on {ip_address}")
                    bruteforcer = BruteForcer(wordlist=args.wordlist, domain=domain, max_threads=args.threads)

                    # if port 80 and 443 both are open, skip http:80
                    # print(f"{protocol}://{ip_address}:{port}/")
                    bruteforcer.start(host=ip_address, port=port, protocol=protocol)
                

if __name__ == '__main__':
    main()