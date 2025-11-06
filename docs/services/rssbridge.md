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

The playbook can install and configure [RSS-Bridge](https://rss-bridge.org/bridge01/) for you.

RSS-Bridge is the PHP web application which generates web feeds for websites that do not have one.

See the project's [documentation](https://rss-bridge.github.io/rss-bridge/) to learn what RSS-Bridge does and why it might be useful to you.

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
rssbridge_path_prefix: /rssbridge

########################################################################
#                                                                      #
# /rssbridge                                                           #
#                                                                      #
########################################################################
```

### Enabling authentication

By default the service is public, and anyone can generate a feed to subscribe.

You can enable HTTP Basic authentication or token authentication. See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-rssbridge/blob/main/docs/configuring-rssbridge.md#enabling-authentication) on the role's documentation for details.

## Usage

After running the command for installation, the RSS-Bridge instance becomes available at the URL specified with `rssbridge_hostname` and `rssbridge_path_prefix`. With the configuration above, the service is hosted at `https://mash.example.com/rssbridge`.

To use it, open the URL on the browser and log in to the service if authentication is enabled.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-rssbridge/blob/main/docs/configuring-rssbridge.md#troubleshooting) on the role's documentation for details.

## Related services

- [RSSHub](rsshub.md) — Create RSS feeds from web pages
