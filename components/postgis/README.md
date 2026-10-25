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

# PostGIS

The playbook can install and configure [Postgres with PostGIS extensions installed](https://github.com/postgis/docker-postgis) for you.

[PostGIS](https://postgis.net/) is a spatial database extender for PostgreSQL object-relational database. It adds support for storing, indexing, and querying geospatial data.

See the project's [documentation](https://postgis.net/documentation/) to learn what PostGIS does and why it might be useful to you.

Some of the services installed by this playbook require a Postgres database with PostGIS extensions installed. Enabling the service will automatically wire all other services which require such a database to use it.

For details about configuring the [Ansible role for Postgres with PostGIS extensions installed](https://github.com/mother-of-all-self-hosting/ansible-role-postgis), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-postgis/blob/main/docs/configuring-postgis.md) online
- 📁 `roles/galaxy/postgis/docs/configuring-postgis.md` locally, if you have [fetched the Ansible roles](../../docs/installing.md)

>[!NOTE]
>
> - Upgrading the Postgres instance with PostGIS extensions installed to a new major version is currently tested and not yet available.
> - The database is not configured to be backed up with BorgBackup. Please make sure to set it up manually if needed.

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../../docs/installing.md) process:

```yaml
########################################################################
#                                                                      #
# postgis                                                              #
#                                                                      #
########################################################################

postgis_enabled: true

# Put a strong password below, generated with `pwgen -s 64 1` or in another way
postgis_connection_password: ''

########################################################################
#                                                                      #
# /postgis                                                             #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the Postgres instance with PostGIS extensions installed becomes available.

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-postgis/blob/main/docs/configuring-postgis.md#maintenance) on the role's documentation for details about how to conduct maintenance tasks, such as upgrading PostgreSQL and backing up its database.

## Troubleshooting

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-postgis/blob/main/docs/configuring-postgis.md#troubleshooting) on the role's documentation for details.

## Related services

- [Postgres](../postgres/README.md) — Powerful object-relational database system
