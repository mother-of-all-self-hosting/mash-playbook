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

# MediaWiki

The playbook can install and configure [MediaWiki](https://mediawiki.net) for you.

MediaWiki is a simple server for sending and receiving messages.

See the project's [documentation](https://mediawiki.net/docs/) to learn what MediaWiki does and why it might be useful to you.

For details about configuring the [Ansible role for MediaWiki](https://github.com/mother-of-all-self-hosting/ansible-role-mediawiki), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-mediawiki/blob/main/docs/configuring-mediawiki.md) online
- 📁 `roles/galaxy/mediawiki/docs/configuring-mediawiki.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server
- [Postgres](postgres.md) / MySQL / [MariaDB](mariadb.md) / [SQLite](https://www.sqlite.org/) database

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# mediawiki                                                            #
#                                                                      #
########################################################################

mediawiki_enabled: true

mediawiki_hostname: mediawiki.example.com

########################################################################
#                                                                      #
# /mediawiki                                                           #
#                                                                      #
########################################################################
```

**Note**: hosting MediaWiki under a subpath (by configuring the `mediawiki_path_prefix` variable) does not seem to be possible due to MediaWiki's technical limitations.

### Select database to use

It is necessary to select a database used by MediaWiki from a MySQL compatible database, Postgres, and SQLite. See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-mediawiki/blob/main/docs/configuring-mediawiki.md#specify-database) on the role's documentation for details.

### Set the username and password for the first user

You also need to set an initial username and password for the first user. Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-mediawiki/blob/main/docs/configuring-mediawiki.md#specify-username-and-password-for-the-first-user) on the role's documentation.

## Usage

After running the command for installation, the MediaWiki instance becomes available at the URL specified with `mediawiki_hostname`. With the configuration above, the service is hosted at `https://mediawiki.example.com`.

To get started, open the URL with a web browser to log in to the instance. **Note that the first registered user becomes an administrator automatically.**

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-mediawiki/blob/main/docs/configuring-mediawiki.md#troubleshooting) on the role's documentation for details.

## Related services

- [ntfy](ntfy.md) — Simple HTTP-based pub-sub notification service to send you push notifications from any computer
