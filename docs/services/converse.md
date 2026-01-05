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

# Converse

The playbook can install and configure [Converse](https://conversejs.org/) for you.

Converse is a free and open-source XMPP chat client written in JavaScript which can be tightly integrated into any website.

See the project's [documentation](https://conversejs.org/docs/html/index.html) to learn what Converse does and why it might be useful to you.

For details about configuring the [Ansible role for Converse](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az22bUmhZzA5VWtmKERFkEjGzdPuke), you can check them via:
- 🌐 [the role's documentation](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az22bUmhZzA5VWtmKERFkEjGzdPuke/tree/docs/configuring-converse.md) online
- 📁 `roles/galaxy/converse/docs/configuring-converse.md` locally, if you have [fetched the Ansible roles](../installing.md)

>[!NOTE]
> The role is configured to build the Docker image by default, as it is not provided by the upstream project. Before proceeding, make sure that the machine which you are going to run the Ansible commands against has sufficient computing power to build it.

## Prerequisites

To use XMPP via HTTP with the client, it is necessary to use a BOSH connection manager or the WebSocket API. When using the service, please check whether your XMPP server supports the WebSocket API and make sure to set up the BOSH connection manager if it does not.

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# converse                                                             #
#                                                                      #
########################################################################

converse_enabled: true

converse_hostname: mash.example.com
converse_path_prefix: /converse

########################################################################
#                                                                      #
# /converse                                                            #
#                                                                      #
########################################################################
```

It is optionally possible to edit settings about encryption, default themes, etc. See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az22bUmhZzA5VWtmKERFkEjGzdPuke/tree/docs/configuring-converse.md#adjusting-the-playbook-configuration) for details.

### Specify BOSH / WebSocket API

To use XMPP via HTTP with the client, it is necessary to use a BOSH connection manager or the WebSocket API. Refer to [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad:z22bUmhZzA5VWtmKERFkEjGzdPuke/tree/docs/configuring-converse.md#specify-bosh-websocket-api) on the role's documentation for details.

## Usage

After running the command for installation, the Converse instance becomes available at the URL specified with `converse_hostname` and `converse_path_prefix`. With the configuration above, the service is hosted at `https://mash.example.com/converse`.

To get started, open the URL with a web browser to log in to your XMPP server.

## Troubleshooting

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az22bUmhZzA5VWtmKERFkEjGzdPuke/tree/docs/configuring-converse.md#troubleshooting) on the role's documentation for details.
