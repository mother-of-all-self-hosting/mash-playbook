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

# Radicle node

The playbook can install and configure [Radicle node](https://radicle-node.net) for you.

Radicle node is a distributed web search engine, based on a peer-to-peer network. It provides three different modes;

- Searching a shared global index on the P2P network
- Crawling web pages of domains you choose to create an individual index for searching
- Setting up a search portal for your intranet behind the firewall to search pages or files on the shared file system, without sharing data with a third party

See the project's [documentation](https://radicle-node.net/docs/) to learn what Radicle node does and why it might be useful to you.

For details about configuring the [Ansible role for Radicle node](https://github.com/mother-of-all-self-hosting/ansible-role-radicle-node), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-radicle-node/blob/main/docs/configuring-radicle-node.md) online
- 📁 `roles/galaxy/radicle_node/docs/configuring-radicle-node.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Prerequisites

You may need to open some ports to your server, if you use another firewall in front of the server. Refer to [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-radicle-node/blob/main/docs/configuring-radicle-node.md#prerequisites) to check which ones to be configured.

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# radicle_node                                                         #
#                                                                      #
########################################################################

radicle_node_enabled: true

radicle_node_hostname: mash.example.com
radicle_node_path_prefix: /radicle-node

########################################################################
#                                                                      #
# /radicle_node                                                        #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the Radicle node instance becomes available at the URL specified with `radicle_node_hostname` and `radicle_node_path_prefix`. With the configuration above, the service is hosted at `https://mash.example.com/radicle-node`.

You can log in to the instance with the default login credential of the admin account (username: `admin`, password: `radicle-node`).

To improve security regarding the admin account, **the role configures the instance on the intranet search mode by default**, so that it does not broadcast its existence to peers before you change the login credential.

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-radicle-node/blob/main/docs/configuring-radicle-node.md#usage) on the role's documentation for details about changing the admin user password and search mode, including protecting the instance with the password.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-radicle-node/blob/main/docs/configuring-radicle-node.md#troubleshooting) on the role's documentation for details.

## Related services

- [SearXNG](searxng.md) — a privacy-respecting, hackable [metasearch engine](https://en.wikipedia.org/wiki/Metasearch_engine). See [this section](searxng.md#add-your-radicle-node-instance-optional) for the instruction to add your Radicle node instance to the SearXNG instance.
