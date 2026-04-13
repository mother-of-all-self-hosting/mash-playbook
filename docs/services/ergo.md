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
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Ergo

The playbook can install and configure [Ergo](https://ergo.chat) for you.

Ergo is a modern IRCd (IRC server software) written in Go.

See the project's [documentation](https://ergo.chat/about) to learn what Ergo does and why it might be useful to you.

For details about configuring the [Ansible role for Ergo](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az2CSxS3YLtJYM87TyGZkZCan3uoSJ), you can check them via:
- 🌐 [the role's documentation](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az2CSxS3YLtJYM87TyGZkZCan3uoSJ/tree/docs/configuring-ergo.md) online
- 📁 `roles/galaxy/ergo/docs/configuring-ergo.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- (optional) [Postgres](postgres.md) / MySQL / [MariaDB](mariadb.md) / [SQLite](https://www.sqlite.org/) database — for persistent message history
- (optional) [Traefik](traefik.md) reverse-proxy server — required on the default configuration

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# ergo                                                                 #
#                                                                      #
########################################################################

ergo_enabled: true

ergo_hostname: ergo.example.com

########################################################################
#                                                                      #
# /ergo                                                                #
#                                                                      #
########################################################################
```

### Set the network's name

It is also necessary to specify to the `ergo_config_network_name` variable the name of the network in a human-readable name that identifies your network.

### Setting passwords for the server and operators (optional)

By default the server is not protected with a shared "server password" (`PASS`), and anyone can use it. For the IRC operators ("oper", "ircop") the role specifies the random password which should be replaced with yours.

See [the role's documentation](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az2CSxS3YLtJYM87TyGZkZCan3uoSJ/tree/docs/configuring-ergo.md#setting-server-39-s-password) for details about how to configure those passwords.

### Enabling permanent message storage (optional)

Ergo supports storing messages in a MySQL-compatible database, Postgres, or SQLite. This playbook is configured to use MariaDB by default. Refer to [this page](mariadb.md) for the instruction to set up a MariaDB instance.

After installing it, add the following configuration to your `vars.yml` file:

```yaml
# Enable storing messages in a persistent database for later playback
ergo_config_history_persistent_enabled: true
```

## Usage

After running the command for installation, the Ergo instance becomes available at the URL specified with `ergo_hostname`. With the configuration above, the service is hosted at `ircs://ergo.example.com:6697`.

Before logging in to the server with your IRC client, you might want to have a look at [`USERGUIDE.md`](https://github.com/ergochat/ergo/blob/stable/docs/USERGUIDE.md#introduction) for general information (what IRC is, how you can use the server with an IRC client, etc.)

## Troubleshooting

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az2CSxS3YLtJYM87TyGZkZCan3uoSJ/tree/docs/configuring-ergo.md#troubleshooting) on the role's documentation for details.

## Related services

- [InspIRCd](inspircd.md) —  Modular IRC server written in C++
- [The Lounge](thelounge.md) — Web IRC client with modern features, which keeps a persistent connection to IRC servers
