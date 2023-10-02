# Roundcube

[Roundcube](https://roundcube.net/) is a browser-based multilingual IMAP client with an application-like user interface. It provides full functionality you expect from an email client, including MIME support, address book, folder manipulation, message searching and spell checking.

## Dependencies

This service requires the following other services:

- a [Postgres](postgres.md) database
- a [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# roundcube                                                            #
#                                                                      #
########################################################################

roundcube_enabled: true

roundcube_hostname: mash.example.com

roundcube_path_prefix: "/roundcube"

# The default IMAP server to connect to.
roundcube_default_imap_host: "imap.example.com"
# If not specified, the default port is 143.
roundcube_default_imap_port: "143"

# The default SMTP server to use.
roundcube_smtp_server: "smtp.example.com"
# If not specified, the default port is 587.
roundcube_smtp_port: "587"

########################################################################
#                                                                      #
# /roundcube                                                           #
#                                                                      #
########################################################################
```

In the example configuration above, we configure the service to be hosted at `https://mash.example.com/roundcube`.

You can remove the `roundcube_path_prefix` variable definition, to make it default to `/`, so that the service is served at `https://mash.example.com/`.


## Usage

After installation, you should be able to access your new Roundcube instance at the configured URL (see above).

The username/password you will use to login are the same ones used in your IMAP server.
