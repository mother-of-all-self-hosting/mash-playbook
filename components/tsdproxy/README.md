<!--
SPDX-FileCopyrightText: 2020 - 2024 MDAD project contributors
SPDX-FileCopyrightText: 2020 - 2025 Slavi Pantaleev
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
SPDX-FileCopyrightText: 2025 MASH project contributors
SPDX-FileCopyrightText: 2026 Bergrübe

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# TSDProxy

The playbook can install and configure [TSDProxy](https://almeidapaulopt.github.io/tsdproxy/) for you.

TSDProxy is an application that automatically creates a proxy to virtual addresses in your [Tailscale](https://tailscale.com/) network.

See the project's [documentation](https://almeidapaulopt.github.io/tsdproxy/docs/) to learn what TSDProxy does and why it might be useful to you.

For details about configuring the [Ansible role for TSDProxy](https://github.com/mother-of-all-self-hosting/ansible-role-tsdproxy), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-tsdproxy/blob/main/docs/configuring-tsdproxy.md) online
- 📁 `roles/galaxy/tsdproxy/docs/configuring-tsdproxy.md` locally, if you have [fetched the Ansible roles](../../docs/installing.md)

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../../docs/installing.md) process:

```yaml
########################################################################
#                                                                      #
# tsdproxy                                                             #
#                                                                      #
########################################################################

tsdproxy_enabled: true

########################################################################
#                                                                      #
# /tsdproxy                                                            #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the TSDProxy instance becomes available.

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-tsdproxy/blob/main/docs/configuring-tsdproxy.md#usage) on the role's documentation for details about the usage, including how to add a new service.

>[!NOTE]
> If [ansible-role-container-socket-proxy](https://github.com/mother-of-all-self-hosting/ansible-role-container-socket-proxy) is installed by the playbook (default), the container will use the proxy. If not, the container will mount the Docker socket at `/var/run/docker.sock`. You can change this by configuring `tsdproxy_docker_endpoint`.
>
> Do not forget to set `tsdproxy_docker_endpoint_is_unix_socket` to `false` if a TCP endpoint is enabled.

## Related services

- [Headscale](../headscale/README.md) — Tailscale-compatible control server for managing Tailscale devices
