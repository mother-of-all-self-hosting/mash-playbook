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
SPDX-FileCopyrightText: 2024 MASH project contributors
SPDX-FileCopyrightText: 2024 Sergio Durigan Junior

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# AdGuard Home

The playbook can install and configure [AdGuard Home](https://adguard.com/en/adguard-home/overview.html) for you.

AdGuard Home is a network-wide DNS software for blocking ads & tracking.

See the project's [documentation](https://adguard.com/kb/) to learn what AdGuard Home does and why it might be useful to you.

For details about configuring the [Ansible role for AdGuard Home](https://github.com/mother-of-all-self-hosting/ansible-role-adguard-home), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-adguard-home/blob/main/docs/configuring-adguard-home.md) online
- 📁 `roles/galaxy/adguard_home/docs/configuring-adguard-home.md` locally, if you have [fetched the Ansible roles](../installing.md)

> [!WARNING]
> Running a public DNS server is not advisable. You'd better install AdGuard Home in a trusted local network, or adjust its network interfaces and port exposure (via the variables in the [Networking](#networking) configuration section below) so that you don't expose your DNS server publicly to the whole world. If you're exposing your DNS server publicly, consider restricting who can use it by adjusting the **Allowed clients** setting in the **Access settings** section of **Settings** -> **DNS settings**.

## Prerequisites

### Open ports

You may need to open the following ports on your server:

- `53` over **TCP**, controlled by `adguard_home_container_dns_tcp_bind_port` — used for DNS over TCP
- `53` over **UDP**, controlled by `adguard_home_container_dns_udp_bind_port` — used for DNS over UDP

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-adguard-home/blob/main/docs/configuring-adguard-home.md#open-ports) on the role's documentation for details.

## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# adguard_home                                                         #
#                                                                      #
########################################################################

adguard_home_enabled: true

adguard_home_hostname: mash.example.com

# Hosting under a subpath sort of works, but is not ideal
# (see the usage section below for details).
# Consider using a dedicated hostname and removing the line below.
adguard_home_path_prefix: /adguard-home

########################################################################
#                                                                      #
# /adguard_home                                                        #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the AdGuard instance becomes available at the URL specified with `adguard_home_hostname` and `adguard_home_path_prefix`. With the configuration above, the service is hosted at `https://mash.example.com/adguard-home`.

>[!NOTE]
> When hosting under a subpath, there are some quirks caused by [this bug](https://github.com/AdguardTeam/AdGuardHome/issues/5478). See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-adguard-home/blob/main/docs/configuring-adguard-home.md#set-the-hostname) on the role's documentation for details.

To get started, open the URL with a web browser, and follow the set up wizard.

On the set up wizard, **make sure to set the HTTP port under "Admin Web Interface" to `3000`**.

>[!WARNING]
> If the default port number (`80`) is used, the web UI will stop working after the set up wizard completes.

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-adguard-home/blob/main/docs/configuring-adguard-home.md#usage) for things to configure.

## Troubleshooting and workaround

Adguard Home does not currently support being set up with a non-`root` account (see [issue](https://github.com/AdguardTeam/AdGuardHome/issues/4714)). See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-adguard-home/blob/main/docs/configuring-adguard-home.md#workaround-for-the-issue-related-non-root-account) on the role's documentation for the workaround.
