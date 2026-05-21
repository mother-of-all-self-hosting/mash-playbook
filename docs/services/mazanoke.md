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

# MAZANOKE

The playbook can install and configure [MAZANOKE](https://github.com/civilblur/mazanoke) for you.

MAZANOKE is a self-hosted web app offering a simple image optimizer that runs in your browser. All files are processed entirely on the client side.

See the project's [documentation](https://github.com/civilblur/mazanoke/blob/main/README.md) to learn what MAZANOKE does and why it might be useful to you.

For details about configuring the [Ansible role for MAZANOKE](https://radicle.network/nodes/seed.radicle.garden/rad%3AzGHUEPjboBuF8AWo3HKxEraEuHFq), you can check them via:

- 🌐 [the role's documentation](https://radicle.network/nodes/seed.radicle.garden/rad%3AzGHUEPjboBuF8AWo3HKxEraEuHFq/tree/docs/configuring-mazanoke.md) online
- 📁 `roles/galaxy/mazanoke/docs/configuring-mazanoke.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# mazanoke                                                             #
#                                                                      #
########################################################################

mazanoke_enabled: true

mazanoke_hostname: mazanoke.example.com

########################################################################
#                                                                      #
# /mazanoke                                                            #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the MAZANOKE instance becomes available at the URL specified with `mazanoke_hostname`. With the configuration above, the service is hosted at `https://mazanoke.example.com`.

## Troubleshooting

See [this section](https://radicle.network/nodes/seed.radicle.garden/rad%3AzGHUEPjboBuF8AWo3HKxEraEuHFq/tree/docs/configuring-mazanoke.md#troubleshooting) on the role's documentation for details.

## Related services

- [ConvertX](convertx.md) — Online file converter which supports a lot of different formats
