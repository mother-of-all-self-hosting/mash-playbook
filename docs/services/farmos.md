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

# farmOS

The playbook can install and configure [farmOS](https://farmos.net) for you.

farmOS is a simple server for sending and receiving messages.

See the project's [documentation](https://farmos.net/docs/) to learn what farmOS does and why it might be useful to you.

For details about configuring the [Ansible role for farmOS](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az3dQNNLitS9sByxZ83ivu5qg6qR4N), you can check them via:
- 🌐 [the role's documentation](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az3dQNNLitS9sByxZ83ivu5qg6qR4N/tree/docs/configuring-farmos.md) online
- 📁 `roles/galaxy/farmos/docs/configuring-farmos.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Postgres](postgres.md) / MySQL / [MariaDB](mariadb.md) / [SQLite](https://www.sqlite.org/) database
- [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# farmos                                                               #
#                                                                      #
########################################################################

farmos_enabled: true

farmos_hostname: farmos.example.com

########################################################################
#                                                                      #
# /farmos                                                              #
#                                                                      #
########################################################################
```

**Note**: hosting farmOS under a subpath (by configuring the `farmos_path_prefix` variable) does not seem to be possible due to farmOS's technical limitations.

### Select database to use

It is necessary to select a database used by farmOS from a MySQL compatible database, Postgres, and SQLite. See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az3dQNNLitS9sByxZ83ivu5qg6qR4N/tree/docs/configuring-farmos.md#specify-database) on the role's documentation for details.

### Set the username and password for the first user

You also need to set an initial username and password for the first user. Refer to [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az3dQNNLitS9sByxZ83ivu5qg6qR4N/tree/docs/configuring-farmos.md#specify-username-and-password-for-the-first-user) on the role's documentation.

## Usage

After running the command for installation, the farmOS instance becomes available at the URL specified with `farmos_hostname`. With the configuration above, the service is hosted at `https://farmos.example.com`.

To get started, open the URL with a web browser to log in to the instance. **Note that the first registered user becomes an administrator automatically.**

## Troubleshooting

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az3dQNNLitS9sByxZ83ivu5qg6qR4N/tree/docs/configuring-farmos.md#troubleshooting) on the role's documentation for details.

## Related services

- [Apprise API](apprise.md) — Lightweight REST framework that wraps the [Apprise](https://github.com/caronc/apprise) Notification Library
- [ntfy](ntfy.md) — Simple HTTP-based pub-sub notification service to send you push notifications from any computer
