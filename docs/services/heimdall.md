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
SPDX-FileCopyrightText: 2024 Thomas Miceli
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Heimdall

The playbook can install and configure [Heimdall](https://heimdall.site/) for you.

Heimdall is a dashboard for web applications.

See the project's [documentation](https://github.com/linuxserver/docker-heimdall/blob/master/README.md) to learn what Heimdall does and why it might be useful to you.

For details about configuring the [Ansible role for Heimdall](https://radicle.network/nodes/seed.radicle.garden/rad%3Az8D2GRZrm8JXZeHHe9j1HMvvj8An), you can check them via:

- 🌐 [the role's documentation](https://radicle.network/nodes/seed.radicle.garden/rad%3Az8D2GRZrm8JXZeHHe9j1HMvvj8An/tree/docs/configuring-heimdall.md) online
- 📁 `roles/galaxy/heimdall/docs/configuring-heimdall.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# heimdall                                                             #
#                                                                      #
########################################################################

heimdall_enabled: true

heimdall_hostname: heimdall.example.com

########################################################################
#                                                                      #
# /heimdall                                                            #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the Heimdall instance becomes available at the URL specified with `heimdall_hostname`. With the configuration above, the service is hosted at `https://heimdall.example.com`.

## Troubleshooting

See [this section](https://radicle.network/nodes/seed.radicle.garden/rad%3Az8D2GRZrm8JXZeHHe9j1HMvvj8An/tree/docs/configuring-heimdall.md#troubleshooting) on the role's documentation for details.

## Related services

- [I hate money](ihatemoney.md) — Shared budget manager
