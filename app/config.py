import os
import requests
import sys
from datetime import datetime

def obtain_ipv4(ip_provider):
    
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
        print("Cannot obtain your public IPv4 address with your provider. Checking again with others...")
        if ip_provider == 'ipify':
            try:
                ip = requests.get('https://am.i.mullvad.net/ip').text.strip()
                return(ip)
            except:
                pass 

            try:
                ip = requests.get('https://ifconfig.io/ip').text.strip()
                return(ip)
            except:
                pass 

        elif ip_provider == 'mullvad':
            try:
                ip = requests.get('https://api.ipify.org').text
                return(ip)
            except:
                pass 

            try:
                ip = requests.get('https://ifconfig.io/ip').text.strip()
                return(ip)
            except:
                pass 
        elif ip_provider == 'ifconfig':
            try:
                ip = requests.get('https://api.ipify.org').text
                return(ip)
            except:
                pass 

            try:
                ip = requests.get('https://am.i.mullvad.net/ip').text.strip()
                return(ip)
            except:
                pass 

    if not ip:
        print("Cannot obtain your public IPv4 address. Please, check if there is something wrong with your firewall or connection and try again")
        sys.exit()

def obtain_ipv6():
    
    ip = str()
    
    try:
        ip = requests.get('https://api6.ipify.org').text
        return(ip)
    except:
        pass

    if not ip:
        print("Cannot obtain your public IPv6 address. Please, check if there is something wrong with your firewall or connection and try again")
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

def message_updated(ip, domain, sub, chat, token):

    message = f"{tims()} - OVH IP UPDATER\n\nYour IP has changed for {sub}.{domain}.\nIt has been updated with this new IP: {ip}."
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat}&text={message}"
    requests.get(url)

def send_create(ip, domain, sub, chat, token):

    message = f"{tims()} - OVH IP UPDATER\n\nCreated subdomain {sub}.{domain} with IP {ip}."
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat}&text={message}"
    requests.get(url)