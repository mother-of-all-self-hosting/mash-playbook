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
SPDX-FileCopyrightText: 2024 Thomas Miceli
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Node-RED

The playbook can install and configure [Node-RED](https://nodered.org) for you.

Node-RED is a flow-based programming tool.

See the project's [documentation](https://nodered.org/docs/) to learn what Node-RED does and why it might be useful to you.

For details about configuring the [Ansible role for Node-RED](https://radicle.network/nodes/iris.radicle.network/rad%3Az3g4bZnzZJis1DEKVzR3pPsyUzicT), you can check them via:

- 🌐 [the role's documentation](https://radicle.network/nodes/iris.radicle.network/rad%3Az3g4bZnzZJis1DEKVzR3pPsyUzicT/tree/docs/configuring-nodered.md) online
- 📁 `roles/galaxy/nodered/docs/configuring-nodered.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# node-red                                                             #
#                                                                      #
########################################################################

nodered_enabled: true

nodered_hostname: nodered.example.com

########################################################################
#                                                                      #
# /node-red                                                            #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the Node-RED instance becomes available at the URL specified with `nodered_hostname`. With the configuration above, the service is hosted at `https://nodered.example.com`.

To get started, open the URL with a web browser to create an account.

## Troubleshooting

See [this section](https://radicle.network/nodes/iris.radicle.network/rad%3Az3g4bZnzZJis1DEKVzR3pPsyUzicT/tree/docs/configuring-nodered.md#troubleshooting) on the role's documentation for details.
