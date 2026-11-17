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

# ParadeDB

The playbook can install and configure [ParadeDB](https://www.paradedb.com) for you.

ParadeDB is a [PostgreSQL](https://www.postgresql.org) extension with a custom index for full-text and vector search, BM25 scoring, filters, facets, aggregations, and joins.

This service runs its own PostgreSQL server with ParadeDB's extension built in, separately from the [Postgres](../postgres/README.md) service. It does not add the extension to an existing Postgres instance.

See the project's [documentation](https://www.paradedb.com/docs/reference/overview) to learn what ParadeDB does and why it might be useful to you.

For details about configuring the [Ansible role for ParadeDB](https://github.com/mother-of-all-self-hosting/ansible-role-paradedb), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-paradedb/blob/main/docs/configuring-paradedb.md) online
- 📁 `roles/galaxy/paradedb/docs/configuring-paradedb.md` locally, if you have [fetched the Ansible roles](../../docs/installing.md)

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../../docs/installing.md) process:

```yaml
########################################################################
#                                                                      #
# paradedb                                                             #
#                                                                      #
########################################################################

paradedb_enabled: true

# Put a strong password below, generated with `pwgen -s 64 1` or in another way
paradedb_connection_password: ''

########################################################################
#                                                                      #
# /paradedb                                                            #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the ParadeDB instance becomes available.

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-paradedb/blob/main/docs/configuring-paradedb.md#maintenance) on the role's documentation for details about how to conduct maintenance tasks, such as upgrading ParadeDB and backing up its database.

## Troubleshooting

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-paradedb/blob/main/docs/configuring-paradedb.md#troubleshooting) on the role's documentation for details.
