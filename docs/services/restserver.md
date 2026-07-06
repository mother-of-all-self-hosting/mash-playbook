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
SPDX-FileCopyrightText: 2024 Tiz
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Rest Server

The playbook can install and configure [Rest Server](https://github.com/Rest ServerOrg/restserver-v3) for you.

Rest Server (Learning Using Texts) is a web application for learning foreign languages through reading.

See the project's [documentation](https://restserverorg.github.io/restserver-manual/) to learn what Rest Server does and why it might be useful to you.

For details about configuring the [Ansible role for Rest Server](https://radicle.network/nodes/iris.radicle.network/rad%3Az3NzUqjPeDbwcwQcZ4Vfi82tpWkm1), you can check them via:

- 🌐 [the role's documentation](https://radicle.network/nodes/iris.radicle.network/rad%3Az3NzUqjPeDbwcwQcZ4Vfi82tpWkm1/tree/docs/configuring-restserver.md) online
- 📁 `roles/galaxy/restserver/docs/configuring-restserver.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# restserver                                                           #
#                                                                      #
########################################################################

restserver_enabled: true

restserver_hostname: restserver.example.com

########################################################################
#                                                                      #
# /restserver                                                          #
#                                                                      #
########################################################################
```

### Configuring HTTP Basic authentication

The HTTP Basic authentication on Traefik is enabled for the web interface by default, considering the nature of the service. See [this section](https://radicle.network/nodes/iris.radicle.network/rad%3Az3NzUqjPeDbwcwQcZ4Vfi82tpWkm1/tree/docs/configuring-restserver.md#configuring-http-basic-authentication) on the role's documentation for details about how to set it up or disable it.

## Usage

After running the command for installation, the Rest Server instance becomes available at the URL specified with `restserver_hostname`. With the configuration above, the service is hosted at `https://restserver.example.com`.

## Troubleshooting

See [this section](https://radicle.network/nodes/iris.radicle.network/rad%3Az3NzUqjPeDbwcwQcZ4Vfi82tpWkm1/tree/docs/configuring-restserver.md#troubleshooting) on the role's documentation for details.
