import socket
import sys
import argparse
import requests
import os
import threading
import subprocess

from colorama import init, Fore, Style

init(autoreset=True)

from .bruteforce import vhost_exists
from .utility import Utility

# disable python requests warning
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

version = "0.0.4"

class BruteForcer:
    def __init__(self, wordlist, domain, max_threads) -> None:
        self.wordlist = wordlist
        self.domain = domain
        self.max_threads = max_threads
    
    def start(self, host, port, protocol):
        target_url = f"{protocol}://{host}:{port}/"

        # print(f"[i] Starting bruteforce on {target_url}\n    Domain: {self.domain}")
        
        threads = []
        try:
            wordlist = self.wordlist
            # for line in file:
            #     line = line.replace('\n', '')
            #     wordlist.append(line)
            
            # print(wordlist)
            # # for -n/--new flag
            # if new == True:
            #     for target in wordlist:
            #         if target in wordlist:
            #             print(True)
            #             wordlist.remove(target)    
            # print(wordlist)

            for line in wordlist:
                if absolute_wordlist == True:
                    vhost = line
                else:
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
        except Exception as e:
            print(e)
            exit(1)
        
        for thread in threads:
            thread.join()

    def start_single_host(self, host, port, protocol):
        target_url = f"{protocol}://{host}:{port}/"

        # print(f"[i] Starting bruteforce on {target_url}\n    Domain: {self.domain}")
        
        threads = []
        for line in wordlist_list:
            line = line.replace('\n', '')

            if absolute_wordlist == True:
                vhost = line
            else:
                vhost = f"{line}"

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

class IPResolve():
    def __init__(self):
        pass
    def resolve(self, hostname):
        ip = get_ip_address(hostname)
        try:
            ip_info[ip].append(hostname) if ip is not None else None
        except:
            ip_info[ip] = []
            ip_info[ip].append(hostname) if ip is not None else None

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

def check_update(latest_version):
    if latest_version != version:
        print(f"{Fore.YELLOW}[i]{Style.RESET_ALL} Updating to latest version...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "vhost-master"])
        print(f"{Fore.GREEN}[i]{Style.RESET_ALL} Updated to the latest version...")
        print(f"{Fore.YELLOW}Please rerun the tool again{Style.RESET_ALL}")
        exit(1)

def banner():
    latest_version = (requests.get("https://raw.githubusercontent.com/shriyanss/vhost-master/main/.info/version").text).replace('\n', '')

    if no_update == False:
        check_update(latest_version)
    
    # https://raw.githubusercontent.com/shriyanss/vhost-master/main/.info/version
    # get the latest version
    if latest_version != version:
        status = f"{Fore.RED}Outdated. Latest: v{latest_version}{Style.RESET_ALL}"
    else:
        status = f"{Fore.GREEN}Latest{Style.RESET_ALL}"
    
    # get the message
    message = (requests.get("https://raw.githubusercontent.com/shriyanss/vhost-master/main/.info/message").text)

    print(f"""__     ___   _           _        __  __           _            
\ \   / / | | | ___  ___| |_     |  \/  | __ _ ___| |_ ___ _ __ 
 \ \ / /| |_| |/ _ \/ __| __|____| |\/| |/ _` / __| __/ _ \ '__|
  \ V / |  _  | (_) \__ \ ||_____| |  | | (_| \__ \ ||  __/ |   
   \_/  |_| |_|\___/|___/\__|    |_|  |_|\__,_|___/\__\___|_|   \n

By {Fore.CYAN}@shriyanss{Style.RESET_ALL}
https://github.com/shriyanss/vhost-master
v{Fore.YELLOW}{version}{Style.RESET_ALL} ({status})
{message}
""")

def main():
    # argparser
    parser = argparse.ArgumentParser()

    parser.add_argument('--resolver-runs', type=int, default=10, help='Number of times to run the resolver to increase the accuracy of the output (default=10)')
    parser.add_argument('-s', '--silent', action='store_true', help='Silent mode (boolean flag)')
    parser.add_argument('--discover-vhost', type=str, help='Discover which IP address has the given VHost')
    parser.add_argument('-b', '--bruteforce', action="store_true", help='Bruteforce using the given wordlist', default=False)
    parser.add_argument('--skip-resolve', action="store_true", default=False, help='Skip resolving IP addresses. Rather, use file parsed from pipe as IP address list (should be used with -b/--bruteforce) (-d/--domain required)')
    parser.add_argument('-d', '--domain', type=str, help='Target domain (required with --skip-resolve)')
    parser.add_argument('-c', '--conditions', type=str, help='Conditions to consider if a valid VHost exists. See https://github.com/shriyanss/vhost-master/match_conditions.md', default="status!=404")
    parser.add_argument('-w', '--wordlist', type=str, help='Wordlist to use (required with -b/--bruteforce)')
    parser.add_argument('--absolute-wordlist', action="store_true", help='Absolute values given in the wordlist', default=False)
    parser.add_argument('-t', "--threads", type=int, help='Number of threads (default=30)', default=30)
    parser.add_argument('-p', '--protocol', type=str, help='Protocol to use (default="http:80,https:443")', default="http:80,https:443")
    parser.add_argument('--force-all-ports', action="store_true", default=False, help='If both http:80 & https:443 are open, tool will skip http:80 and show results for https:443. Use this flag to disable it')
    parser.add_argument('--no-update', action="store_true", default=False, help="Don't update the tool if it is not the latest version")
    parser.add_argument('-n', '--new', action='store_true', default=False, help="Display the new subdomains only. Remove the known ones")
    args = parser.parse_args()
    targets = None

    global silent
    silent = args.silent

    global new
    new = args.new

    global conditions
    conditions = ((args.conditions).replace(' ', '')).split(',')

    global absolute_wordlist
    absolute_wordlist = args.absolute_wordlist

    global no_update
    no_update = args.no_update

    # print banner if not silent
    if not args.silent:
        banner()
    
    if args.bruteforce == True and args.discover_vhost != None:
        print("Bruteforce flag -b/--bruteforce and --discover-vhost can't be used together")
        exit(1)
    
    # checks for --skip-resolve flag
    if args.skip_resolve == True:
        if args.domain == None:
            print("Domain is required with --skip-resolve flag...")
            exit(1)
        elif args.bruteforce == False:
            print("-b/--bruteforce is required with --skip-resolve flag")
            exit(1)
    
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
    
    # if the -n/--new flag is used, bruteforce flag should be also used
    if args.new == True and (args.bruteforce == False or args.absolute_wordlist == False):
        print("-n/--new flag can be only used with -b/--bruteforce flag")
        exit(1)

    # read data from pipe
    if not sys.stdin.isatty():
        pipe_data = sys.stdin.read()
        targets = process_pipe(pipe_data)
    if targets == None:
        print("Usage: cat subdomains.txt | vhost_master <options>")
        exit(1)
    
    # get the IP addresses
    global ip_info
    ip_info = {}

    if args.skip_resolve == False:
        threads = []
        ip_resolver = IPResolve()

        for i in range(args.resolver_runs):
        # loop through hostnames
            for hostname in targets:
                # IPResolve.resolve(hostname)
                thread = threading.Thread(target=ip_resolver.resolve, args=(hostname,))
                thread.start()
                threads.append(thread)

                # Wait for the number of active threads to be less than the maximum allowed threads
                while threading.active_count() > args.threads:
                    pass
                # thread = threading.Thread(target=ip_resolver.resolve, args=(hostname,))
                # thread.start()
                # while True:
                #     if threading.active_count() > args.threads:
                #         pass
                #     else:
                #         threads.append(thread)
                #         break
                # ip = get_ip_address(hostname)
                # try:
                #     ip_info[ip].append(hostname) if ip is not None else None
                # except:
                #     ip_info[ip] = []
                #     ip_info[ip].append(hostname) if ip is not None else None
            
            # get the IP addresses who have more than 1 hostname
        
        for thread in threads:
            thread.join()

        multiple_hostnames_ips = []
        for key in ip_info:
            if len(ip_info[key]) > 1:
                multiple_hostnames_ips.append({key: ip_info[key]})
    else:
        multiple_hostnames_ips = []
        for add_ip_address in targets:
            ip_info[add_ip_address] = []
            multiple_hostnames_ips.append({add_ip_address: []})

    
    # print IP addresses which have more than one hostname
    print_output(multiple_hostnames_ips, args.silent)
    print()

    if args.discover_vhost != None:
        print(f"{Fore.YELLOW}[i] Discovering VHost {args.discover_vhost} on {len(multiple_hostnames_ips)} IP addresses {Style.RESET_ALL}")

        if args.force_all_ports == False:
            print(f"{Fore.YELLOW}[i] Will prioritize https:443 over http:80 if both are open. Test both with --force-all-ports{Style.RESET_ALL}")
        
        global wordlist_list
        wordlist_list = [args.discover_vhost]
        # bruteforcer = BruteForcer(wordlist=args.wordlist, domain=domain, max_threads=args.threads)

        # loop through multiple_hostname_ips
        # data structure for multiple_hostnames_ips:-
        # [{ip: []}, {ip: []}]
        for ip in multiple_hostnames_ips:
            add_ip_address = (list(ip.keys())[0])
            protocols = (args.protocol).split(",")
            # get the domain for the target
            domain = Utility.get_domain_from_subdomain(ip[add_ip_address][0])

            # check if scanning for both port 80 and 443 is enabled
            # creates 2 vars, both_major_ports_enabled and both_major_ports_open
            if "http:80" in protocols and "https:443" in protocols:
                both_major_ports_enabled = True

                # check is port 80 and 443 are open on IP address
                try:
                    r_http = requests.get(f"http://{add_ip_address}:80/", verify=False)
                    r_https = requests.get(f"https://{add_ip_address}:443/", verify=False)
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
                bruteforcer = BruteForcer(wordlist=wordlist_list, domain=domain, max_threads=args.threads)

                # start bruteforce on port 80 and 443
                # print(f"--force-all-ports enabled. Starting bruteforce on port 80 and 443")
                bruteforcer.start(host=add_ip_address, port=80, protocol="http")
                bruteforcer.start(host=add_ip_address, port=443, protocol="https")

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
                    bruteforcer = BruteForcer(wordlist=wordlist_list, domain=domain, max_threads=args.threads)

                    # if port 80 and 443 both are open, skip http:80
                    # print(f"{protocol}://{ip_address}:{port}/")
                    bruteforcer.start_single_host(host=add_ip_address, port=port, protocol=protocol)

    # feature to bruteforce VHosts
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
        
        # remove the existing subdomains if the -n/--new flag is enabled
        if args.new == True:
            for target in targets:
                if target in wordlist_list:
                    wordlist_list.remove(target)

                # try:
                #     wordlist_list.remove(target.replace('\n', ''))
                # except:
                #     pass

        # loop through multiple_hostname_ips
        # data structure for multiple_hostnames_ips:-
        # [{ip: []}, {ip: []}]
        for ip in multiple_hostnames_ips:
            add_ip_address = (list(ip.keys())[0])
            protocols = (args.protocol).split(",")
            # get the domain for the target
            if args.domain == None:
                domain = Utility.get_domain_from_subdomain(ip[add_ip_address][0])
            else:
                domain = args.domain

            # check if scanning for both port 80 and 443 is enabled
            # creates 2 vars, both_major_ports_enabled and both_major_ports_open
            if "http:80" in protocols and "https:443" in protocols:
                both_major_ports_enabled = True

                # check is port 80 and 443 are open on IP address
                try:
                    r_http = requests.get(f"http://{add_ip_address}:80/", verify=False)
                    r_https = requests.get(f"https://{add_ip_address}:443/", verify=False)
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
                bruteforcer = BruteForcer(wordlist=wordlist_list, domain=domain, max_threads=args.threads)

                # start bruteforce on port 80 and 443
                # print(f"--force-all-ports enabled. Starting bruteforce on port 80 and 443")
                bruteforcer.start(host=add_ip_address, port=80, protocol="http")
                bruteforcer.start(host=add_ip_address, port=443, protocol="https")

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
                    bruteforcer = BruteForcer(wordlist=wordlist_list, domain=domain, max_threads=args.threads)

                    # if port 80 and 443 both are open, skip http:80
                    # print(f"{protocol}://{ip_address}:{port}/")
                    bruteforcer.start(host=add_ip_address, port=port, protocol=protocol)
                

if __name__ == '__main__':
    main()
