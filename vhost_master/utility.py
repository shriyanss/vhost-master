import tldextract

from colorama import init, Fore, Style

init(autoreset=True)

class Utility:
    def get_domain_from_subdomain(subdomain):
        extracted_info = tldextract.extract(subdomain)
        domain = extracted_info.domain
        tld = extracted_info.suffix
        
        return f"{domain}.{tld}"
    
    def print_vhost_exists(vhost, request, url):
        print(f"{Fore.GREEN}[+] {vhost} on {url}{Style.RESET_ALL}")
        # color as per status code

        if str(request.status_code).startswith("2"):
            color = Fore.GREEN
        elif str(request.status_code).startswith("3"):
            color = Fore.CYAN
        elif str(request.status_code).startswith("4"):
            color = Fore.YELLOW
        elif str(request.status_code).startswith("5"):
            color = Fore.RED
        else:
            color = ""
        print(f"    {color}Status: {request.status_code}{Style.RESET_ALL}")