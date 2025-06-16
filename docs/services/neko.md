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
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Neko

The playbook can install and configure [Neko](https://neko.m1k1o.net/) for you.

Neko is a self-hosted virtual browser which runs in a Docker's container based on the WebRTC protocol. It enables to run not only web browsers but also desktop environments like KDE and Xfce remotely.

See the project's [documentation](https://neko.m1k1o.net/docs/v3/introduction) to learn what Neko does and why it might be useful to you.

For details about configuring the [Ansible role for Neko](https://github.com/mother-of-all-self-hosting/ansible-role-neko), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-neko/blob/main/docs/configuring-neko.md) online
- 📁 `roles/galaxy/neko/docs/configuring-neko.md` locally, if you have [fetched the Ansible roles](../installing.md)

> [!WARNING]
> The Neko service will run in a container with root privileges, no dropped capabilities and will be able to write inside the container. This seems to be a necessary deviation from the usual security standards in this playbook.

## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server

## Prerequisites

To use the service, by default you need to open ports `56000-56100/udp` of the host. See [here](https://neko.m1k1o.net/docs/v3/configuration/webrtc#epr) for details.

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# neko                                                                 #
#                                                                      #
########################################################################

neko_enabled: true

neko_hostname: neko.example.com

########################################################################
#                                                                      #
# /neko                                                                #
#                                                                      #
########################################################################
```

**Note**: hosting Neko under a subpath does not seem to be possible due to Neko's technical limitations.

Refer the role's documentation for settings required to use the instance, such as [configuring authentication](https://github.com/mother-of-all-self-hosting/ansible-role-neko/blob/main/docs/configuring-neko.md#configuring-authentication).

By default the instance is configured to authenticate administrators and regular users with passwords. To specify the passwords, add the following configuration to your `vars.yml` file. Make sure to replace `ADMIN_PASSWORD_HERE` and `USER_PASSWORD_HERE` with your own values.

```yaml
neko_environment_variables_neko_member_multiuser_admin_password: ADMIN_PASSWORD_HERE

neko_environment_variables_neko_member_multiuser_user_password: USER_PASSWORD_HERE
```

## Usage

After installation, your Neko instance becomes available at the URL specified with `neko_hostname`.

If you cannot log in to the instance, make sure that the ports are open on the server and WebRTC is enabled on the browser.

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-neko/blob/main/docs/configuring-neko.md#usage) on the role's documentation for the usage.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-neko/blob/main/docs/configuring-neko.md#troubleshooting) on the role's documentation for details.
