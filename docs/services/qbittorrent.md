<!--
SPDX-FileCopyrightText: 2023 Alejandro AR
SPDX-FileCopyrightText: 2023 Nikita Chernyi
SPDX-FileCopyrightText: 2023, 2024 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023, 2024 Sergio Durigan Junior
SPDX-FileCopyrightText: 2023-2025 MASH project contributors
SPDX-FileCopyrightText: 2023-2025 Slavi Pantaleev
SPDX-FileCopyrightText: 2024 Katherine Door
SPDX-FileCopyrightText: 2024 Oliver Lorenz
SPDX-FileCopyrightText: 2025 Gergely Horváth
SPDX-FileCopyrightText: 2025 XHawk87
SPDX-FileCopyrightText: 2025 spatterlight
SPDX-FileCopyrightText: 2025, 2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# qBittorrent

The playbook can install and configure [qBittorrent](https://www.qbittorrent.org/) for you.

qBittorrent is a BitTorrent client programmed in C++ / Qt that uses libtorrent.

See the project's [documentation](https://github.com/qbittorrent/qBittorrent/wiki/) to learn what qBittorrent does and why it might be useful to you.

For details about configuring the [Ansible role for qBittorrent](https://github.com/mother-of-all-self-hosting/ansible-role-qbittorrent), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-qbittorrent/blob/main/docs/configuring-qbittorrent.md) online
- 📁 `roles/galaxy/qbittorrent/docs/configuring-qbittorrent.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# qbittorrent                                                          #
#                                                                      #
########################################################################

qbittorrent_enabled: true

qbittorrent_hostname: qbittorrent.example.com

########################################################################
#                                                                      #
# /qbittorrent                                                         #
#                                                                      #
########################################################################
```

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-qbittorrent/blob/main/docs/configuring-qbittorrent.md#adjusting-the-playbook-configuration) on the role's documentation for details about other settings.

## Usage

After running the command for installation, the qBittorrent instance becomes available at the URL specified with `qbittorrent_hostname`. With the configuration above, the service is hosted at `https://qbittorrent.example.com`.

To get started, open the URL with a web browser to log in to the instance with a **temporary** randomly generated password. Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-qbittorrent/blob/main/docs/configuring-qbittorrent.md#usage) on the role's documentation for details.

## Related services

- [Autobrr](autobrr.md) — Download automation for torrents and Usenet
- [bitmagnet](bitmagnet.md) — BitTorrent indexer, DHT crawler, content classifier and search engine
- [Jackett](jackett.md) — API for Torrent trackers
- [Jellyfin](jellyfin.md) — Personal media server
- [Seerr](seerr.md) — A media request and discovery manager
- [Plex](plex.md) — Personal media server
- [Radarr](radarr.md) — Movie organizer/manager for Usenet and BitTorrent users
- [Sonarr](sonarr.md) — PVR for newsgroup and BitTorrent users
