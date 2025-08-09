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
SPDX-FileCopyrightText: 2025 Nicola Murino

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Firezone

>[!WARNING]
> On this playbook, Firezone is implemented with [ansible-role-firezone](https://github.com/mother-of-all-self-hosting/ansible-role-firezone). The role is configured to install the legacy 0.7 version of Firezone which has reached end-of-life status and stopped receiving updates since January 31st, 2024. For later versions, Firezone, Inc. does not provide support for self-hosting in production, while the source code remains provided for self-hosting Firezone for merely *educational* or *hobby* purposes. See [this page](https://web.archive.org/web/20241230194456/https://github.com/firezone/firezone/blob/main/docs/README.md#can-i-self-host-firezone) for details.

The playbook can install and configure [Firezone](https://www.firezone.dev/) for you.

Firezone is a self-hosted VPN server based on [WireGuard](https://www.wireguard.com/) with a web UI.

See the project's [documentation](https://www.firezone.dev/kb) to learn what Firezone does and why it might be useful to you.

For details about configuring the [Ansible role for Firezone](https://github.com/mother-of-all-self-hosting/ansible-role-firezone), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-firezone/blob/main/docs/configuring-firezone.md) online
- 📁 `roles/galaxy/firezone/docs/configuring-firezone.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Prerequisites

### Open ports

You may need to open the following ports on your server. See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-firezone/blob/main/docs/configuring-firezone.md#open-ports) on the role's documentation for details.

## Dependencies

This service requires the following other services:

- a [Postgres](postgres.md) database
- a [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# firezone                                                             #
#                                                                      #
########################################################################

firezone_enabled: true

firezone_hostname: firezone.example.com

########################################################################
#                                                                      #
# /firezone                                                            #
#                                                                      #
########################################################################
```

To use Firezone, you also need to add other confurations for creating an admin account and setting a string for a secret key. See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-firezone/blob/main/docs/configuring-firezone.md#adjusting-the-playbook-configuration) on the role's documentation for details.

### Usage

After running the command for installation, the Firezone instance becomes available at the URL specified with `firezone_hostname`. With the configuration above, the service is hosted at `https://firezone.example.com`.

To get started, open the URL with a web browser, and log in to the service with the credentials set to `firezone_default_admin_email` and `firezone_default_admin_password`.

## Related services

- [WireGuard Easy](wg-easy.md) — [WireGuard](https://www.wireguard.com/) VPN + Web-based Admin UI
