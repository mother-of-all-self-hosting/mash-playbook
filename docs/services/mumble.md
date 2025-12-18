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
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Mumble

The playbook can install and configure [Mumble](https://mumble.chat) for you.

Mumble is a modern IRCd (IRC server software) written in Go.

See the project's [documentation](https://mumble.chat/about) to learn what Mumble does and why it might be useful to you.

For details about configuring the [Ansible role for Mumble](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az2CSxS3YLtJYM87TyGZkZCan3uoSJ), you can check them via:
- 🌐 [the role's documentation](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az2CSxS3YLtJYM87TyGZkZCan3uoSJ/tree/docs/configuring-mumble.md) online
- 📁 `roles/galaxy/mumble/docs/configuring-mumble.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- (optional) MySQL / [MariaDB](mariadb.md) database — for persistent message history
- (optional) [Traefik](traefik.md) reverse-proxy server — required on the default configuration

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# mumble                                                               #
#                                                                      #
########################################################################

mumble_enabled: true

mumble_hostname: mumble.example.com

########################################################################
#                                                                      #
# /mumble                                                              #
#                                                                      #
########################################################################
```

### Set the network's name

It is also necessary to specify to the `mumble_config_network_name` variable the name of the network in a human-readable name that identifies your network.

### Setting passwords for the server and operators (optional)

By default the server is not protected with a shared "server password" (`PASS`), and anyone can use it. For the IRC operators ("oper", "ircop") the role specifies the random password which should be replaced with yours.

See [the role's documentation](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az2CSxS3YLtJYM87TyGZkZCan3uoSJ/tree/docs/configuring-mumble.md#setting-server-39-s-password) for details about how to configure those passwords.

### Enabling message storage on MariaDB database (optional)

Mumble supports storing messages in a persistent storage. Currently a MySQL-compatible database is supported for it. This playbook supports MariaDB, and you can set up a MariaDB instance by enabling it on `vars.yml`. Refer to [this page](mariadb.md) for the instruction to enable it.

After installing it, add the following configuration to your `vars.yml` file:

```yaml
# Enable storing messages in a persistent database for later playback
mumble_config_history_persistent_enabled: true
```

## Usage

After running the command for installation, the Mumble instance becomes available at the URL specified with `mumble_hostname`. With the configuration above, the service is hosted at `ircs://mumble.example.com:6697`.

Before logging in to the server with your IRC client, you might want to have a look at [`USERGUIDE.md`](https://github.com/mumblechat/mumble/blob/stable/docs/USERGUIDE.md#introduction) for general information (what IRC is, how you can use the server with an IRC client, etc.)

## Troubleshooting

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az2CSxS3YLtJYM87TyGZkZCan3uoSJ/tree/docs/configuring-mumble.md#troubleshooting) on the role's documentation for details.

## Related services

- [InspIRCd](inspircd.md) —  Modular IRC server written in C++
- [The Lounge](thelounge.md) — Web IRC client with modern features, which keeps a persistent connection to IRC servers
