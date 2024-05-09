import ovh
import requests
import time
import json
import os
import sys
from config import *
from datetime import datetime 

zone_name = os.environ.get("DOMAIN")
sub = os.environ.get("SUBDOMAIN")
ttl = os.environ.get("TTL")
sec = os.environ.get("INTERVAL")
ip_provider = os.environ.get("PROVIDER")

ip = obtain_ip(ip_provider)

if not ip:
    print(f"{tims()} Cannot obtain your public IP address. Please, check if there is something wrong with your firewall or connection and try again")
    sys.exit()
else:
    print(f"{tims()} IP obtained succesfully. Your current public IP is {ip}, using {ip_provider}")

client = ovh.Client() 

time.sleep(2)

# Get the ID of the subdomain, needed for update its IP
record_id = client.get(f'/domain/zone/{zone_name}/record', 
    fieldType='A', 
    subDomain=sub,
)

## If it is correct, check if the record is empty to know if it exists previously or not
if record_id:

    rec_id = record_id[0]

    result = client.put(f'/domain/zone/{zone_name}/record/{rec_id}', 
        subDomain=sub, 
        target=ip, 
        ttl=ttl, 
    )

    time.sleep(2)

    refresh = client.post(f'/domain/zone/{zone_name}/refresh')
    print(f"{tims()} IP updated for {sub}.{zone_name} with IP {ip}.")

elif not record_id:
    print(f'{tims()} The subdomain you have provided does not exist. Please, create it first on your OVH web console and try again.')
    sys.exit()

