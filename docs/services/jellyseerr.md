<!--
SPDX-FileCopyrightText: 2025 MASH project contributors
SPDX-FileCopyrightText: 2025 sudo-Tiz
SPDX-FileCopyrightText: 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Jellyseerr

[Jellyseerr](https://www.jellyseerr.org/) is an open-source media request and discovery manager for Jellyfin, Plex, and Emby.

## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# jellyseerr                                                            #
#                                                                      #
########################################################################

jellyseerr_enabled: true

jellyseerr_hostname: jellyseerr.example.com
########################################################################
#                                                                      #
# /jellyseerr                                                           #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the Jellyseerr instance becomes available at the URL specified with `jellyseerr_hostname`. With the configuration above, the service is hosted at `https://jellyseerr.example.com`.

> [!NOTE]
> The `jellyseerr_path_prefix` variable can be adjusted to host under a subpath (e.g. `jellyseerr_path_prefix: /jellyseerr`), but this hasn't been tested yet.

For additional configuration options, refer to [ansible-role-jellyseerr](https://github.com/spatterIight/ansible-role-jellyseerr)'s `defaults/main.yml` file.

## Recommended other services

Consider these other related services:

- [Autobrr](autobrr.md)
- [Jackett](jackett.md)
- [Jellyfin](jellyfin.md)
- [qBittorrent](qbittorrent.md)
- [Radarr](radarr.md)
- [Sonarr](sonarr.md)
