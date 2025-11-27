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

# Radicle HTTP Daemon

The playbook can install and configure [Radicle HTTP Daemon](https://app.radicle.xyz/nodes/seed.radicle.xyz/rad%3Az4V1sjrXqjvFdnCUbxPFqd5p4DtH5/tree/radicle-httpd/) for you.

Radicle HTTP Daemon is a background process which makes it possible to browse the content of your [seed node](https://radicle.xyz/guides/seeder#configuring-your-node) (`radicle-node`) on the [Radicle](https://radicle.xyz/) network, a peer-to-peer code collaboration stack built on Git. It is configured to have direct read-only access to the node’s storage and database, and expose this data via an HTTP JSON API.

See the project's [documentation](https://radicle.xyz/guides/seeder#running-the-http-daemon) to learn what Radicle HTTP Daemon does and why it might be useful to you.

For details about configuring the [Ansible role for Radicle HTTP Daemon](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az3roZFCprFZhmK8BvkrsKwkLZXr56), you can check them via:
- 🌐 [the role's documentation](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az3roZFCprFZhmK8BvkrsKwkLZXr56/tree/docs/configuring-radicle-httpd.md) online
- 📁 `roles/galaxy/radicle_httpd/docs/configuring-radicle-httpd.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Prerequisites

This service requires the following other services:

- [Radicle node](radicle-node.md)
- [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# radicle_httpd                                                        #
#                                                                      #
########################################################################

radicle_httpd_enabled: true

########################################################################
#                                                                      #
# /radicle_httpd                                                       #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the Radicle HTTP Daemon instance becomes available at the same URL as specified to the Radicle node with `radicle_node_hostname`.

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az3roZFCprFZhmK8BvkrsKwkLZXr56/tree/docs/configuring-radicle-httpd.md#usage) on the role's documentation for details about how to browse a repository on your seed node via a web client like [Radicle Explorer](https://app.radicle.xyz/nodes/seed.radicle.xyz/rad%3Az4V1sjrXqjvFdnCUbxPFqd5p4DtH5).

This playbook supports Radicle Explorer, and you can set up the instance by enabling it on `vars.yml`. See [this page](radicle-explorer.md) for details.

## Troubleshooting

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az3roZFCprFZhmK8BvkrsKwkLZXr56/tree/docs/configuring-radicle-httpd.md#troubleshooting) on the role's documentation for details.

## Related services

- [Radicle Explorer](radicle-explorer.md) — Radicle user interface for the web browser
- [Radicle node](radicle-node.md) — Network daemon for the Radicle network
