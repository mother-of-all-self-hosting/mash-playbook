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
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# PostGIS

The playbook can install and configure [Postgres with PostGIS extensions installed](https://github.com/postgis/docker-postgis) for you.

[PostGIS](https://postgis.net/) is a spatial database extender for PostgreSQL object-relational database. It adds support for storing, indexing, and querying geospatial data.

See the project's [documentation](https://postgis.net/documentation/) to learn what PostGIS does and why it might be useful to you.

Some of the services installed by this playbook require a Postgres database with PostGIS extensions installed. Enabling the service will automatically wire all other services which require such a database to use it.

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

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

## Related services

- [Postgres](postgres.md) — Powerful object-relational database system
