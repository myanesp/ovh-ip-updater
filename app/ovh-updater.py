import ovh
import requests
import time
import json
import os
import sys
from config import *
from datetime import datetime

version = "0.6"
zone_name = os.environ.get("DOMAIN")
sub = os.environ.get("SUBDOMAIN")
ttl = int(os.environ.get("TTL"))
sec = os.environ.get("INTERVAL")
ip_provider = os.environ.get("PROVIDER")
tg_token = os.environ.get("TELEGRAM_TOKEN")
tg_chat = os.environ.get("TELEGRAM_CHAT_ID")
ipv6_supp = os.environ.get("IPV6_SUPPORT").lower()
update_root = os.environ.get("UPDATE_ROOT_DOMAIN").lower()

n_sub = count_sub(sub)

if ipv6_supp == "true":
    ipv6 = obtain_ipv6()

    if not ipv6:
        print(f"{tims()} Cannot obtain your public IPv6 address. Please, check if there is something wrong with your firewall or connection and try again")
        sys.exit()
    else:
        print(f"{tims()} IPv6 obtained succesfully. Your current public IPv6 is {ipv6}, using ipify")

    client = ovh.Client() 

    time.sleep(2)

    if n_sub == 0 or update_root == "true":
        record_ids = client.get(f'/domain/zone/{zone_name}/record', fieldType='AAAA')
        for record in record_ids:
            domain_rec = client.get(f'/domain/zone/{zone_name}/record/{record}')
            if domain_rec["subDomain"] == '':
                if domain_rec['target'] == ipv6:
                    print(f"{tims()} Your IP hasn't changed since last time. Skipping this time...")
                else:
                    client.put(
                        f'/domain/zone/{zone_name}/record/{record}',
                        target=ipv6,
                        ttl=ttl,
                    )
                    time.sleep(2)

                    client.post(f'/domain/zone/{zone_name}/refresh')
                    print(f"{tims()} IP updated for {zone_name} with IP {ipv6}.")
                    if tg_token is None:
                        pass
                    else:
                        message_updated(ip=ipv6, sub=sub, domain=zone_name, chat=tg_chat, token=tg_token)

    if n_sub == 1:
        # Get the ID of the subdomain, needed for update its IP
        record_id = client.get(
            f'/domain/zone/{zone_name}/record',
            fieldType='AAAA',
            subDomain=sub,
        )

        if record_id:

            rec_id = record_id[0]

            # Check for current IP
            current_ip = client.get(f'/domain/zone/{zone_name}/record/{rec_id}')
            target = current_ip['target']
            if target == ipv6:
                print(f"{tims()} Your IP hasn't changed since last time. Skipping this time...")

            else:
                result = client.put(
                    f'/domain/zone/{zone_name}/record/{rec_id}',
                    subDomain=sub,
                    target=ipv6,
                    ttl=ttl,
                )

                time.sleep(2)

                refresh = client.post(f'/domain/zone/{zone_name}/refresh')
                print(f"{tims()} IP updated for {sub}.{zone_name} with IP {ipv6}.")
                if tg_token is None:
                    pass
                else:
                    message_updated(ip=ipv6, sub=sub, domain=zone_name, chat=tg_chat, token=tg_token)

        elif not record_id:
            print(f'{tims()} The subdomain you have provided does not exist. Trying to create it...')

            create = client.post(
                f"/domain/zone/{zone_name}/record",
                target=ipv6,
                ttl=ttl,
                fieldType="AAAA",
                subDomain=sub,
            )

            refresh = client.post(f'/domain/zone/{zone_name}/refresh')
            print(f"{tims()} {sub}.{zone_name} created and assigned IP {ipv6}.")
            if tg_token is None:
                pass
            else:
                send_create(ip=ipv6, sub=sub, domain=zone_name, chat=tg_chat, token=tg_token)

    elif n_sub > 1:
        sub_list = sub.split(',')

        for sub in sub_list:
            record_id = client.get(
                f'/domain/zone/{zone_name}/record',
                fieldType='AAAA',
                subDomain=sub,
            )

            if record_id:

                rec_id = record_id[0]

                current_ip = client.get(f'/domain/zone/{zone_name}/record/{rec_id}')
                target = current_ip['target']

                if target == ipv6:
                    print(f"{tims()} Your IP hasn't changed since last time. Skipping this time...")
                    continue
                else:
                    result = client.put(
                        f'/domain/zone/{zone_name}/record/{rec_id}',
                        subDomain=sub,
                        target=ipv6,
                        ttl=ttl,
                    )

                    time.sleep(2)
                    print(f"{tims()} IP updated for {sub}.{zone_name} with IP {ipv6}.")
                    if tg_token is None:
                        pass
                    else:
                        message_updated(ip=ipv6, sub=sub, domain=zone_name, chat=tg_chat, token=tg_token)

            elif not record_id:
                print(f'{tims()} The subdomain you have provided does not exist. Trying to create it...')

                create = client.post(
                    f"/domain/zone/{zone_name}/record",
                    target=ipv6,
                    ttl=ttl,
                    fieldType="AAAA",
                    subDomain=sub,
                )

                refresh = client.post(f'/domain/zone/{zone_name}/refresh')
                print(f"{tims()} {sub}.{zone_name} created and assigned IP {ipv6}.")
                if tg_token is None:
                    pass
                else:
                    send_create(ip=ipv6, sub=sub, domain=zone_name, chat=tg_chat, token=tg_token)

    refresh = client.post(f'/domain/zone/{zone_name}/refresh')
    print(f"{tims()} All subdomains for {zone_name} has been updated.")

else:
    ipv4 = obtain_ipv4(ip_provider)
    if not ipv4:
        print(f"{tims()} Cannot obtain your public IP address. Please, check if there is something wrong with your firewall or connection and try again")
        sys.exit()
    else:
        print(f"{tims()} IPv4 obtained succesfully. Your current public IPv4 is {ipv4}, using {ip_provider}")

    client = ovh.Client()

    time.sleep(2)

    if n_sub == 0 or update_root == "true":
        record_ids = client.get(f'/domain/zone/{zone_name}/record', fieldType='A')
        for record in record_ids:
            domain_rec = client.get(f'/domain/zone/{zone_name}/record/{record}')
            if domain_rec["subDomain"] == '':
                if domain_rec['target'] == ipv4:
                    print(f"{tims()} Your IP hasn't changed since last time. Skipping this time...")
                else:
                    client.put(
                        f'/domain/zone/{zone_name}/record/{record}',
                        target=ipv4,
                        ttl=ttl,
                    )
                    time.sleep(2)

                    client.post(f'/domain/zone/{zone_name}/refresh')
                    print(f"{tims()} IP updated for {zone_name} with IP {ipv4}.")
                    if tg_token is None:
                        pass
                    else:
                        message_updated(ip=ipv4, sub=sub, domain=zone_name, chat=tg_chat, token=tg_token)

    if n_sub == 1:

        record_id = client.get(
            f'/domain/zone/{zone_name}/record',
            fieldType='A',
            subDomain=sub,
        )

        if record_id:

            rec_id = record_id[0]

            # Check for current IP
            current_ip = client.get(f'/domain/zone/{zone_name}/record/{rec_id}')
            target = current_ip['target']

            if target == ipv4:
                print(f"{tims()} Your IP hasn't changed since last time. Skipping this time...")

            else:

                result = client.put(
                    f'/domain/zone/{zone_name}/record/{rec_id}',
                    subDomain=sub,
                    target=ipv4,
                    ttl=ttl,
                )

                time.sleep(2)

                refresh = client.post(f'/domain/zone/{zone_name}/refresh')
                print(f"{tims()} IP updated for {sub}.{zone_name} with IP {ipv4}.")
                if tg_token is None:
                    pass
                else:
                    message_updated(ip=ipv4, sub=sub, domain=zone_name, chat=tg_chat, token=tg_token)

        elif not record_id:
            print(f'{tims()} The subdomain you have provided does not exist. Trying to create it...')

            create = client.post(
                f"/domain/zone/{zone_name}/record",
                target=ipv4,
                ttl=ttl,
                fieldType="A",
                subDomain=sub,
            )

            refresh = client.post(f'/domain/zone/{zone_name}/refresh')
            print(f"{tims()} {sub}.{zone_name} created and assigned IP {ipv4}.")
            if tg_token is None:
                pass
            else:
                send_create(ip=ipv4, sub=sub, domain=zone_name, chat=tg_chat, token=tg_token)

    elif n_sub > 1:
        sub_list = sub.split(',')

        for sub in sub_list:

            record_id = client.get(
                f'/domain/zone/{zone_name}/record',
                fieldType='A',
                subDomain=sub,
            )

            if record_id:

                rec_id = record_id[0]

                current_ip = client.get(f'/domain/zone/{zone_name}/record/{rec_id}')
                target = current_ip['target']

                if target == ipv4:
                    print(f"{tims()} Your IP hasn't changed since last time. Skipping this time...")
                    continue
                else:
                    result = client.put(
                        f'/domain/zone/{zone_name}/record/{rec_id}',
                        subDomain=sub,
                        target=ipv4,
                        ttl=ttl,
                    )

                    time.sleep(2)
                    print(f"{tims()} IP updated for {sub}.{zone_name} with IP {ipv4}.")
                    if tg_token is None:
                        pass
                    else:
                        message_updated(ip=ipv4, sub=sub, domain=zone_name, chat=tg_chat, token=tg_token)

            elif not record_id:
                print(f'{tims()} The subdomain you have provided does not exist. Trying to create it...')

                create = client.post(
                    f"/domain/zone/{zone_name}/record",
                    target=ipv4,
                    ttl=ttl,
                    fieldType="A",
                    subDomain=sub,
                )

                refresh = client.post(f'/domain/zone/{zone_name}/refresh')
                print(f"{tims()} {sub}.{zone_name} created and assigned IP {ipv4}.")
                if tg_token is None:
                    pass
                else:
                    send_create(ip=ipv4, sub=sub, domain=zone_name, chat=tg_chat, token=tg_token)

        refresh = client.post(f'/domain/zone/{zone_name}/refresh')
        print(f"{tims()} All subdomains for {zone_name} has been updated.")
