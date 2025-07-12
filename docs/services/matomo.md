# Matomo

[Matomo](https://matomo.org/) (formerly Piwik) is a free and open source web analytics platform.

## Dependencies

This service requires the following other services:

- [MariaDB](mariadb.md) database
- [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# matomo                                                               #
#                                                                      #
########################################################################

matomo_enabled: true

matomo_hostname: matomo.example.com

########################################################################
#                                                                      #
# /matomo                                                              #
#                                                                      #
########################################################################

```

## Usage

After installation, visit your Matomo instance at the configured URL. You'll be guided through a setup wizard where you can:

1. Create your administrator account
2. Configure your first website to track
3. Get the tracking code to add to your website

Add the tracking code to your website's HTML to start collecting analytics data.

For additional configuration options, refer to [ansible-role-matomo](https://github.com/mother-of-all-self-hosting/ansible-role-matomo)'s `defaults/main.yml` file.
