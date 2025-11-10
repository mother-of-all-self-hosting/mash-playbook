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

# pgAdmin

The playbook can install and configure [pgAdmin](https://www.pgadmin.net/) for you.

pgAdmin is a free software tool written in PHP that is intended to handle the administration of a MySQL or MariaDB database server.

See the project's [documentation](https://docs.pgadmin.net/en/latest/) to learn what pgAdmin does and why it might be useful to you.

For details about configuring the [Ansible role for pgAdmin](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Azby9EmMBhyNe8Nj4f66izwrmhk5g), you can check them via:
- 🌐 [the role's documentation](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Azby9EmMBhyNe8Nj4f66izwrmhk5g/tree/docs/configuring-pgadmin.md) online
- 📁 `roles/galaxy/pgadmin/docs/configuring-pgadmin.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# pgadmin                                                              #
#                                                                      #
########################################################################

pgadmin_enabled: true

pgadmin_hostname: pgadmin.example.com

########################################################################
#                                                                      #
# /pgadmin                                                             #
#                                                                      #
########################################################################
```

**Note**: hosting pgAdmin under a subpath (by configuring the `pgadmin_path_prefix` variable) does not seem to be possible due to pgAdmin's technical limitations.

### Enabling to specify the database server to connect (optional)

The default setting is that the pgAdmin can connect to the [MariaDB](mariadb.md) instance managed with this playbook only. To allow the pgAdmin instance to connect to any MySQL / MariaDB server, add the following configuration to your `vars.yml` file:

```yaml
pgadmin_environment_variables_pma_arbitrary: "1"
```

## Usage

After running the command for installation, the pgAdmin instance becomes available at the URL specified with `pgadmin_hostname`. With the configuration above, the service is hosted at `https://pgadmin.example.com`.

To get started, open the URL `https://pgadmin.example.com` with a web browser, and log in to the instance with the database's credentials. By default its username is `root`, and the password is the one specified to `mariadb_root_password` on your `vars.yml` file.

>[!NOTE]
>
> - As some commands are destructive and cannot be undone, it is **highly recommended** to have a look at the [documentation](https://docs.pgadmin.net/en/latest/) to learn its usage before running them against the actual database.
> - Since enabling pgAdmin with this playbook exposes the instance (thus practically the MariaDB database as well) to the internet, it is important to set a proper method to restrict who can access to it, such as [two-factor authentication](https://docs.pgadmin.net/en/latest/two_factor.html). Protecting it with an Identity Provider (IdP) like [authentik](authentik.md) is also worth considering.

## Troubleshooting

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Azby9EmMBhyNe8Nj4f66izwrmhk5g/tree/docs/configuring-pgadmin.md#troubleshooting) on the role's documentation for details.

## Related services

- [Adminer](adminer.md) — Full-featured database management tool written in PHP
- [MariaDB](mariadb.md) — Powerful, open source object-relational database system
