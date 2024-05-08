import os
import requests
import sys

def obtain_ip(ip_provider):
    
    ip = str()
    
    if ip_provider == 'ipify':
        try:
            ip = requests.get('https://api.ipify.org').text
            return(ip)
        except:
            pass
    elif ip_provider == 'mullvad':
        try:
            ip = requests.get('https://am.i.mullvad.net/ip').text
            return(ip)
        except:
            pass
    elif ip_provider == 'ifconfig':
        try:
            ip = requests.get('https://ifconfig.io/ip').text
            return(ip)
        except:
            pass

    else:
        return("Provider not supported")
        sys.exit()

    if not ip:
        print("Cannot obtain your public IP address. Please, check if there is something wrong with your firewall or connection and try again")
        sys.exit()
