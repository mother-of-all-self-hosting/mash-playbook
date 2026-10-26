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
SPDX-FileCopyrightText: 2024, 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Homarr

The playbook can install and configure [Homarr](https://homarr.dev) for you.

Homarr is a highly customizable dashboard for management of your favorite applications and services with a drag-and-drop grid system, which integrates with various self-hosted applications.

See the project's [documentation](https://homarr.dev/docs/getting-started) to learn what Homarr does and why it might be useful to you.

For details about configuring the [Ansible role for Homarr](https://github.com/mother-of-all-self-hosting/ansible-role-homarr), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-homarr/blob/main/docs/configuring-homarr.md) online
- 📁 `roles/galaxy/homarr/docs/configuring-homarr.md` locally, if you have [fetched the Ansible roles](../../docs/installing.md)

## Dependencies

This service requires the following other services:

- [Postgres](../postgres/README.md) / [SQLite](https://www.sqlite.org/) database
- [Traefik](../traefik/README.md) reverse-proxy server
- (optional) [ntfy](../ntfy/README.md)

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../../docs/installing.md) process:

```yaml
########################################################################
#                                                                      #
# homarr                                                               #
#                                                                      #
########################################################################

homarr_enabled: true

homarr_hostname: homarr.example.com

########################################################################
#                                                                      #
# /homarr                                                              #
#                                                                      #
########################################################################
```

**Note**: hosting Homarr under a subpath (by configuring the `homarr_path_prefix` variable) does not seem to be possible due to Homarr's technical limitations.

### Set random 32-byte hex digits for secret key

You also need to set random **32-byte hex digits** to encrypt integration secrets on the database. To do so, add the following configuration to your `vars.yml` file. The value can be generated with `openssl rand -hex 32` or in another way.

```yaml
homarr_environment_variables_secret_encryption_key: YOUR_SECRET_KEY_HERE
```

>[!NOTE]
> Other type of values such as one generated with `pwgen -s 64 1` does not work.

### Select database to use

Homarr can use Postgres or SQLite, and you need to choose one. Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-homarr/blob/main/docs/configuring-homarr.md#specify-database) on the role's documentation for details.

>[!NOTE]
> If you have not disabled Postgres explicitly with this playbook, the database for your existing installation is most likely to be `postgres`.

## Usage

After running the command for installation, the Homarr instance becomes available at the URL specified with `homarr_hostname`. With the configuration above, the service is hosted at `https://homarr.example.com`.

To get started, open the URL with a web browser, and follow the set up wizard. Refer to [this official guide](https://homarr.dev/docs/getting-started/after-the-installation/) for details.

### Playbook's services on Homarr

On Homarr's board it is possible to create and add icons of many services, including the ones which can be installed with this playbook such as [Nextcloud](../nextcloud/README.md), [PeerTube](../peertube/README.md), [PrivateBin](../privatebin/README.md), [Syncthing](../syncthing/README.md), etc.

Homarr also integrates with various software, to which you can connect your applications to interact via widgets. Here is a list of integrations which are also available on this playbook:

| Category | Service |
| ---------- | -------- |
| Bookmark | [Karakeep](../karakeep/README.md), [Linkwarden](../linkwarden/README.md) |
| Indexer | [Jackett](../jackett/README.md), [Prowlarr](../prowlarr/README.md) |
| Media | [audiobookshelf](../audiobookshelf/README.md), [Bazarr](../bazarr/README.md), [Immich](../immich/README.md), [Jellyfin](../jellyfin/README.md), [Lidarr](../lidarr/README.md), [Navidrome](../navidrome/README.md), [Plex](../plex/README.md), [Radarr](../radarr/README.md), [Seerr](../seerr/README.md), [Sonarr](../sonarr/README.md) |
| Monitoring | [Beszel](../beszel_hub/README.md), [Changedetection.io](../changedetection/README.md), [Prometheus](../prometheus/README.md), [Uptime Kuma](../uptime_kuma/README.md) |
| Notification | [Gotify](../gotify/README.md), [Nextcloud](../nextcloud/README.md), [ntfy](../ntfy/README.md) |
| Misc | [AdGuard Home](../adguard_home/README.md), [Autobrr](../autobrr/README.md), [Miniflux](../miniflux/README.md), [Paperless-ngx](../paperless/README.md), [qBittorrent](../qbittorrent/README.md), [Syncthing](../syncthing/README.md), [Tandoor](../tandoor/README.md), [Wazuh](../wazuh/README.md) |

Refer to [this page](https://homarr.dev/docs/integrations/) on the official documentation for the latest information about integrations.

## Troubleshooting

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-homarr/blob/main/docs/configuring-homarr.md#troubleshooting) on the role's documentation for details.

## Related services

- [Heimdall](../heimdall/README.md) — Dashboard for web applications
