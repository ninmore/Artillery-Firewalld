#!/usr/bin/python
#
# simple remove banned ip
#
#
import sys
from src.core import *

try:
    ipaddress = sys.argv[1]
    if is_valid_ipv4(ipaddress):
        path = check_banlist_path()
        fileopen = file(path, "r")
        data = fileopen.read()
        data = data.replace(ipaddress + "\n", "")
        filewrite = file(path, "w")
        filewrite.write(data)
        filewrite.close()

        print("Removing ip from ipset alias set...")
        
        try:
            proc = subprocess.check_call("ipset del artillery-bans %s" % (ipaddress) , shell=True)
        except subprocess.CalledProcessError as er:
            print("[!] Could not remove the IP Address, is it valid?")
            sys.exit()
        
        print("The ip was successfully removed from the bans list.")
        
    # if not valid then flag
    else:
        print("[!] Not a valid IP Address. Exiting.")
        sys.exit()

except IndexError:
    print("Description: Simple removal of IP address from banned sites.")
    print("[!] Usage: remove_ban.py <ip_address_to_ban>")
