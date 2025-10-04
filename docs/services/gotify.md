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

The playbook can install and configure [Gotify](https://gotify.io) for you.

Gotify is a self-hosted pastebin powered by Git. All snippets are stored in a Git repository and can be read and/or modified using standard Git commands, or with the web interface.

See the project's [documentation](https://gotify.io/docs/) to learn what Gotify does and why it might be useful to you.

For details about configuring the [Ansible role for Gotify](https://codeberg.org/acioustick/ansible-role-gotify), you can check them via:
- 🌐 [the role's documentation](https://codeberg.org/acioustick/ansible-role-gotify/src/branch/master/docs/configuring-gotify.md) online
- 📁 `roles/galaxy/gotify/docs/configuring-gotify.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server
- (optional) [Postgres](postgres.md) / MySQL / [MariaDB](mariadb.md) database — Gotify will default to [SQLite](https://www.sqlite.org/) if Postgres is not enabled

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

### Set 32-byte hex digits for secret key

You also need to specify **32-byte hex digits** for session store and encrypting MFA data on the database. To do so, add the following configuration to your `vars.yml` file. The value can be generated with `openssl rand -hex 32` or in another way.

```yaml
gotify_environment_variables_secret_key: YOUR_SECRET_KEY_HERE
```

>[!NOTE]
> Other type of values such as one generated with `pwgen -s 64 1` does not work.

### Select database to use (optional)

By default Gotify is configured to use Postgres, but you can choose other database such as SQLite and MySQL. See [this section](https://codeberg.org/acioustick/ansible-role-gotify/src/branch/master/docs/configuring-gotify.md#specify-database-optional) on the role's documentation for details.

## Usage

After running the command for installation, the Gotify instance becomes available at the URL specified with `gotify_hostname`. With the configuration above, the service is hosted at `https://gotify.example.com`.

To get started, open the URL with a web browser, and register the account. **Note that the first registered user becomes an administrator automatically.**

## Troubleshooting

See [this section](https://codeberg.org/acioustick/ansible-role-gotify/src/branch/master/docs/configuring-gotify.md#troubleshooting) on the role's documentation for details.

## Related services

- [PrivateBin](privatebin.md) — Minimalist, open source online pastebin where the server has zero knowledge of pasted data
