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

# Appsmith

The playbook can install and configure [Appsmith](https://www.appsmith.com/) for you.

Appsmith is an open-source platform that enables developers to build and deploy custom internal tools and applications without writing code.

## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file:

```yaml
########################################################################
#                                                                      #
# appsmith                                                             #
#                                                                      #
########################################################################

appsmith_enabled: true

appsmith_hostname: appsmith.example.com

########################################################################
#                                                                      #
# /appsmith                                                            #
#                                                                      #
########################################################################
```

**Note**: hosting Appsmith under a subpath (by configuring the `appsmith_path_prefix` variable) does not seem to be possible due to Appsmith's technical limitations.

## Installation

After configuring the playbook, run the [installation](../installing.md) command.

It is recommended to install Appsmith with public registration enabled at first, create your user account, and disable public registration unless you need it.

By default, public registration on the instance is disabled. You can enable it by adding the following configuration to your `vars.yml` file:

```yaml
appsmith_environment_variable_appsmith_signup_disabled: false
```

To disable public registration, remove the configuration and run the command below:

```sh
just install-service appsmith
```

## Usage

After installation, your Appsmith instance becomes available at the URL specified with `appsmith_hostname` (`https://appsmith.example.com` per the setting above). You can create the first user from the web interface.
