<!--
SPDX-FileCopyrightText: 2023 Alejandro AR
SPDX-FileCopyrightText: 2023 Slavi Pantaleev
SPDX-FileCopyrightText: 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# FreshRSS

The playbook can install and configure [FreshRSS](https://freshrss.org) for you.

FreshRSS is a self-hosted RSS and Atom feed aggregator, which is lightweight, easy to work with, powerful, and customizable.

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server
- (optional) [Postgres](postgres.md) database — FreshRSS will default to [SQLite](https://www.sqlite.org/) if Postgres is not enabled

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# freshrss                                                             #
#                                                                      #
########################################################################

freshrss_enabled: true

freshrss_hostname: freshrss.example.com

########################################################################
#                                                                      #
# /freshrss                                                            #
#                                                                      #
########################################################################
```

**Note**: hosting FreshRSS under a subpath (by configuring the `freshrss_path_prefix` variable) does not seem to be possible due to FreshRSS's technical limitations. See [this issue](https://github.com/mother-of-all-self-hosting/mash-playbook/issues/116) for details.

### Set a database password

You also need to set a password for the database by adding the following configuration to your `vars.yml` file. Make sure to replace `DATABASE_PASSWORD_HERE` with your own value. Generating a strong token (e.g. `pwgen -s 64 1`) is recommended.

```yaml
freshrss_database_password: DATABASE_PASSWORD_HERE
```

## Usage

After running the command for installation, FreshRSS becomes available at the specified hostname like `https://freshrss.example.com`.

You can go to the URL with a web browser to complete installation on the server. During the installation, the database password specified to `freshrss_database_password` variable is required to be submitted.

Refer to FreshRSS [official documentation](http://freshrss.github.io/FreshRSS/en/) for usage.

## Related services

- [Miniflux](miniflux.md) — Minimalist and opinionated feed reader
