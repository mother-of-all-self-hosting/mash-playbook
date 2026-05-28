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

# CiviCRM

The playbook can install and configure [CiviCRM](https://civicrm.org/) for you.

CiviCRM is a relationship management system designed to meet the needs of advocacy, non-profit and non-governmental groups.

See the project's [documentation](https://docs.civicrm.org) to learn what CiviCRM does and why it might be useful to you.

For details about configuring the [Ansible role for CiviCRM](https://radicle.network/nodes/iris.radicle.network/rad%3Az2kX5GbCKBFjiunvLKThDXLzbYnw1), you can check them via:

- 🌐 [the role's documentation](https://radicle.network/nodes/iris.radicle.network/rad%3Az2kX5GbCKBFjiunvLKThDXLzbYnw1/tree/docs/configuring-civicrm.md) online
- 📁 `roles/galaxy/civicrm/docs/configuring-civicrm.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- MySQL / [MariaDB](mariadb.md) database
- [Traefik](traefik.md) reverse-proxy server
- (optional) [exim-relay](exim-relay.md) mailer

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# civicrm                                                              #
#                                                                      #
########################################################################

civicrm_enabled: true

civicrm_hostname: civicrm.example.com

########################################################################
#                                                                      #
# /civicrm                                                             #
#                                                                      #
########################################################################
```

### Enable MariaDB

CiviCRM requires a MySQL-compatible database to work. This playbook supports MariaDB, and you can set up a MariaDB instance by enabling it on `vars.yml`.

Refer to [this page](mariadb.md) for the instruction to enable it.

## Usage

After running the command for installation, the CiviCRM instance becomes available at the URL specified with `civicrm_hostname`. With the configuration above, the service is hosted at `https://civicrm.example.com`.

To get started, open the URL with a web browser, and follow the set up wizard.

On the set up wizard, it is required to input database credentials. See [this section](https://radicle.network/nodes/iris.radicle.network/rad%3Az2kX5GbCKBFjiunvLKThDXLzbYnw1/tree/docs/configuring-civicrm.md#outputting-database-credentials) on the role's documentation for details about how to check them.

## Troubleshooting

See [this section](https://radicle.network/nodes/iris.radicle.network/rad%3Az2kX5GbCKBFjiunvLKThDXLzbYnw1/tree/docs/configuring-civicrm.md#troubleshooting) on the role's documentation for details.
