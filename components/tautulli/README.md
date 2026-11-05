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
SPDX-FileCopyrightText: 2026 spatterlight

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Tautulli

The playbook can install and configure [Tautulli](https://tautulli.com/) for you.

Tautulli monitors the activity of a [Plex Media Server](../plex/README.md), and keeps statistics and a history of what has been watched, by whom and on which device. It can also send notifications and newsletters.

See the project's [documentation](https://github.com/Tautulli/Tautulli/wiki) to learn what Tautulli does and why it might be useful to you.

For details about configuring the [Ansible role for Tautulli](https://github.com/mother-of-all-self-hosting/ansible-role-tautulli), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-tautulli/blob/main/docs/configuring-tautulli.md) online
- 📁 `roles/galaxy/tautulli/docs/configuring-tautulli.md` locally, if you have [fetched the Ansible roles](../../docs/installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](../traefik/README.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../../docs/installing.md) process:

```yaml
########################################################################
#                                                                      #
# tautulli                                                             #
#                                                                      #
########################################################################

tautulli_enabled: true

tautulli_hostname: tautulli.example.com

########################################################################
#                                                                      #
# /tautulli                                                            #
#                                                                      #
########################################################################
```

### Connecting to Plex Media Server

If [Plex Media Server](../plex/README.md) is enabled as well, the playbook wires Tautulli to it automatically: Tautulli joins Plex Media Server's container network, and starting Tautulli starts Plex Media Server too.

Tautulli's log viewer can also show the logs of Plex Media Server, if its data directory is mounted into Tautulli. Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-tautulli/blob/main/docs/configuring-tautulli.md#mounting-plex-media-server-logs-optional) on the role's documentation for details.

## Usage

After running the command for installation, the Tautulli instance becomes available at the URL specified with `tautulli_hostname`. With the configuration above, the service is hosted at `https://tautulli.example.com`.

To get started, open the URL with a web browser, and follow the setup wizard to create an account. As whoever opens it first can complete the wizard, it is recommended to do so immediately after installing.

To connect the Plex Media Server installed by the playbook, set `Plex IP Address or Hostname` to `mash-plex` and `Plex Port` to `32400` when the setup wizard asks for them.

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-tautulli/blob/main/docs/configuring-tautulli.md#usage) on the role's documentation for details about the usage.

## Troubleshooting

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-tautulli/blob/main/docs/configuring-tautulli.md#troubleshooting) on the role's documentation for details.

## Related services

- [Plex Media Server](../plex/README.md) — A personal media server
- [Seerr](../seerr/README.md) — A media request and discovery manager
