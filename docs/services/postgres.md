<!--
SPDX-FileCopyrightText: 2019-2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2020 Chris van Dijk
SPDX-FileCopyrightText: 2020 Dominik Zajac
SPDX-FileCopyrightText: 2020 Hardy Erlinger
SPDX-FileCopyrightText: 2020 Mickaël Cornière
SPDX-FileCopyrightText: 2020, 2021 Aaron Raimist
SPDX-FileCopyrightText: 2020-2024 MDAD project contributors
SPDX-FileCopyrightText: 2021 Marc Leuser
SPDX-FileCopyrightText: 2022 François Darveau
SPDX-FileCopyrightText: 2022 Julian Foad
SPDX-FileCopyrightText: 2022 Warren Bailey
SPDX-FileCopyrightText: 2023 Antonis Christofides
SPDX-FileCopyrightText: 2023 Felix Stupp
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 Kim Brose
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Postgres

The playbook can install and configure [PostgreSQL](https://www.postgresql.org) for you.

PostgreSQL is a powerful, open-source object-relational database system with over 35 years of active development that has earned it a strong reputation for reliability, feature robustness, and performance.

See the project's [documentation](https://www.postgresql.org/docs/) to learn what PostgreSQL does and why it might be useful to you.

Many of the services installed by this playbook require a Postgres database. Enabling the Postgres database service will automatically wire all other services which require such a database to use it.

For details about configuring the [Ansible role for PostgreSQL](https://github.com/mother-of-all-self-hosting/ansible-role-postgres), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-postgres/blob/main/docs/configuring-postgres.md) online
- 📁 `roles/galaxy/postgres/docs/configuring-postgres.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# postgres                                                             #
#                                                                      #
########################################################################

postgres_enabled: true

# Put a strong password below, generated with `pwgen -s 64 1` or in another way
postgres_connection_password: ''

########################################################################
#                                                                      #
# /postgres                                                            #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the PostgreSQL instance becomes available.

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-postgres/blob/main/docs/configuring-postgres.md#maintenance) on the role's documentation for details about how to conduct maintenance tasks, such as upgrading PostgreSQL and backing up its database.

## Troubleshooting

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-postgres/blob/main/docs/configuring-postgres.md#troubleshooting) on the role's documentation for details.

## Related services

- [Adminer](adminer.md) — Full-featured database management tool written in PHP
- [pgAdmin](pgadmin.md) — Management tool for Postgres with a graphical interface
- [PostGIS](postgis.md) — Spatial database extender for PostgreSQL
- [Postgres Backup](postgres-backup.md) for backing up your Postgres database
- [Prometheus](prometheus.md), [prometheus-postgres-exporter](prometheus-postgres-exporter.md) and [Grafana](grafana.md) for monitoring your Postgres database
