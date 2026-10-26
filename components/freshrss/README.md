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
SPDX-FileCopyrightText: 2023 Alejandro AR
SPDX-FileCopyrightText: 2023 Antonis Christofides
SPDX-FileCopyrightText: 2023 Felix Stupp
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 Thomas Miceli
SPDX-FileCopyrightText: 2024 kinduff
SPDX-FileCopyrightText: 2024, 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# FreshRSS

The playbook can install and configure [FreshRSS](https://freshrss.org) for you.

FreshRSS is a self-hosted RSS and Atom feed aggregator, which is lightweight, easy to work with, powerful, and customizable.

See the project's [documentation](https://freshrss.github.io/FreshRSS/) to learn what FreshRSS does and why it might be useful to you.

## Dependencies

This service requires the following other services:

- [Traefik](../traefik/README.md) reverse-proxy server
- [Postgres](../postgres/README.md) / MySQL / [MariaDB](../mariadb/README.md) / [SQLite](https://www.sqlite.org/) database

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../../docs/installing.md) process:

```yaml
########################################################################
#                                                                      #
# freshrss                                                             #
#                                                                      #
########################################################################

freshrss_enabled: true

freshrss_hostname: freshrss.example.com

########################################################################
#                                                                      #
# /freshrss                                                            #
#                                                                      #
########################################################################
```

**Note**: hosting FreshRSS under a subpath (by configuring the `freshrss_path_prefix` variable) does not seem to be possible due to FreshRSS's technical limitations. Refer to [this issue](https://github.com/mother-of-all-self-hosting/mash-playbook/issues/116) for details.

### Select database to use

FreshRSS can use a MySQL compatible database, Postgres, or SQLite, and you need to choose one. Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-freshrss/blob/main/docs/configuring-freshrss.md#specify-database) on the role's documentation for details.

## Usage

After running the command for installation, the FreshRSS instance becomes available at the URL specified with `freshrss_hostname`. With the configuration above, the service is hosted at `https://freshrss.example.com`.

To get started, open the URL with a web browser, and follow the set up wizard. On the wizard, it is required to input database credentials to use a MySQL compatible database or Postgres. You can output its credentials by running the playbook as below:

```sh
ansible-playbook -i inventory/hosts setup.yml --tags=print-freshrss-db-credentials
```

Refer to FreshRSS [official documentation](http://freshrss.github.io/FreshRSS/en/) for usage.

## Related services

- [Miniflux](../miniflux/README.md) — Minimalist and opinionated feed reader
