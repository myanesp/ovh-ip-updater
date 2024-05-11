# ovh-ip-updater

[![](https://badgen.net/badge/icon/github?icon=github&label)](https://github.com/myanesp/ovh-ip-updater)
[![](https://badgen.net/badge/icon/docker?icon=docker&label)]()
[![Docker Pulls](https://badgen.net/docker/pulls/myanesp/ovh-ip-updater?icon=docker&label=pulls)](https://hub.docker.com/r/myanesp/ovh-ip-updater/)
![](https://badgen.net/github/stars/myanesp/ovh-ip-updater?icon=github&label=stars)
[![Docker Image Size](https://badgen.net/docker/size/myanesp/ovh-ip-updater?icon=docker&label=image%20size)](https://hub.docker.com/r/myanesp/ovh-ip-updater/)
![Github last-commit](https://img.shields.io/github/last-commit/myanesp/ovh-ip-updater)
![Github license](https://badgen.net/github/license/myanesp/ovh-ip-updater)
[![Project Status: Active - The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)

## Why?

The traditional way of updating the IP of the subdomains of your OVH domains if you have a dynamic IP is through DynHost, the Duck-DNS-kind-of DDNS system of OVH, and the Internet is full of scripts and programs to update with that system. 

However, I was looking for a system that uses the official API, as that is my favourite method and the one I've been using with other providers. So I tinkered a little and this image, however, uses the OVH API so you don't need to setup a DynHost domain and associate it to your A/AAAA records. With this Docker container, you just need your keys and token and the subdomains you want to update. 

With the release (I hope it will be soon!) of the v1.0 version, you will also forget to access the web portal of OVH to create the subdomains you want to update with this image, as the container will create it if the subdomain does not exist previously.

## How to run

### Obtain API keys from OVH console

In order to update and modify the IP value for your subdomains, you need to grab some credentials from your OVH account. For that, you can follow [this official guide](https://help.ovhcloud.com/csm/en-gb-api-getting-started-ovhcloud-api?id=kb_article_view&sysparm_article=KB0042784) and create a new app. At the end, you should have an application key, an application secret and your consumer key.

Then, you need to put those credentials in a `.conf` file, like the one provided in this repo [as an example](ohv.conf).

Your `ovh.conf` file should look like this:

```
[default]
endpoint=ovh-eu # can be ovh-us, ovh-ca and others depending on your region

[ovh-eu]
application_key=r4nd0mstr1ng
application_secret=4n0th3rstr1ngw1thch4r4ct3s
consumer_key=4n0th3rstr1ngw1thch4r4ct3s
```

Put it within the same folder as the `docker-compose.yml` file and map it into the container as in the docker compose example just below.

### Run with docker compose

This image is available both on [Docker Hub](https://hub.docker.com/r/myanesp/ovh-ip-updater) and [GitHub Container Registry](https://github.com/myanesp/ovh-ip-updater), so you're free to choose from which one you're going to download the image. Edit the following docker compose/docker run command to match your needs (domain, subdomains, image registry, the IP fetching provider and the conf file) and you are ready to go!

```
services:
  ovh-ip-updater:
    image: ghcr.io/myanesp/ovh-ip-updater
    # image: myanesp/ovh-ip-updater # if you prefer to download from DockerHub
    restart: always
    container_name: ovh-ip-updater
    volumes:
      - ./my-ovh.conf:/etc/ovh.conf:ro
      - /etc/localtime:/etc/localtime:ro
    environment:
      - DOMAIN=yourdomain.com
      - SUBDOMAIN=subdomain,subdomain2
      # - PROVIDER=ipify
      # - TTL=600
```

### Run with docker run

```
docker run -d \
  --name ovh-ip-updater \
  --restart always \
  -v ./my-ovh.conf:/etc/ovh.conf:ro \
  -v /etc/localtime:/etc/localtime:ro \
  -e DOMAIN=yourdomain.com \
  -e SUBDOMAIN=subdomain,subdomain2 \
  ghcr.io/myanesp/ovh-ip-updater # or myanesp/ovh-ip-updater
```

## Environmental variables

| VARIABLE | MANDATORY | VALUE | DEFAULT |
|----------|:---------:|-------------------------------------------------------------|---------|
| DOMAIN | ✅ | Your domain (like `example.com`) | `empty` |
| SUBDOMAIN| ✅ | Subdomain to update the IP (like `www`, if you want to update more: `sub,sub2`...) | `empty` |
| TTL | ❌ | The time-to-live in seconds of the record | `600` |
| PROVIDER | ❌ | Service for checking the public IP address (can be `ipify`, `mullvad` or `ifconfig`) | `ipify` |


## Planned features for v1.0, stable version

- [x] Option to update more than a subdomain at a time
- [ ] Option to select interval between IP updates (now is only every 5 minutes), and update the IP at container boot
- [ ] Fallback for obtaining public IP address
- [ ] Create the record for the subdomain if it does not exist
- [ ] Multiarch support
- [x] Publish on DockerHub
- [ ] Improve the log outputs and generate an ovh.log
- [ ] Support for IPv6
- [ ] Rethink the way of forcing updates if IP hasn't changed
- [ ] Multilingual support
- [ ] Remove cron jobs and migrate to s6-overlay