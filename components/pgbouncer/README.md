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
SPDX-FileCopyrightText: 2024 Thomas Miceli
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# PgBouncer

The playbook can install and configure [PgBouncer](https://www.pgbouncer.org/) for you.

PgBouncer is a PostgreSQL connection pooler. Any target application can be connected to PgBouncer as if it were a PostgreSQL server, and PgBouncer will create a connection to the actual server, or it will reuse one of its existing connections.

See the project's [documentation](https://www.pgbouncer.org/usage.html) to learn what PgBouncer does and why it might be useful to you.

For details about configuring the [Ansible role for PgBouncer](https://github.com/mother-of-all-self-hosting/ansible-role-pgbouncer), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-pgbouncer/blob/main/docs/configuring-pgbouncer.md) online
- 📁 `roles/galaxy/pgbouncer/docs/configuring-pgbouncer.md` locally, if you have [fetched the Ansible roles](../../docs/installing.md)

## Dependencies

This service requires the following other services:

- [Postgres](../postgres/README.md) database

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../../docs/installing.md) process:

```yaml
########################################################################
#                                                                      #
# pgbouncer                                                            #
#                                                                      #
########################################################################

pgbouncer_enabled: true

########################################################################
#                                                                      #
# /pgbouncer                                                           #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the PgBouncer instance becomes available.

Since the PgBouncer instance is not (yet) wired to the services on the playbook by default (except Postgres), it is necessary to add configurations manually to use it by overriding the default values specified on each service's `with/postgres.yml` file.

To have a service connect to the PgBouncer instance via the Unix socket, add the following configuration to your `vars.yml` file:

```yaml
YOUR-SERVICE_database_socket_path_host: "{{ pgbouncer_run_path }}"
```

If the service does not support connecting to the Postgres database via the Unix socket, add the following configuration to your `vars.yml` file:

```yaml
YOUR-SERVICE_database_hostname: "{{ pgbouncer_connection_hostname }}"
YOUR-SERVICE_database_port: "{{ pgbouncer_connection_port }}"
YOUR-SERVICE_container_additional_networks_custom:
  - "{{ pgbouncer_container_network }}"
```

>[!NOTE]
>
> - If the service supports multiple database drivers (e.g., Postgres and SQLite), the variables for Postgres are usually specified by following the `YOUR-SERVICE_database_postgres_*` pattern. Refer to each service's `with/postgres.yml` file for exact values.
> - There may be services which are not fully compatible with PgBouncer. Please report to us if you find such ones.

## Troubleshooting

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-pgbouncer/blob/main/docs/configuring-pgbouncer.md#troubleshooting) on the role's documentation for details.
