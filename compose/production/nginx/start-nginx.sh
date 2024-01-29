#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

# Create a self signed default certificate, so Nginx can start before we have
# any real certificates.

# Ensure we have folders available
if [[ ! -f /usr/share/nginx/certificates ]];then
  mkdir -p /usr/share/nginx/certificates
fi

# If certificates don't exist yet we must ensure we create them (dummy) to start nginx.
if [[ ! -f /usr/share/nginx/certificates/fullchain.pem ]]; then
  echo "Create dummy SSL certificates..."
  openssl genrsa -out /usr/share/nginx/certificates/privkey.pem 4096
  openssl req -new -key /usr/share/nginx/certificates/privkey.pem -out /usr/share/nginx/certificates/cert.csr -nodes -subj "/C=PT/ST=World/L=World/O=${CERT_NAME:-example.com}/OU=${OU_CERT_NAME:-example} lda/CN=${CERT_NAME:-example.com}"
  openssl x509 -req -days 365 -in /usr/share/nginx/certificates/cert.csr -signkey /usr/share/nginx/certificates/privkey.pem -out /usr/share/nginx/certificates/fullchain.pem
fi

# Check if legitimate certificates are requested.
if [[ ${CERT_GENERATE:-0} == 1 ]]; then
  echo "Request to create authenticated SSL certificates..."

  # Here we send certbot Emission/Renewal to system background as running service.
  # Info: Let's Encrypt certificates are valid for 90 days. You can read about why here. There is no way to adjust this,
  #       there are no exceptions. We recommend automatically renewing your certificates every 60 days.
  # Note: || true is used in case certbot faced an error.
  # Note: `&`: It starts a asynchronous process.
  # $(while :; do /usr/src/compose/certbot.sh || true; sleep "${CERT_RENEW_INTERVAL:-12h}"; done;) &
  while true; do
    /usr/src/compose/certbot.sh || true; sleep "${CERT_RENEW_INTERVAL:-12h}"
  done &

  # Check for changes in the certificate (i.e renewals or first start) and send this process to background.
  # shellcheck disable=SC2091
  # $(while inotifywait -e close_write /usr/share/nginx/certificates; do nginx -s reload; done) &
  while inotifywait -e close_write /usr/share/nginx/certificates; do
    nginx -s reload
  done &

  # Start nginx with daemon off as our main pid.
  # Info: nginx has multiple signals to use with:
  #
  #       >> nginx -s <SIGNAL>
  #
  #       where <SIGNAL> can be one of the following:
  #       quit – Shut down gracefully (the SIGQUIT signal)
  #       reload – Reload the configuration file (the SIGHUP signal)
  #       reopen – Reopen log files (the SIGUSR1 signal)
  #       stop – Shut down immediately (or fast shutdown, the SIGTERM singal)
  nginx -g "daemon off;"

else

  # Start nginx with daemon off as our main pid with dummy certificates.
  nginx -g "daemon off;"

fi

exit 0
