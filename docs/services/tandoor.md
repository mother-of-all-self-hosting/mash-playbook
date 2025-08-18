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
SPDX-FileCopyrightText: 2023 Alejandro AR
SPDX-FileCopyrightText: 2023 Antonis Christofides
SPDX-FileCopyrightText: 2023 Felix Stupp
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara
SPDX-FileCopyrightText: 2024 MASH project contributors

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Tandoor

The playbook can install and configure [Tandoor](https://github.com/vabene1111/recipes) for you.

Tandoor is a self-hosted recipe manager.

See the project's [documentation](https://docs.tandoor.dev/) to learn what Tandoor does and why it might be useful to you.

## Dependencies

This service requires the following other services:

- a [Postgres](postgres.md) database
- a [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# tandoor                                                              #
#                                                                      #
########################################################################

tandoor_enabled: true

tandoor_hostname: mash.example.com
tandoor_path_prefix: /tandoor

########################################################################
#                                                                      #
# /tandoor                                                             #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the Tandoor instance becomes available at the URL specified with `tandoor_hostname` and `tandoor_path_prefix`. With the configuration above, the service is hosted at `https://mash.example.com/tandoor`.

To get started, open the URL with a web browser, and create the first administrator user.
