<!--
SPDX-FileCopyrightText: 2025 MASH project contributors
SPDX-FileCopyrightText: 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Sonarr

[Sonarr](https://sonarr.tv/) is a smart PVR for newsgroup and bittorrent users.

## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# sonarr                                                               #
#                                                                      #
########################################################################

sonarr_enabled: true

sonarr_hostname: sonarr.example.com

# To mount additional data directories, use `sonarr_container_additional_volumes`
#
# Example:
# sonarr_container_additional_volumes:
#   - type: bind
#     src: /path/on/the/host
#     dst: /data
#   - type: bind
#     src: /another-path/on/the/host
#     dst: /read-only
#     options: readonly

########################################################################
#                                                                      #
# /sonarr                                                              #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the Sonarr instance becomes available at the URL specified with `sonarr_hostname`. With the configuration above, the service is hosted at `https://sonarr.example.com`.

>[!NOTE]
> The `sonarr_path_prefix` variable can be adjusted to host under a subpath (e.g. `sonarr_path_prefix: /sonarr`), but this hasn't been tested yet.

To get started, open the URL with a web browser, and configure a username and password. The recommended authentication method is `Forms (Login Page)`.

For additional configuration options, refer to [ansible-role-sonarr](https://github.com/spatterIight/ansible-role-sonarr)'s `defaults/main.yml` file.

## Recommended other services

Consider these other related services:

- [Autobrr](autobrr.md)
- [Jackett](jackett.md)
  - For Jackett integration instructions, see the [setup guide](jackett.md#intergration-with-sonarrradarr)
- [Jellyfin](jellyfin.md)
- [Overseerr](overseerr.md)
- [Plex](plex.md)
- [qBittorrent](qbittorrent.md)
  - For qBittorrent integration instructions, see the [setup guide](qbittorrent.md#intergration-with-sonarrradarr)
- [Radarr](radarr.md)
