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

# SQLPage

The playbook can install and configure [SQLPage](https://sql-page.com/) for you.

SQLPage is a web server written in Rust which works as a SQL-only data application builder.

See the project's [documentation](https://sql-page.com/documentation.sql) to learn what SQLPage does and why it might be useful to you.

For details about configuring the [Ansible role for SQLPage](https://radicle.network/nodes/iris.radicle.network/rad:z2eyt9uovdZtjh8TL5qiyv2PqAYvP), you can check them via:

- 🌐 [the role's documentation](https://radicle.network/nodes/iris.radicle.network/rad:z2eyt9uovdZtjh8TL5qiyv2PqAYvP/tree/docs/configuring-sqlpage.md) online
- 📁 `roles/galaxy/sqlpage/docs/configuring-sqlpage.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# sqlpage                                                              #
#                                                                      #
########################################################################

sqlpage_enabled: true

sqlpage_hostname: sqlpage.example.com

########################################################################
#                                                                      #
# /sqlpage                                                             #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the SQLPage instance becomes available at the URL specified with `sqlpage_hostname`. With the configuration above, the service is hosted at `https://sqlpage.example.com`.

Refer to [this page](https://sql-page.com/your-first-sql-website/) on the official documentation for details about how to create a website. By default the files to be served should be put in the directory specified with `sqlpage_data_path`.

## Troubleshooting

See [this section](https://radicle.network/nodes/iris.radicle.network/rad:z2eyt9uovdZtjh8TL5qiyv2PqAYvP/tree/docs/configuring-sqlpage.md#troubleshooting) on the role's documentation for details.
