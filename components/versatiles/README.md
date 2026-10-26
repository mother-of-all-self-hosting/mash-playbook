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
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2023, 2024 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2024, 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# VersaTiles

The playbook can install and configure [VersaTiles](https://versatiles.org) for you.

VersaTiles is a free stack for generating and serving vector tiles based on [OpenStreetMap](https://openstreetmap.com) data.

See the project's [documentation](https://docs.versatiles.org/) to learn what VersaTiles does and why it might be useful to you.

For details about configuring the [Ansible role for VersaTiles](https://github.com/mother-of-all-self-hosting/ansible-role-versatiles/), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-versatiles/blob/main/docs/configuring-versatiles.md) online
- 📁 `roles/galaxy/versatiles/docs/configuring-versatiles.md` locally, if you have [fetched the Ansible roles](../../docs/installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](../traefik/README.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../../docs/installing.md) process:

```yaml
########################################################################
#                                                                      #
# versatiles                                                           #
#                                                                      #
########################################################################

versatiles_enabled: true

versatiles_hostname: versatiles.example.com

########################################################################
#                                                                      #
# /versatiles                                                          #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the VersaTiles instance becomes available at the URL specified with `versatiles_hostname`. With the configuration above, the service is hosted at `https://versatiles.example.com`.

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-versatiles/blob/main/docs/configuring-versatiles.md#usage) on the role's documentation for details about the usage.

## Troubleshooting

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-versatiles/blob/main/docs/configuring-versatiles.md#troubleshooting) on the role's documentation for details.
