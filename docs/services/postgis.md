<!--
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Postgis

[Postgis](https://postgis.net/) is a spatial database extender for PostgreSQL object-relational database. It adds support for geographic objects allowing location queries to be run in SQL.

Services like [Mobilizon](./mobilizon.md) depend on the ability to store gespatial data.
Enabling the PPostgisostgres database service will automatically wire these services to use it.


## Configuration

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
