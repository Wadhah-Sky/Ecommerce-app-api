#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

# This script is running in the background every 60 days by default, and its responsible for emiting
# and renewing the certificates, copying them from the letsencrypt folder to the location nginx will be
# using to serve.
# Given how certbot works, we must copy the location of the files, as if we were to serve directly
# from the {LETSENCRYPT_DIR} certbot would see there were already some files in there from our dummy
# certificates creation, and would create a symlink to another {CERT_DOMAINS}.001 location that would complicate
# our logic, and that’s why we will used a fixed location to serve our certificates, given that we wan’t
# this nginx to have simple reverse proxy/ load balancer configurations, and not a multi domain approach,
# with multiple certificates.
# As shown bellow, we see that we have a --webroot-path , and this is the folder where certbot will create the
# challenges files to prove ownership of domain.

# Info: The ACME server refuses to issue a certificate for 'example.com' domain name, because it is forbidden by
#       policy.

# Info: common errors that you can find in /var/log/letsencrypt/letsencrypt.log
#
#       1- Hint: The Certificate Authority failed to download the temporary challenge files created by Certbot.
#          Ensure that the listed domains serve their content from the provided --webroot-path/-w and that files
#          created there can be downloaded from the internet.
#
#       2- Type: Unautherized for the given domain
#
#       These errors related to domain that can't be reached through PING/curl command or the given domain names
#       illegitimate. So you should make sure your Nginx is running on public IP address and given domains/subdomains
#       are registered with A/AAAA records in DNS server where A and AAAA records are equally important when it comes
#       to resolving DNS. The difference lies in that A records is used to resolve a hostname which corresponds to
#       an IPv4 address, while AAAA records are used to resolve a domain name which corresponds to an IPv6 address.

# Info: to check if domain is available with windows cmd:
#
#       For main domain:
#       >> ping jamieandcassie.store
#
#       For subdomain:
#       >> ping www.jamieandcassie.store
#
#       In linux:
#
#       >> curl -Iki http://jamieandcassie.store
#       >> curl -Iki http://www.jamieandcassie.store

echo "Check webroot path directory is exists otherwise create it"

# Check if file of /var/www/certbot is not exists, create it.
if [[ ! -f /var/www/certbot ]]; then
    mkdir -p /var/www/certbot
fi

# Clear the existing certificates file in "live" folder in letsencrypt directory for given $CERT_NAME. To prevent of
# creating another copy of received certificates from server.
echo "Clear letsencrypt directory for received certificates from ACM server"
if [[ -f ${LETSENCRYPT_DIR:-/etc/letsencrypt}/live/${CERT_NAME:-jamieandcassie.store} ]]; then
    rm -rf "${LETSENCRYPT_DIR:-/etc/letsencrypt}/live/${CERT_NAME:-jamieandcassie.store}"
fi


# Check that if a given custom certbot command is available and not None.
if [[ ${CUSTOM_CERT_COMMAND:-None} != None ]]; then
  cert_command="certbot $CUSTOM_CERT_COMMAND"
  # eval command is a built-in function that allows you to execute arguments as a bash command.
  eval "$cert_command" || true

# Else, check if environment variable "CERT_TEST_CERT" is 1 (means call certbot for test purpose).
elif [[ ${CERT_TEST_CERT:-1} == 1 ]]; then

  # Note: Let's Encrypt limits the amount of available free certificates per month (100), so in case of test, run
  #       this service with adding the flag: --dry-run. to the commands renew, certonly or certbot, or you can
  #       test your syntax without actually having any certificates issued on your behalf. As a result, you will
  #       receive detailed output in the console:
  #
  #       >> docker-compose -f <file_of_docker_compose> run --rm certbot sh -c
  #          "certonly --webroot --webroot-path /var/www/certbot/ --dry-run -d <domain-name>"
  #
  # Info: To obtain a certificate and also install it, use the certbot run command (or certbot , which is the same).
  #       To just obtain the certificate without installing it anywhere, the certbot certonly (“certificate only”)
  #       command can be used. You should know if you’re running a local webserver for which you have the ability to
  #       modify the content being served, and you’d prefer not to stop the webserver during the certificate issuance
  #       process, you can use the webroot plugin to obtain a certificate by including certonly and --webroot on the
  #       command line. see for more details https://eff-certbot.readthedocs.io/en/stable/using.html

  # Some of useful flags (attribute) for certbot command,
  # check for more details:
  # A) https://github.com/certbot/certbot/blob/master/certbot/docs/cli-help.txt
  # B) https://eff-certbot.readthedocs.io/en/stable/using.html
  #
  # 1) --test-cert: Use the Let's Encrypt staging server to obtain or revoke test (invalid) certificates;
  #                 equivalent to --server https://acme-staging-v02.api.letsencrypt.org/directory
  #                 (default: False).
  #
  # 2) --non-interactive: Run without ever asking for user input. This may require additional command line flags;
  #                       the client will try to explain which ones are required if it finds one missing (default: False).
  #
  # 3) --config-dir: Configuration directory. (default: /etc/letsencrypt).
  #
  # 4) --domains: Domain names to include. For multiple domains you can use multiple -d flags or enter a comma
  #               separated list (without space) of domains as a parameter. All domains will be included as Subject
  #               Alternative Names on the certificate. The first domain will be used as the certificate name, unless
  #               otherwise specified or if you already have a certificate with the same name. In the case of a name
  #               conflict, a number like -0001 will be appended to the certificate name. (default: Ask).
  #
  # 5) --cert-name: Certificate name to apply. This name is used by Certbot for housekeeping and in file paths,
  #                 it doesn't affect the content of the certificate itself. Certificate name cannot contain filepath
  #                 separators (i.e. '/' or '\', depending on the platform). To see certificate names, run
  #
  #                 >> certbot certificates
  #
  #                 When creating a new certificate, specifies the new certificate's name. (default: the first provided
  #                 domain or the name of an existing certificate on your system for the same domains).
  #
  # 6) --email: Email used for registration and recovery contact. Use comma to register multiple emails, ex:
  #             u1@example.com,u2@example.com. (default: Ask).
  #
  # 7) --no-eff-email: Don't share your e-mail address with EFF (default: None).
  #
  # 8) --webroot: is plugin that required of many (--nginx, --manual, --apache ...etc) to create certificate,
  #               with webroot can place files in a server's webroot folder for authentication.
  #
  # 9) --webroot-path: public_html / webroot path. This can be specified multiple times to handle
  #                    different domains; each domain will have the webroot path that preceded it.
  #                    For instance:
  #
  #                    `-w /var/www/example -d example.com -d www.example.com -w /var/www/thing -d thing.net -d m.thing.net`
  #
  #                    (default: Ask)
  #
  # 10) --debug: Show tracebacks in case of errors (default: False)
  #
  # 11) --debug-challenges: After setting up challenges (challenge is what it use during authorization with the most
  #                         preferred challenge listed first (Eg, "dns" or "http,dns"). Not all plugins support all
  #                         challenges.), wait for user input before submitting to CA.
  #                         When used in combination with the `-v` option, the challenge URLs or FQDNs
  #                         and their expected return values are shown. (default: False)
  #
  # 12) --agree-tos: Agree to the ACME Subscriber Agreement (default: Ask)
  #
  # 13) --expand: If an existing certificate is a strict subset of the requested names, always expand and replace it
  #               with the additional names. (default: Ask)
  #
  # 14) --redirect: Automatically redirect all HTTP traffic to HTTPS for the newly authenticated vhost.
  #                 (default: redirect enabled for install and run, disabled for enhance).
  #
  # 15) --uir: Add the "Content-Security-Policy: upgrade-insecure-requests" header to every HTTP response.
  #            Forcing the browser to use https:// for every http:// resource. (default: None)
  #
  # 16) --staple-ocsp: Enables OCSP Stapling. A valid OCSP response is stapled to the certificate that
  #                    the server offers during TLS. (default: None)
  #
  # 17) --verbose: This flag can be used multiple times to incrementally increase the verbosity of
  #                output, e.g. -vvv. (default: 0)
  #
  # 18) --no-verify-ssl: Disable verification of the ACME server's certificate. The root certificates
  #                      trusted by Certbot can be overriden by setting the REQUESTS_CA_BUNDLE environment
  #                      variable. (default: False)
  #
  # 19) --register-unsafely-without-email: Specifying this flag enables registering an account with no email
  #                                        address. This is strongly discouraged, because you will be unable to
  #                                        receive notice about impending expiration or revocation of your certificates
  #                                        or problems with your Certbot installation that will lead to failure to
  #                                        renew. (default: False)

  # Note: || true is used in case certbot faced an error.

  certbot certonly \
          --test-cert \
          --non-interactive \
          --config-dir "${LETSENCRYPT_DIR:-/etc/letsencrypt}" \
          --domains "${CERT_DOMAINS:-jamieandcassie.store}" \
          --cert-name "${CERT_NAME:-jamieandcassie.store}" \
          --agree-tos \
          --no-eff-email \
          --register-unsafely-without-email \
          --webroot \
          --webroot-path /var/www/certbot/ \
          --verbose || echo "Certbot has failed to generate test certificate" && exit 0

# Else condition
else
  certbot certonly \
          --non-interactive \
          --config-dir "${LETSENCRYPT_DIR:-/etc/letsencrypt}" \
          --domains "${CERT_DOMAINS:-jamieandcassie.store}" \
          --cert-name "${CERT_NAME:-jamieandcassie.store}" \
          --email "${CERT_EMAIL:-wadhah_sky@hotmail.com}" \
          --agree-tos \
          --no-eff-email \
          --webroot \
          --webroot-path /var/www/certbot/ \
          --expand \
          --redirect || echo "Certbot has failed" && exit 0
fi

# Check if we get the certificate files from server, copy it to wanted destination as specified in default.conf file as
# ssl_certificate and ssl_certificate_key.
if [[ -f "${LETSENCRYPT_DIR:-/etc/letsencrypt}/live/${CERT_NAME:-jamieandcassie.store}/privkey.pem" ]]; then

  # Remove all file from /usr/share/nginx/certificates/.
  rm -rf /usr/share/nginx/certificates/* &&

  # Use the cp command to create a copy of the contents of the file or directory specified by the SourceFile or
  # SourceDirectory parameters into the file or directory specified by the TargetFile or TargetDirectory parameters.
  cp "${LETSENCRYPT_DIR:-/etc/letsencrypt}/live/${CERT_NAME:-jamieandcassie.store}/*" /usr/share/nginx/certificates/

fi

exit 0