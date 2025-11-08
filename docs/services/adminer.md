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

# Adminer

The playbook can install and configure [Adminer](https://www.adminer.org/) for you.

Adminer is a full-featured database management tool written in PHP. It supports MySQL, MariaDB, PostgreSQL, CockroachDB, SQLite, MS SQL, and Oracle out of the box. Elasticsearch, SimpleDB, MongoDB, Firebird, and Clickhouse can be supported via plugins.

See the project's [documentation](https://github.com/vrana/adminer/blob/master/README.md) to learn what Adminer does and why it might be useful to you.

For details about configuring the [Ansible role for Adminer](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az3px8gLDo2opjQZW7qFiLoNuk4eSu), you can check them via:
- 🌐 [the role's documentation](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az3px8gLDo2opjQZW7qFiLoNuk4eSu/tree/docs/configuring-adminer.md) online
- 📁 `roles/galaxy/adminer/docs/configuring-adminer.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# adminer                                                              #
#                                                                      #
########################################################################

adminer_enabled: true

adminer_hostname: adminer.example.com

########################################################################
#                                                                      #
# /adminer                                                             #
#                                                                      #
########################################################################
```

It is optionally possible to edit settings about the default server to connect, plugins to load (ones for loading databases), etc. See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az3px8gLDo2opjQZW7qFiLoNuk4eSu/tree/docs/configuring-adminer.md#adjusting-the-playbook-configuration) for details.

## Usage

After running the command for installation, the Adminer instance becomes available at the URL specified with `adminer_hostname`. With the configuration above, the service is hosted at `https://adminer.example.com`.

To get started, open the URL `https://adminer.example.com` with a web browser, and log in to the instance with the database's credentials specified on your `vars.yml` file.

To log in to database servers which this playbook manages, you need to specify its `*_identifier` to the `server` input area. For example, the default value for the MariaDB server is `mash-mariadb` and the one for the Postgres server is `mash-postgres`, respectively.

>[!NOTE]
> Since enabling Adminer with this playbook exposes the instance (thus practically the databases as well) to the internet, it is important to set a proper method to restrict who can access to it. See [this section](https://www.adminer.org/en/#requirements) on the project website for security recommendations.

## Troubleshooting

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az3px8gLDo2opjQZW7qFiLoNuk4eSu/tree/docs/configuring-adminer.md#troubleshooting) on the role's documentation for details.

## Related services

- [MariaDB](mariadb.md) — Powerful, open source object-relational database system
