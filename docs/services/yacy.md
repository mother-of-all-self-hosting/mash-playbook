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

# YaCy

The playbook can install and configure [YaCy](https://yacy.net) for you.

YaCy is a distributed web search engine, based on a peer-to-peer network. It provides three different modes;

- Searching a shared global index on the P2P network
- Crawling web pages of domains you choose to create an individual index for searching
- Setting up a search portal for your intranet behind the firewall to search pages or files on the shared file system, without sharing data with a third party

See the project's [documentation](https://yacy.net/docs/) to learn what YaCy does and why it might be useful to you.

For details about configuring the [Ansible role for YaCy](https://github.com/mother-of-all-self-hosting/ansible-role-yacy), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-yacy/blob/main/docs/configuring-yacy.md) online
- 📁 `roles/galaxy/yacy/docs/configuring-yacy.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Prerequisites

You may need to open some ports to your server, if you use another firewall in front of the server. Refer to [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-yacy/blob/main/docs/configuring-yacy.md#prerequisites) to check which ones to be configured.

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# yacy                                                                 #
#                                                                      #
########################################################################

yacy_enabled: true

yacy_hostname: mash.example.com
yacy_path_prefix: /yacy

########################################################################
#                                                                      #
# /yacy                                                                #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, YaCy becomes available at the specified hostname like `https://mash.example.com/yacy`.

You can log in to the instance with the default login credential of the admin account (username: `admin`, password: `yacy`).

To improve security regarding the default login credential, **the role configures the instance on the intranet search mode by default**, so that it does not broadcast its existence to peers before you change the login credential.

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-yacy/blob/main/docs/configuring-yacy.md#usage) on the role's documentation for details about changing the admin user password and search mode, including protecting the instance with the password.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-yacy/blob/main/docs/configuring-yacy.md#troubleshooting) on the role's documentation for details.
