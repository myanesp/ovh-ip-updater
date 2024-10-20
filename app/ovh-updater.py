import ovh
import requests
import time
import json
import os
import sys
from config import *
from datetime import datetime

version = "0.3.2"
zone_name = os.environ.get("DOMAIN")
sub = os.environ.get("SUBDOMAIN")
ttl = os.environ.get("TTL")
sec = os.environ.get("INTERVAL")
ip_provider = os.environ.get("PROVIDER")
tg_token = os.environ.get("TELEGRAM_TOKEN")
tg_chat = os.environ.get("TELEGRAM_CHAT_ID")

ip = obtain_ip(ip_provider)

if not ip:
    print(f"{tims()} Cannot obtain your public IP address. Please, check if there is something wrong with your firewall or connection and try again")
    sys.exit()
else:
    print(f"{tims()} IP obtained succesfully. Your current public IP is {ip}, using {ip_provider}")

client = ovh.Client() 

time.sleep(2)

n_sub = count_sub(sub)

if n_sub == 1:

    # Get the ID of the subdomain, needed for update its IP
    record_id = client.get(f'/domain/zone/{zone_name}/record', 
        fieldType='A', 
        subDomain=sub,
    )

    ## If it is correct, check if the record is empty to know if it exists previously or not
    if record_id:

        rec_id = record_id[0]

        # Check for current IP
        current_ip = client.get(f'/domain/zone/{zone_name}/record/{rec_id}')
        target = current_ip['target']

        if target == ip:
            print(f"{tims()} Your IP hasn't changed since last time. Skipping this time...")

        else:

            result = client.put(f'/domain/zone/{zone_name}/record/{rec_id}', 
                subDomain=sub, 
                target=ip, 
                ttl=ttl, 
            )

            time.sleep(2)

            refresh = client.post(f'/domain/zone/{zone_name}/refresh')
            print(f"{tims()} IP updated for {sub}.{zone_name} with IP {ip}.")
            if tg_token == None:
                pass
            else:
                send_message(ip = ip, domain = zone_name, chat = tg_chat, token = tg_token)

    elif not record_id:
        print(f'{tims()} The subdomain you have provided does not exist. Please, create it first on your OVH web console and try again.')
        sys.exit()

elif n_sub > 1:
    sub_list = sub.split(',')

    for sub in sub_list:
        record_id = client.get(f'/domain/zone/{zone_name}/record', 
        fieldType='A', 
        subDomain=sub,
        )

    ## If it is correct, check if the record is empty to know if it exists previously or not
        if record_id:

            rec_id = record_id[0]
            # Check for current IP
            current_ip = client.get(f'/domain/zone/{zone_name}/record/{rec_id}')
            target = current_ip['target']

            if target == ip:
                print(f"{tims()} Your IP hasn't changed since last time. Skipping this time...")
                continue
            else:
                result = client.put(f'/domain/zone/{zone_name}/record/{rec_id}', 
                    subDomain=sub, 
                    target=ip, 
                    ttl=ttl, 
                )

                time.sleep(2)
                print(f"{tims()} IP updated for {sub}.{zone_name} with IP {ip}.")

        elif not record_id:
            print(f'{tims()} The subdomain you have provided does not exist. Please, create it first on your OVH web console and try again.')
            sys.exit()

        refresh = client.post(f'/domain/zone/{zone_name}/refresh')
        if tg_token == None:
            pass
        else:
            send_message(ip = ip, domain = zone_name, chat = tg_chat, token = tg_token)
            print(f"{tims()} All subdomains for {zone_name} has been updated.")

