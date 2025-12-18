<!--
SPDX-FileCopyrightText: 2020 - 2024 MDAD project contributors
SPDX-FileCopyrightText: 2020 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2020 Aaron Raimist
SPDX-FileCopyrightText: 2020 Chris van Dijk
SPDX-FileCopyrightText: 2020 Dominik Zajac
SPDX-FileCopyrightText: 2020 Mickaël Cornière
SPDX-FileCopyrightText: 2022 François Darveau
SPDX-FileCopyrightText: 2022 Julian Foad
SPDX-FileCopyrightText: 2022 Warren Bailey
SPDX-FileCopyrightText: 2023 Antonis Christofides
SPDX-FileCopyrightText: 2023 Felix Stupp
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Mumble

The playbook can install and configure [Mumble](https://www.mumble.info) for you.

Mumble is a free and open source voice chat application known for its low latency and high voice quality.

See the project's [documentation](https://www.mumble.info/documentation/) to learn what Mumble does and why it might be useful to you.

For details about configuring the [Ansible role for Mumble](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az4VBCibmQHyfHKEWTAJmQKBAAjtsv), you can check them via:
- 🌐 [the role's documentation](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az4VBCibmQHyfHKEWTAJmQKBAAjtsv/tree/docs/configuring-mumble.md) online
- 📁 `roles/galaxy/mumble/docs/configuring-mumble.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Prerequisites

You may need to open some ports to your server if another firewall is used in front of the server. Refer to [the role's documentation](https://app.radicle.xyz/nodes/seed.radicle.garden/rad:z4VBCibmQHyfHKEWTAJmQKBAAjtsv/tree/docs/configuring-mumble.md#prerequisites) to check which ones to be configured.

## Dependencies

This service requires the following other services:

- [Postgres](postgres.md) / MySQL / [MariaDB](mariadb.md) / [SQLite](https://www.sqlite.org/) database
- (optional) [Traefik](traefik.md) reverse-proxy server — required on the default configuration for retrieving a TLS certificate
- (optional) [traefik-certs-dumper](traefik-certs-dumper.md) — required on the default configuration for setting up the TLS certificate

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# mumble                                                               #
#                                                                      #
########################################################################

mumble_enabled: true

mumble_hostname: mumble.example.com

########################################################################
#                                                                      #
# /mumble                                                              #
#                                                                      #
########################################################################
```

### Select database to use

It is necessary to select a database used by Mumble from a MySQL compatible database, Postgres, and SQLite. See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az4VBCibmQHyfHKEWTAJmQKBAAjtsv/tree/docs/configuring-mumble.md#specify-database) on the role's documentation for details.

### Setting admin's password (optional)

It is possible to specify the admin (`SuperUser`) password by configuring a variable for it. See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az4VBCibmQHyfHKEWTAJmQKBAAjtsv/tree/docs/configuring-mumble.md#setting-admin-39-s-password) on the role's documentation for details. **If not specified, a random password will be generated upon the first startup.**

## Usage

After running the command for installation, the Mumble instance becomes available at the URL specified with `mumble_hostname`. With the configuration above, the service is hosted at `mumble.example.com:64738`.

To get started, open the URL on a client for Mumble to log in to the server.

As anyone can use the server without a password by default, you might also want to set one for the server to the `mumble_environment_variables_mumble_config_serverpassword` variable to authenticate who can log in to it.

## Troubleshooting

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az4VBCibmQHyfHKEWTAJmQKBAAjtsv/tree/docs/configuring-mumble.md#troubleshooting) on the role's documentation for details.
