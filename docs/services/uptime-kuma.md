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

# Uptime Kuma

The playbook can install and configure [Uptime Kuma](https://uptime.kuma.pet/) for you.

Uptime Kuma is a fancy self-hosted monitoring tool similar to [Uptime Robot](https://uptimerobot.com/). It has functions such as monitoring uptime for HTTP(s), TCP, DNS Record, Steam Game Server, and Docker Containers, etc.

See the project's [documentation](https://github.com/louislam/uptime-kuma/wiki) to learn what Uptime Kuma does and why it might be useful to you.

For details about configuring the [Ansible role for Uptime Kuma](https://github.com/mother-of-all-self-hosting/ansible-role-uptime_kuma), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-uptime_kuma/blob/main/docs/configuring-uptime-kuma.md) online
- 📁 `roles/galaxy/uptime_kuma/docs/configuring-uptime-kuma.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# uptime-kuma                                                          #
#                                                                      #
########################################################################

uptime_kuma_enabled: true

uptime_kuma_hostname: uptime-kuma.example.com

########################################################################
#                                                                      #
# /uptime-kuma                                                         #
#                                                                      #
########################################################################
```

**Note**: hosting Uptime Kuma under a subpath (by configuring the `uptime_kuma_path_prefix` variable) does not seem to be possible due to Uptime Kuma's technical limitations.

## Usage

After running the command for installation, the Uptime Kuma instance becomes available at the URL specified with `uptime_kuma_hostname`. With the configuration above, the service is hosted at `https://uptime-kuma.example.com`.

To get started, open the URL with a web browser, and follow the set up wizard where you can create your admin user and configure the service. You can add monitors for web services as many as you like.

If you have enabled a self-hosted [ntfy](ntfy.md) server, it is possible to set up the Uptime Kuma instance to have it send notifications to a ntfy's "topic" (channel) when the monitored web service is down, without relaying them through servers owned and controlled by third parties.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting//ansible-role-uptime_kuma/blob/main/docs/configuring-uptime-kuma.md#troubleshooting) on the role's documentation for details.
