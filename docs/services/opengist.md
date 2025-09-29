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

# Opengist

The playbook can install and configure [Opengist](https://opengist.io) for you.

Opengist is a self-hosted pastebin powered by Git. All snippets are stored in a Git repository and can be read and/or modified using standard Git commands, or with the web interface.

See the project's [documentation](https://opengist.io/docs/) to learn what Opengist does and why it might be useful to you.

For details about configuring the [Ansible role for Opengist](https://codeberg.org/acioustick/ansible-role-opengist), you can check them via:
- 🌐 [the role's documentation](https://codeberg.org/acioustick/ansible-role-opengist/src/branch/master/docs/configuring-opengist.md) online
- 📁 `roles/galaxy/opengist/docs/configuring-opengist.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server
- (optional) [Postgres](postgres.md) / MySQL / [MariaDB](mariadb.md) database — Opengist will default to [SQLite](https://www.sqlite.org/) if Postgres is not enabled

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# opengist                                                             #
#                                                                      #
########################################################################

opengist_enabled: true

opengist_hostname: opengist.example.com

########################################################################
#                                                                      #
# /opengist                                                            #
#                                                                      #
########################################################################
```

**Note**: hosting Opengist under a subpath (by configuring the `opengist_path_prefix` variable) does not seem to be possible due to Opengist's technical limitations.

### Set 32-byte hex digits for secret key

You also need to specify **32-byte hex digits** for session store and encrypting MFA data on the database. To do so, add the following configuration to your `vars.yml` file. The value can be generated with `openssl rand -hex 32` or in another way.

```yaml
opengist_environment_variables_secret_key: YOUR_SECRET_KEY_HERE
```

>[!NOTE]
> Other type of values such as one generated with `pwgen -s 64 1` does not work.

### Select database to use (optional)

By default Opengist is configured to use Postgres, but you can choose other database such as SQLite and MySQL. See [this section](https://codeberg.org/acioustick/ansible-role-opengist/src/branch/master/docs/configuring-opengist.md#specify-database-optional) on the role's documentation for details.

## Usage

After running the command for installation, the Opengist instance becomes available at the URL specified with `opengist_hostname`. With the configuration above, the service is hosted at `https://opengist.example.com`.

To get started, open the URL with a web browser, and register the account. **Note that the first registered user becomes an administrator automatically.**

## Troubleshooting

See [this section](https://codeberg.org/acioustick/ansible-role-opengist/src/branch/master/docs/configuring-opengist.md#troubleshooting) on the role's documentation for details.
