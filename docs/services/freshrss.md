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
SPDX-FileCopyrightText: 2023 Alejandro AR
SPDX-FileCopyrightText: 2023 Antonis Christofides
SPDX-FileCopyrightText: 2023 Felix Stupp
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara
SPDX-FileCopyrightText: 2024 Thomas Miceli

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# FreshRSS

The playbook can install and configure [FreshRSS](https://freshrss.org) for you.

FreshRSS is a self-hosted RSS and Atom feed aggregator, which is lightweight, easy to work with, powerful, and customizable.

See the project's [documentation](https://freshrss.github.io/FreshRSS/) to learn what FreshRSS does and why it might be useful to you.

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server
- [Postgres](postgres.md) / MySQL / [MariaDB](mariadb.md) / [SQLite](https://www.sqlite.org/) database

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

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

**Note**: hosting FreshRSS under a subpath (by configuring the `freshrss_path_prefix` variable) does not seem to be possible due to FreshRSS's technical limitations. See [this issue](https://github.com/mother-of-all-self-hosting/mash-playbook/issues/116) for details.

### Specify database

It is necessary to select database used by FreshRSS from a MySQL compatible database, Postgres, and SQLite.

To use Postgres, add the following configuration to your `vars.yml` file:

```yaml
freshrss_database_type: postgres
```

Set `mysql` to use a MySQL compatible database, and `sqlite` to use SQLite. The SQLite database is stored in the directory specified with `freshrss_data_path`.

## Usage

After running the command for installation, the FreshRSS instance becomes available at the URL specified with `freshrss_hostname`. With the configuration above, the service is hosted at `https://freshrss.example.com`.

To get started, open the URL with a web browser, and follow the set up wizard. On the wizard, it is required to input database credentials to use a MySQL compatible database or Postgres. You can output its credentials by running the playbook as below:

```sh
ansible-playbook -i inventory/hosts setup.yml --tags=print-freshrss-db-credentials
```

Refer to FreshRSS [official documentation](http://freshrss.github.io/FreshRSS/en/) for usage.

## Related services

- [Miniflux](miniflux.md) — Minimalist and opinionated feed reader
