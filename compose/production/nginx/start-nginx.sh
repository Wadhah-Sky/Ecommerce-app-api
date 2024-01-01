#!/usr/bin/env bash

# Create a self signed default certificate, so Nginx can start before we have
# any real certificates.

# Ensure we have folders available
if [[ ! -f /usr/share/nginx/certificates/fullchain.pem ]];then
    mkdir -p /usr/share/nginx/certificates
fi

# If certificates don't exist yet we must ensure we create them (dummy) to start nginx.
if [[ ! -f /usr/share/nginx/certificates/fullchain.pem ]]; then
    openssl genrsa -out /usr/share/nginx/certificates/privkey.pem 4096
    openssl genrsa -out /usr/share/nginx/certificates/privkey.pem 4096
    openssl req -new -key /usr/share/nginx/certificates/privkey.pem -out /usr/share/nginx/certificates/cert.csr -nodes -subj "/C=PT/ST=World/L=World/O=example.store/OU=example lda/CN=example.store"
    openssl x509 -req -days 365 -in /usr/share/nginx/certificates/cert.csr -signkey /usr/share/nginx/certificates/privkey.pem -out /usr/share/nginx/certificates/fullchain.pem
fi

# Check if legitimate certificates are requested.
if [[ ${CERT_GENERATE:-1} == 1 ]]; then

  # Send certbot Emission/Renewal to background
  # Let's Encrypt certificates are valid for 90 days. You can read about why here. There is no way to adjust this,
  # there are no exceptions. We recommend automatically renewing your certificates every 60 days.
  if while :; do /usr/src/compose/certbot.sh; sleep "${CERT_RENEW_INTERVAL:-60d}"; done; then

    # Check for changes in the certificate (i.e renewals or first start) and send this process to background
    if while inotifywait -e close_write /usr/share/nginx/certificates; do nginx -s reload; done; then

    # Start nginx with daemon off as our main pid.
    nginx -g "daemon off;"

    fi;

  fi;

else

  # Start nginx with daemon off as our main pid with dummy certificates.
  nginx -g "daemon off;"

fi
