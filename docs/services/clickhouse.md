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

# ClickHouse

The playbook can install and configure [ClickHouse](https://clickhouse.com/) for you.

ClickHouse is an open-source column-oriented DBMS for online analytical processing (OLAP) that allows users to generate analytical reports using SQL queries in real-time.

See the project's [documentation](https://clickhouse.com/docs) to learn what ClickHouse does and why it might be useful to you.

For details about configuring the [Ansible role for ClickHouse](https://github.com/mother-of-all-self-hosting/ansible-role-clickhouse), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-clickhouse/blob/main/docs/configuring-clickhouse.md) online
- 📁 `roles/galaxy/clickhouse/docs/configuring-clickhouse.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# clickhouse                                                           #
#                                                                      #
########################################################################

clickhouse_enabled: true

# Put a strong password below, generated with `pwgen -s 64 1` or in another way
clickhouse_root_password: ''

########################################################################
#                                                                      #
# /clickhouse                                                          #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the Clickhouse instance becomes available.

Some of the services installed by this playbook like [Plausible Analytics](plausible.md) require a ClickHouse database. Enabling the ClickHouse database service will automatically wire all other services which require such a database to use it.

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-clickhouse/blob/main/docs/configuring-clickhouse.md#usage) for details about how to use it (backing up the database, etc).

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-clickhouse/blob/main/docs/configuring-clickhouse.md#troubleshooting) on the role's documentation for details.
