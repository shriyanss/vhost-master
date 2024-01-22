import requests
import re

from .utility import Utility

# function to check if a vhost exists
# conditions are of form AND
# means that all conditions should match
def vhost_exists(url, vhost, conditions):
    try:
        num_conditions = 0
        exists = False
        headers = {
            "Host": vhost # as subdomain.target.com
        }
        r = requests.get(url, headers=headers, verify=False, timeout=5)

        # check conditions
        for condition in conditions:
            # check status code
            if condition.startswith("status"):
                condition_status = int((re.findall(r"\d+", condition))[0])
                if "!=" in condition:
                    if r.status_code != condition_status:
                        num_conditions += 1
                        # exists = True
                if "==" in condition:
                    if r.status_code == condition_status:
                        num_conditions += 1
                        # exists = True
        
        # if exists == True:
        #     Utility.print_vhost_exists(vhost=vhost, request=r, url=url)
        if num_conditions == len(conditions):
            Utility.print_vhost_exists(vhost=vhost, request=r, url=url)
        return num_conditions/len(conditions)
    except:
        pass