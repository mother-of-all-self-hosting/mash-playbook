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
SPDX-FileCopyrightText: 2024 Thomas Miceli
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Gotify

The playbook can install and configure [Gotify](https://gotify.net) for you.

Gotify is a simple server for sending and receiving messages.

See the project's [documentation](https://gotify.net/docs/) to learn what Gotify does and why it might be useful to you.

For details about configuring the [Ansible role for Gotify](https://codeberg.org/acioustick/ansible-role-gotify), you can check them via:
- 🌐 [the role's documentation](https://codeberg.org/acioustick/ansible-role-gotify/src/branch/master/docs/configuring-gotify.md) online
- 📁 `roles/galaxy/gotify/docs/configuring-gotify.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server
- [Postgres](postgres.md) / MySQL / [MariaDB](mariadb.md) / [SQLite](https://www.sqlite.org/) database

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# gotify                                                               #
#                                                                      #
########################################################################

gotify_enabled: true

gotify_hostname: gotify.example.com

########################################################################
#                                                                      #
# /gotify                                                              #
#                                                                      #
########################################################################
```

**Note**: hosting Gotify under a subpath (by configuring the `gotify_path_prefix` variable) does not seem to be possible due to Gotify's technical limitations.

### Select database to use

It is necessary to select a database used by Gotify from a MySQL compatible database, Postgres, and SQLite. See [this section](https://codeberg.org/acioustick/ansible-role-gotify/src/branch/master/docs/configuring-gotify.md#specify-database) on the role's documentation for details.

### Set the username and password for the first user

You also need to set an initial username and password for the first user. Refer to [this section](https://codeberg.org/acioustick/ansible-role-gotify/src/branch/master/docs/configuring-gotify.md#specify-username-and-password-for-the-first-user) on the role's documentation.

## Usage

After running the command for installation, the Gotify instance becomes available at the URL specified with `gotify_hostname`. With the configuration above, the service is hosted at `https://gotify.example.com`.

To get started, open the URL with a web browser to log in to the instance. **Note that the first registered user becomes an administrator automatically.**

## Troubleshooting

See [this section](https://codeberg.org/acioustick/ansible-role-gotify/src/branch/master/docs/configuring-gotify.md#troubleshooting) on the role's documentation for details.

## Related services

- [Apprise API](apprise.md) — Lightweight REST framework that wraps the [Apprise](https://github.com/caronc/apprise) Notification Library
- [ntfy](ntfy.md) — Simple HTTP-based pub-sub notification service to send you push notifications from any computer
