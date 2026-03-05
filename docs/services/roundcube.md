<!--
SPDX-FileCopyrightText: 2020 Aaron Raimist
SPDX-FileCopyrightText: 2020 Chris van Dijk
SPDX-FileCopyrightText: 2020 Dominik Zajac
SPDX-FileCopyrightText: 2020 Mickaël Cornière
SPDX-FileCopyrightText: 2020-2024 MDAD project contributors
SPDX-FileCopyrightText: 2020-2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2022 François Darveau
SPDX-FileCopyrightText: 2022 Julian Foad
SPDX-FileCopyrightText: 2022 Warren Bailey
SPDX-FileCopyrightText: 2023 Antonis Christofides
SPDX-FileCopyrightText: 2023 Felix Stupp
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2023 Sergio Durigan Junior
SPDX-FileCopyrightText: 2024 Thomas Miceli
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Roundcube

The playbook can install and configure [Roundcube](https://roundcube.net/) for you.

Roundcube is a browser-based multilingual IMAP client with an application-like user interface. It provides full functionality you expect from an email client, including MIME support, address book, folder manipulation, message searching and spell checking.

See the project's [documentation](https://docs.roundcube.net/) to learn what Roundcube does and why it might be useful to you.

## Dependencies

This service requires the following other services:

- [Postgres](postgres.md) / MySQL / [MariaDB](mariadb.md) / [SQLite](https://www.sqlite.org/) database
- [Traefik](traefik.md) reverse-proxy server

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
roundcube_path_prefix: /roundcube

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

### Select database to use

It is necessary to select a database used by Roundcube from a MySQL compatible database, Postgres, and SQLite. See [`defaults/main.yml`](https://github.com/mother-of-all-self-hosting/ansible-role-roundcube/blob/main/defaults/main.yml) of the role for details.

## Usage

After running the command for installation, the Roundcube instance becomes available at the URL specified with `roundcube_hostname` and `roundcube_path_prefix`. With the configuration above, the service is hosted at `https://mash.example.com/roundcube`.

To get started, open the URL with a web browser, and log in to the instance with the username and password, which are the same ones for your IMAP server.
