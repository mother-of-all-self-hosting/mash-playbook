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

# MariaDB

The playbook can install and configure [MariaDB](https://mariadb.org) for you.

MariaDB is a powerful, open source object-relational database system.

See the project's [documentation](https://mariadb.org/documentation/) to learn what MariaDB does and why it might be useful to you.

Some of the services installed by this playbook require a MariaDB database. Enabling the MariaDB database service will automatically wire all other services which require such a database to use it.

For details about configuring the [Ansible role for MariaDB](https://github.com/mother-of-all-self-hosting/ansible-role-mariadb), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-mariadb/blob/main/docs/configuring-mariadb.md) online
- 📁 `roles/galaxy/mariadb/docs/configuring-mariadb.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# mariadb                                                              #
#                                                                      #
########################################################################

mariadb_enabled: true

# Put a strong password below, generated with `pwgen -s 64 1` or in another way
mariadb_root_password: ''

########################################################################
#                                                                      #
# /mariadb                                                             #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the MariaDB instance becomes available.

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-mariadb/blob/main/docs/configuring-mariadb.md#usage) on the role's documentation for details about how to use it, such as upgrading MariaDB and backing up its database.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-mariadb/blob/main/docs/configuring-mariadb.md#troubleshooting) on the role's documentation for details.
