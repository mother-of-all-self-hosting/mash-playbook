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

# CodiMD

The playbook can install and configure [CodiMD](https://codimd.org/) for you.

CodiMD is web-based free software for farm management, planning, and record keeping. It is developed by a community of farmers, developers, researchers, and organizations.

See the project's [documentation](https://codimd.org/guide/) to learn what CodiMD does and why it might be useful to you.

For details about configuring the [Ansible role for CodiMD](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az2H8vYeXaYHLzV3jXH1YjVwhuzTsk), you can check them via:
- 🌐 [the role's documentation](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az2H8vYeXaYHLzV3jXH1YjVwhuzTsk/tree/docs/configuring-codimd.md) online
- 📁 `roles/galaxy/codimd/docs/configuring-codimd.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Postgres](postgres.md) / MySQL / [MariaDB](mariadb.md) / [SQLite](https://www.sqlite.org/) database
- [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# codimd                                                               #
#                                                                      #
########################################################################

codimd_enabled: true

codimd_hostname: codimd.example.com

########################################################################
#                                                                      #
# /codimd                                                              #
#                                                                      #
########################################################################
```

**Note**: hosting CodiMD under a subpath (by configuring the `codimd_path_prefix` variable) does not seem to be possible due to CodiMD's technical limitations.

>[!WARNING]
> Once the hostname is set, it cannot be changed easily as it involves adjusting configuration files.

### Select database to use

It is necessary to select a database used by CodiMD from a MySQL compatible database, Postgres, and SQLite. See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az2H8vYeXaYHLzV3jXH1YjVwhuzTsk/tree/docs/configuring-codimd.md#specify-database) on the role's documentation for details.

## Usage

After running the command for installation, the CodiMD instance becomes available at the URL specified with `codimd_hostname`. With the configuration above, the service is hosted at `https://codimd.example.com`.

To get started, open the URL with a web browser, and follow the set up wizard.

On the set up wizard, it is required to input database credentials to use a MySQL compatible database or Postgres. See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az2H8vYeXaYHLzV3jXH1YjVwhuzTsk/tree/docs/configuring-codimd.md#outputting-database-credentials) on the role's documentation for details about how to check them.

## Troubleshooting

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az2H8vYeXaYHLzV3jXH1YjVwhuzTsk/tree/docs/configuring-codimd.md#troubleshooting) on the role's documentation for details.
