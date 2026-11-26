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
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara
SPDX-FileCopyrightText: 2025 MASH project contributors
SPDX-FileCopyrightText: 2025 spatterlight

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Autobrr

The playbook can install and configure [Autobrr](https://autobrr.com/) for you.

Autobrr is a modern autodl-irssi replacement, an easy to use download automator for torrents and Usenet.

See the project's [documentation](https://autobrr.com/introduction) to learn what Autobrr does and why it might be useful to you.

For details about configuring the [Ansible role for Autobrr](https://github.com/mother-of-all-self-hosting/ansible-role-autobrr), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-autobrr/blob/main/docs/configuring-autobrr.md) online
- 📁 `roles/galaxy/autobrr/docs/configuring-autobrr.md` locally, if you have [fetched the Ansible roles](../../docs/installing.md)

## Dependencies

This service requires the following other services:

- [Postgres](../postgres/README.md) / [SQLite](https://www.sqlite.org/) database
- [Traefik](../traefik/README.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../../docs/installing.md) process:

```yaml
########################################################################
#                                                                      #
# autobrr                                                              #
#                                                                      #
########################################################################

autobrr_enabled: true

autobrr_hostname: mash.example.com
autobrr_path_prefix: /autobrr

########################################################################
#                                                                      #
# /autobrr                                                             #
#                                                                      #
########################################################################
```

### Select database to use

Autobrr can use either Postgres or SQLite, and you need to choose one. Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-autobrr/blob/main/docs/configuring-autobrr.md#specify-database) on the role's documentation for details.

>[!NOTE]
> The database for your existing installation is most likely to be `sqlite`.

## Usage

After running the command for installation, the Autobrr instance becomes available at the URL specified with `autobrr_hostname` and `autobrr_path_prefix`. With the configuration above, the service is hosted at `https://mash.example.com/autobrr`.

To get started, open the URL with a web browser to create an account.

## Troubleshooting

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-autobrr/blob/main/docs/configuring-autobrr.md#troubleshooting) on the role's documentation for details.

## Related services

- "* Arr" applications — [Homarr](../homarr/README.md) / [Radarr](../radarr/README.md) / [Sonarr](../sonarr/README.md)
- [Jackett](../jackett/README.md)
- [Jellyfin](../jellyfin/README.md)
- [Seerr](../seerr/README.md)
- [Plex](../plex/README.md)
- [qBittorrent](../qbittorrent/README.md)
- [qui](../qui/README.md)
