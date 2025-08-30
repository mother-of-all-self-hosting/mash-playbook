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
SPDX-FileCopyrightText: 2024 - 2025 MASH project contributors
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara
SPDX-FileCopyrightText: 2024 noah

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Readeck

The playbook can install and configure [Readeck](https://readeck.org) for you.

Readeck is a simple web application that lets you save the precious readable content of web pages you like and want to keep forever.

See the project's [documentation](https://readeck.org/en/docs/) to learn what Readeck does and why it might be useful to you.

For details about configuring the [Ansible role for Readeck](https://github.com/mother-of-all-self-hosting/ansible-role-readeck), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-readeck/blob/main/docs/configuring-readeck.md) online
- 📁 `roles/galaxy/readeck/docs/configuring-readeck.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# readeck                                                              #
#                                                                      #
########################################################################

readeck_enabled: true

readeck_hostname: readeck.example.com

########################################################################
#                                                                      #
# /readeck                                                             #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the Readeck instance becomes available at the URL specified with `readeck_hostname`. With the configuration above, the service is hosted at `https://readeck.example.com`.

To get started, open the URL with a web browser, and create a user.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-readeck/blob/main/docs/configuring-readeck.md#troubleshooting) on the role's documentation for details.
