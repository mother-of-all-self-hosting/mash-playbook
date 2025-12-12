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

# SMP server

The playbook can install and configure [SMP server](https://simplex.chat/docs/server.html) for you.

SMP server is the relay server used to pass messages in [SimpleX](https://simplex.chat/) network.

See the project's [documentation](https://simplex.chat/docs/server.html#overview) to learn what SMP server does and why it might be useful to you.

For details about configuring the [Ansible role for SMP server](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3AzXf3qnvPwC2UsBpfTYmPesL5KSZc), you can check them via:
- 🌐 [the role's documentation](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3AzXf3qnvPwC2UsBpfTYmPesL5KSZc/tree/docs/configuring-smp-server.md) online
- 📁 `roles/galaxy/smp-server/docs/configuring-smp-server.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- (optional) [Traefik](traefik.md) reverse-proxy server — required on the default configuration

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# smp_server                                                           #
#                                                                      #
########################################################################

smp_server_enabled: true

smp_server_hostname: smpserver.example.com

########################################################################
#                                                                      #
# /smp_server                                                          #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the SMP server instance becomes available at the hostname specified with `smp_server_hostname`. With the configuration above, the service is hosted at `smpserver.example.com`.

See [this section](https://app.radicle.xyz/nodes/seed.progressiv.dev/rad:zXf3qnvPwC2UsBpfTYmPesL5KSZc/tree/docs/configuring-smp-server.md#usage) on the role's documentation for details about how to use the server. Also refer to [the official documentation](https://simplex.chat/docs/server.html#configuring-the-app-to-use-the-server) about how to configure the client to get it connect to your SMP server.

## Troubleshooting

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3AzXf3qnvPwC2UsBpfTYmPesL5KSZc/tree/docs/configuring-smp-server.md#troubleshooting) on the role's documentation for details.
