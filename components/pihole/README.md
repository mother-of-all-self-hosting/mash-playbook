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
SPDX-FileCopyrightText: 2024 MASH project contributors
SPDX-FileCopyrightText: 2024 Sergio Durigan Junior
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara
SPDX-FileCopyrightText: 2026 spatterlight

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Pi-hole

The playbook can install and configure [Pi-hole](https://pi-hole.net/) for you.

Pi-hole is a DNS sinkhole which blocks ads and trackers for every device that uses it as its DNS server, and comes with a web interface to manage it.

See the project's [documentation](https://docs.pi-hole.net/) to learn what Pi-hole does and why it might be useful to you.

For details about configuring the [Ansible role for Pi-hole](https://github.com/mother-of-all-self-hosting/ansible-role-pihole), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-pihole/blob/main/docs/configuring-pihole.md) online
- 📁 `roles/galaxy/pihole/docs/configuring-pihole.md` locally, if you have [fetched the Ansible roles](../../docs/installing.md)

> [!WARNING]
> Running a public DNS server is not advisable. You should install Pi-hole in a trusted local network, or set its port exposure so that you don't expose your DNS server publicly to the whole world.

## Prerequisites

### Open ports

You may need to open the following ports on your server:

- `53` over **TCP**, controlled by `pihole_container_dns_tcp_bind_port` — used for DNS over TCP
- `53` over **UDP**, controlled by `pihole_container_dns_udp_bind_port` — used for DNS over UDP

These ports are not exposed by default. Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-pihole/blob/main/docs/configuring-pihole.md#open-ports) on the role's documentation for details.

## Dependencies

This service requires the following other services:

- [Traefik](../traefik/README.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../../docs/installing.md) process:

```yaml
########################################################################
#                                                                      #
# pihole                                                               #
#                                                                      #
########################################################################

pihole_enabled: true

pihole_hostname: pihole.example.com

########################################################################
#                                                                      #
# /pihole                                                              #
#                                                                      #
########################################################################
```

### Set the password

You also need to set the password for the web interface. To do so, add the following configuration to your `vars.yml` file. Make sure to replace `YOUR_PASSWORD_HERE` with your own value.

```yaml
pihole_environment_variables_ftlconf_webserver_api_password: YOUR_PASSWORD_HERE
```

As it is set by the playbook, the password cannot be changed on the web interface.

## Usage

After running the command for installation, the Pi-hole instance becomes available at the URL specified with `pihole_hostname`. With the configuration above, the service is hosted at `https://pihole.example.com`. Log in with the password you have set.

To have Pi-hole block ads and trackers, set the server as the DNS server of your devices, or of your router, so that it hands the server out to them.

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-pihole/blob/main/docs/configuring-pihole.md#usage) on the role's documentation for details about the usage.

## Troubleshooting

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-pihole/blob/main/docs/configuring-pihole.md#troubleshooting) on the role's documentation for details.

## Related services

- [AdGuard Home](../adguard_home/README.md) — A network-wide DNS software for blocking ads & tracking
- [WireGuard Easy](../wg_easy/README.md) — The easiest way to run WireGuard VPN + Web-based Admin UI
