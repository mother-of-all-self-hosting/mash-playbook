# FreshRSS

[FreshRSS](https://freshrss.org) is a self-hosted RSS and Atom feed aggregator. It is lightweight, easy to work with, powerful, and customizable.

## Dependencies

This service requires the following other services:

-   a [Traefik](traefik.md) reverse-proxy server
-   an optional [Postgres](postgres.md) database, but [SQLite](https://www.sqlite.org/) is set by default.

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# freshrss                                                             #
#                                                                      #
########################################################################

freshrss_enabled: true

freshrss_hostname: mash.example.com
freshrss_path_prefix: /freshrss

########################################################################
#                                                                      #
# /freshrss                                                            #
#                                                                      #
########################################################################
```

## Usage

After installation, visit the configured path and complete the setup through the wizard.

Feel free to follow FreshRSS [official documentation](http://freshrss.github.io/FreshRSS/en/).
