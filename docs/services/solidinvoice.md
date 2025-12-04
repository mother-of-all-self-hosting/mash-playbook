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

# SolidInvoice

The playbook can install and configure [SolidInvoice](https://solidinvoice.org/) for you.

SolidInvoice is web-based free software for farm management, planning, and record keeping. It is developed by a community of farmers, developers, researchers, and organizations.

See the project's [documentation](https://solidinvoice.org/guide/) to learn what SolidInvoice does and why it might be useful to you.

For details about configuring the [Ansible role for SolidInvoice](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az2H8vYeXaYHLzV3jXH1YjVwhuzTsk), you can check them via:
- 🌐 [the role's documentation](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az2H8vYeXaYHLzV3jXH1YjVwhuzTsk/tree/docs/configuring-solidinvoice.md) online
- 📁 `roles/galaxy/solidinvoice/docs/configuring-solidinvoice.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Postgres](postgres.md) / MySQL / [MariaDB](mariadb.md) / [SQLite](https://www.sqlite.org/) database
- [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# solidinvoice                                                         #
#                                                                      #
########################################################################

solidinvoice_enabled: true

solidinvoice_hostname: solidinvoice.example.com

########################################################################
#                                                                      #
# /solidinvoice                                                        #
#                                                                      #
########################################################################
```

**Note**: hosting SolidInvoice under a subpath (by configuring the `solidinvoice_path_prefix` variable) does not seem to be possible due to SolidInvoice's technical limitations.

>[!WARNING]
> Once the hostname is set, it cannot be changed easily as it involves adjusting configuration files.

### Select database to use

It is necessary to select a database used by SolidInvoice from a MySQL compatible database, Postgres, and SQLite. See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az2H8vYeXaYHLzV3jXH1YjVwhuzTsk/tree/docs/configuring-solidinvoice.md#specify-database) on the role's documentation for details.

## Usage

After running the command for installation, the SolidInvoice instance becomes available at the URL specified with `solidinvoice_hostname`. With the configuration above, the service is hosted at `https://solidinvoice.example.com`.

To get started, open the URL with a web browser, and follow the set up wizard.

On the set up wizard, it is required to input database credentials to use a MySQL compatible database or Postgres. See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az2H8vYeXaYHLzV3jXH1YjVwhuzTsk/tree/docs/configuring-solidinvoice.md#outputting-database-credentials) on the role's documentation for details about how to check them.

## Troubleshooting

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az2H8vYeXaYHLzV3jXH1YjVwhuzTsk/tree/docs/configuring-solidinvoice.md#troubleshooting) on the role's documentation for details.
