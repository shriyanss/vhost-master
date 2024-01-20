import socket
import sys
import argparse
import requests

version = "0.0.1"

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
    latest_version = requests.get("https://raw.githubusercontent.com/shriyanss/vhost-master/main/.info/version").text
    # https://raw.githubusercontent.com/shriyanss/vhost-master/main/.info/version
    if latest_version != version:
        status = f"Outdated. Latest: {latest_version}"
    else:
        status = "Latest"
    print(f"""__     ___   _           _        __  __           _            
\ \   / / | | | ___  ___| |_     |  \/  | __ _ ___| |_ ___ _ __ 
 \ \ / /| |_| |/ _ \/ __| __|____| |\/| |/ _` / __| __/ _ \ '__|
  \ V / |  _  | (_) \__ \ ||_____| |  | | (_| \__ \ ||  __/ |   
   \_/  |_| |_|\___/|___/\__|    |_|  |_|\__,_|___/\__\___|_|   \n

By @shriyanss: https://github.com/shriyanss
{version} ({status})
""")

def main():
    # argparser
    parser = argparse.ArgumentParser()

    parser.add_argument('-s', '--silent', action='store_true', help='Silent mode (boolean flag)')
    args = parser.parse_args()
    targets = None

    # print banner if not silent
    if not args.silent:
        banner()

    if not sys.stdin.isatty():
        # Read from pipe
        pipe_data = sys.stdin.read()
        targets = process_pipe(pipe_data)
    if targets == None:
        print("Usage: cat subdomains.txt | vhost_master")
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
    
    print_output(multiple_hostnames_ips, args.silent)

if __name__ == '__main__':
    main()
