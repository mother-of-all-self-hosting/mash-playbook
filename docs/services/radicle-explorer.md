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

# Radicle Explorer

The playbook can install and configure [Radicle Explorer](https://app.radicle.xyz/nodes/seed.radicle.xyz/rad%3Az4V1sjrXqjvFdnCUbxPFqd5p4DtH5) for you.

Radicle Explorer allows you to interact with [Radicle](https://radicle.xyz/), a peer-to-peer code collaboration and publishing stack, directly from your web browser.

See the project's [documentation](https://app.radicle.xyz/nodes/seed.radicle.xyz/rad%3Az4V1sjrXqjvFdnCUbxPFqd5p4DtH5/tree/README.md) to learn what Radicle Explorer does and why it might be useful to you.

For details about configuring the [Ansible role for Radicle Explorer](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Azopwjin5Vh5dMgdHWiifJ2cg3bQW), you can check them via:
- 🌐 [the role's documentation](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Azopwjin5Vh5dMgdHWiifJ2cg3bQW/tree/docs/configuring-radicle-explorer.md) online
- 📁 `roles/galaxy/radicle_explorer/docs/configuring-radicle-explorer.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Prerequisites

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# radicle_explorer                                                     #
#                                                                      #
########################################################################

radicle_explorer_enabled: true

radicle_explorer_hostname: explorer.example.com

########################################################################
#                                                                      #
# /radicle_explorer                                                    #
#                                                                      #
########################################################################
```

**Note**: hosting Radicle Explorer under a subpath (by configuring the `radicle_explorer_path_prefix` variable) does not seem to be possible due to Radicle Explorer's technical limitations.

## Usage

After running the command for installation, the Radicle Explorer instance becomes available at the URL specified with `radicle_node_hostname`. With the configuration above, the service is hosted at `https://explorer.example.com`.

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Azopwjin5Vh5dMgdHWiifJ2cg3bQW/tree/docs/configuring-radicle-explorer.md#usage) on the role's documentation for details about how to browse a repository with the web client.

## Troubleshooting

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Azopwjin5Vh5dMgdHWiifJ2cg3bQW/tree/docs/configuring-radicle-explorer.md#troubleshooting) on the role's documentation for details.

## Related services

- [Radicle HTTP Daemon](radicle-httpd.md) — Gateway between the Radicle protocol and the HTTP protocol
- [Radicle node](radicle-node.md) — Network daemon for the Radicle network
