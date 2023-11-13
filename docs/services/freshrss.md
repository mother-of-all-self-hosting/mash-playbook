# FreshRSS

[FreshRSS](https://freshrss.org) is a self-hosted RSS and Atom feed aggregator. It is lightweight, easy to work with, powerful, and customizable.

## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server
- an optional [Postgres](postgres.md) database, but FreshRSS will default to [SQLite](https://www.sqlite.org/) if you don't have Postgres enabled.


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# freshrss                                                             #
#                                                                      #
########################################################################

freshrss_enabled: true

freshrss_hostname: freshrss.example.com

# Put a strong password below, generated with `pwgen -s 64 1` or in another way.
# You will need to use this password in the setup wizard after installation.
freshrss_database_password: ''

########################################################################
#                                                                      #
# /freshrss                                                            #
#                                                                      #
########################################################################
```

**NOTE**: while FreshRSS can potentially be installed under a subpath (using the `freshrss_path_prefix` variable), this [doesn't currently work](https://github.com/mother-of-all-self-hosting/mash-playbook/issues/116) and will be fixed in the future. For now, you'd need to install it on its own dedicated hostname.


## Usage

After installation, visit the configured path and complete the setup through the wizard. To do this you will need the database password from your `vars.yml` file (in the `freshrss_database_password` variable).

Feel free to follow FreshRSS [official documentation](http://freshrss.github.io/FreshRSS/en/).
