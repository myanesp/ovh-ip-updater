FROM python:3.13-alpine3.20

LABEL org.opencontainers.image.title="OVH IP updater Docker image"
LABEL org.opencontainers.image.description="Docker image for updating the DNS records of your OVH domain using the API"
LABEL org.opencontainers.image.authors="Mario Yanes <mario.yanes@uc3m.es> (@myanesp)"
LABEL org.opencontainers.image.url=https://github.com/myanesp/ovh-ip-updater/blob/main/README.md
LABEL org.opencontainers.image.documentation=https://github.com/myanesp/ovh-ip-updater
LABEL org.opencontainers.image.source=https://github.com/myanesp/ovh-ip-updater
LABEL org.opencontainers.image.licenses="AGPL-3.0-or-later"

ENV DOMAIN=
ENV SUBDOMAIN=
ENV TTL=600
ENV PROVIDER=ipify

RUN pip3 install --upgrade pip && pip3 install --no-cache-dir ovh requests

RUN echo "@reboot sleep 10 && python3 /app/ovh-updater.py" >> /etc/crontabs/root && \ 
    echo "*/5 * * * * python3 /app/ovh-updater.py" >> /etc/crontabs/root

COPY app/ /app

CMD ["crond", "-f", "-c", "/etc/crontabs"]