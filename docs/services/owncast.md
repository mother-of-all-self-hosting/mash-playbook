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
SPDX-FileCopyrightText: 2024 MASH project contributors
SPDX-FileCopyrightText: 2024 Sergio Durigan Junior

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Owncast

The playbook can install and configure [Owncast](https://owncast.online) for you.

Owncast is a free and open source live video and web chat server for use with existing popular broadcasting software.

See the project's [documentation](https://owncast.online/docs/) to learn what Owncast does and why it might be useful to you.

For details about configuring the [Ansible role for Owncast](https://github.com/mother-of-all-self-hosting/ansible-role-owncast), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-owncast/blob/main/docs/configuring-owncast.md) online
- 📁 `roles/galaxy/owncast/docs/configuring-owncast.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Prerequisites

### Open a port

You may need to open a port for TCP based [RTMP](https://en.wikipedia.org/wiki/Real-Time_Messaging_Protocol) on your server. See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-owncast/blob/main/docs/configuring-owncast.md#open-a-port) on the role's documentation for details.

## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# owncast                                                              #
#                                                                      #
########################################################################

owncast_enabled: true

owncast_hostname: owncast.example.com

########################################################################
#                                                                      #
# /owncast                                                             #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the Owncast instance becomes available at the URL specified with `owncast_hostname`. With the configuration above, the service is hosted at `https://owncast.example.com`.

To get started, open the URL `https://owncast.example.com/admin` with a web browser.

>[!NOTE]
> Change the default stream key set to `abc123` as soon as possible.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-owncast/blob/main/docs/configuring-owncast.md#troubleshooting) on the role's documentation for details.
