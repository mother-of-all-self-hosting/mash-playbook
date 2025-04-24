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

# ConvertX

The playbook can install and configure [ConvertX](https://github.com/C4illin/ConvertX) for you.

ConvertX is a self-hosted online file converter which supports a lot of different formats for pictures, video, images, document files, etc.

See the project's [documentation](https://github.com/C4illin/ConvertX/blob/main/README.md) to learn what ConvertX does and why it might be useful to you.

For details about configuring the [Ansible role for ConvertX](https://github.com/mother-of-all-self-hosting/ansible-role-convertx), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-convertx/blob/main/docs/configuring-convertx.md) online
- 📁 `roles/galaxy/convertx/docs/configuring-convertx.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# convertx                                                             #
#                                                                      #
########################################################################

convertx_enabled: true

convertx_hostname: mash.example.com
convertx_environment_variables_webroot: /convertx

########################################################################
#                                                                      #
# /convertx                                                            #
#                                                                      #
########################################################################
```

As the most of the necessary settings for the role have been taken care of by the playbook, you can enable ConvertX on your server with this minimum configuration.

See the role's documentation for details about configuring ConvertX per your preference (such as [enabling account registration](https://github.com/mother-of-all-self-hosting/ansible-role-convertx/blob/main/docs/configuring-convertx.md#enable-account-registration-optional)).

## Usage

After running the command for installation, ConvertX becomes available at the specified hostname with the subpath like `https://mash.example.com/convertx`. To use it, open the URL on the browser and create an account.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-convertx/blob/main/docs/configuring-convertx.md#troubleshooting) on the role's documentation for details.
