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
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# bitmagnet

The playbook can install and configure [bitmagnet](https://bitmagnet.org/bridge01/) for you.

bitmagnet is the PHP web application which generates web feeds for websites that do not have one.

See the project's [documentation](https://bitmagnet.github.io/bitmagnet/) to learn what bitmagnet does and why it might be useful to you.

For details about configuring the [Ansible role for bitmagnet](https://github.com/mother-of-all-self-hosting/ansible-role-bitmagnet), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-bitmagnet/blob/main/docs/configuring-bitmagnet.md) online
- 📁 `roles/galaxy/bitmagnet/docs/configuring-bitmagnet.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# bitmagnet                                                            #
#                                                                      #
########################################################################

bitmagnet_enabled: true

bitmagnet_hostname: mash.example.com
bitmagnet_path_prefix: /bitmagnet

########################################################################
#                                                                      #
# /bitmagnet                                                           #
#                                                                      #
########################################################################
```

### Enabling authentication

By default the service is public, and anyone can generate a feed to subscribe.

You can enable HTTP Basic authentication or token authentication. See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-bitmagnet/blob/main/docs/configuring-bitmagnet.md#enabling-authentication) on the role's documentation for details.

## Usage

After running the command for installation, the bitmagnet instance becomes available at the URL specified with `bitmagnet_hostname` and `bitmagnet_path_prefix`. With the configuration above, the service is hosted at `https://mash.example.com/bitmagnet`.

To use it, open the URL on the browser and log in to the service if authentication is enabled.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-bitmagnet/blob/main/docs/configuring-bitmagnet.md#troubleshooting) on the role's documentation for details.

## Related services

- [RSSHub](rsshub.md) — Create RSS feeds from web pages
