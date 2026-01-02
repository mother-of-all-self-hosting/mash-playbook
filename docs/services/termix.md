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

# Termix

The playbook can install and configure [Termix](https://termix.com/) for you.

Termix is free software for backing up database of PostgreSQL, MySQL, MariaDB, and MongoDB.

See the project's [documentation](https://termix.com/installation) to learn what Termix does and why it might be useful to you.

For details about configuring the [Ansible role for Termix](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3AzeQ4hXq2LkbADcndSsjesgq9kDPf), you can check them via:
- 🌐 [the role's documentation](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3AzeQ4hXq2LkbADcndSsjesgq9kDPf/tree/docs/configuring-termix.md) online
- 📁 `roles/galaxy/termix/docs/configuring-termix.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# termix                                                               #
#                                                                      #
########################################################################

termix_enabled: true

termix_hostname: termix.example.com

########################################################################
#                                                                      #
# /termix                                                              #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the Termix instance becomes available at the URL specified with `termix_hostname`. With the configuration above, the service is hosted at `https://termix.example.com`.

To get started, open the URL with a web browser to create an account. **Note that the first registered user becomes an administrator automatically.**

Since MariaDB, PostgreSQL, and MongoDB are wired to the service, it is possible to set `mash-mariadb`, `mash-postgres`, or `mash-mongodb` to the input area for the host when adding a database to back up.

## Troubleshooting

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3AzeQ4hXq2LkbADcndSsjesgq9kDPf/tree/docs/configuring-termix.md#troubleshooting) on the role's documentation for details.

## Related services

- [Postgres Backup](postgres-backup.md) — A solution for backing up PostgreSQL to local filesystem with periodic backups
