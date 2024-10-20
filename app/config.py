import os
import requests
import sys
from datetime import datetime

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
            ip = requests.get('https://am.i.mullvad.net/ip').text.strip()
            return(ip)
        except:
            pass
    elif ip_provider == 'ifconfig':
        try:
            ip = requests.get('https://ifconfig.io/ip').text.strip()
            return(ip)
        except:
            pass

    else:
        return("Provider not supported")
        sys.exit()

    if not ip:
        print("Cannot obtain your public IP address. Please, check if there is something wrong with your firewall or connection and try again")
        sys.exit()

def tims():
    ts = datetime.now().strftime("[%d-%m %H:%M:%S]")
    return(ts)

def count_sub(env):

    if env:
        subdomains = env.split(',')

        subquan = len(subdomains)

        return(subquan)

    else:
        print(f"{tims()} Subdomain environment variable is not set, exiting")
        sys.exit()

def send_message(ip, domain, chat, token):

    message = f"{tims()} - OVH IP UPDATER\n\nYour IP has changed, now is {ip}.\nThe subdomains of {domain} have been updated with this new IP."
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat}&text={message}"
    requests.get(url)