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

# Gokapi

The playbook can install and configure [Gokapi](https://github.com/Forceu/Gokapi) for you.

Gokapi is a lightweight server to share files that expire after a set number of downloads or days.

See the project's [documentation](https://gokapi.readthedocs.io) to learn what Gokapi does and why it might be useful to you.

For details about configuring the [Ansible role for Gokapi](https://radicle.network/nodes/iris.radicle.network/rad%3Az2zryaw72dpp4pRWKK1qvQzsY4qHR), you can check them via:

- 🌐 [the role's documentation](https://radicle.network/nodes/iris.radicle.network/rad%3Az2zryaw72dpp4pRWKK1qvQzsY4qHR/tree/docs/configuring-gokapi.md) online
- 📁 `roles/galaxy/gokapi/docs/configuring-gokapi.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# gokapi                                                               #
#                                                                      #
########################################################################

gokapi_enabled: true

gokapi_hostname: gokapi.example.com

########################################################################
#                                                                      #
# /gokapi                                                              #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the Gokapi instance becomes available at the URL specified with `gokapi_hostname`. With the configuration above, the service is hosted at `https://gokapi.example.com`.

To get started, open the URL `https://gokapi.example.com/setup` with a web browser, and follow the set up wizard. Refer to [this page](https://gokapi.readthedocs.io/en/latest/setup.html#initial-setup) on the official documentation for details.

## Troubleshooting

See [this section](https://radicle.network/nodes/iris.radicle.network/rad%3Az2zryaw72dpp4pRWKK1qvQzsY4qHR/tree/docs/configuring-gokapi.md#troubleshooting) on the role's documentation for details.

## Related services

- [Send](send.md) — Fork of Mozilla's Firefox Send which allows you to send encrypted files to other users
