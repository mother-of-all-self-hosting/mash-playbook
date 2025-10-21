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

# RSS-Bridge

The playbook can install and configure [RSS-Bridge](https://github.com/C4illin/RSS-Bridge) for you.

RSS-Bridge is a self-hosted online file converter which supports a lot of different formats for pictures, video, images, document files, etc.

See the project's [documentation](https://github.com/C4illin/RSS-Bridge/blob/main/README.md) to learn what RSS-Bridge does and why it might be useful to you.

For details about configuring the [Ansible role for RSS-Bridge](https://github.com/mother-of-all-self-hosting/ansible-role-rssbridge), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-rssbridge/blob/main/docs/configuring-rssbridge.md) online
- 📁 `roles/galaxy/rssbridge/docs/configuring-rssbridge.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# rssbridge                                                            #
#                                                                      #
########################################################################

rssbridge_enabled: true

rssbridge_hostname: mash.example.com
rssbridge_environment_variables_webroot: /rssbridge

########################################################################
#                                                                      #
# /rssbridge                                                           #
#                                                                      #
########################################################################
```

As the most of the necessary settings for the role have been taken care of by the playbook, you can enable RSS-Bridge on your server with this minimum configuration.

See the role's documentation for details about configuring RSS-Bridge per your preference (such as [enabling account registration](https://github.com/mother-of-all-self-hosting/ansible-role-rssbridge/blob/main/docs/configuring-rssbridge.md#enable-account-registration-optional)).

By deploying an authentication service like [Tinyauth](tinyauth.md), you can disable the authentication function provided by RSS-Bridge in favor of it.

## Usage

After running the command for installation, the RSS-Bridge instance becomes available at the URL specified with `rssbridge_hostname` and `rssbridge_path_prefix`. With the configuration above, the service is hosted at `https://mash.example.com/rssbridge`.

To use it, open the URL on the browser and create an account.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-rssbridge/blob/main/docs/configuring-rssbridge.md#troubleshooting) on the role's documentation for details.
