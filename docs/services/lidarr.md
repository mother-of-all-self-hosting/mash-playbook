<!--
SPDX-FileCopyrightText: 2025 MASH project contributors
SPDX-FileCopyrightText: 2025, 2026 Suguru Hirahara
SPDX-FileCopyrightText: 2026 Sudo-Tiz

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Lidarr

The playbook can install and configure [Lidarr](https://lidarr.audio/) for you.

Lidarr is a music collection manager for Usenet and BitTorrent users.

See the project's [documentation](https://wiki.servarr.com/lidarr) to learn what Lidarr does and why it might be useful to you.

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# lidarr                                                               #
#                                                                      #
########################################################################

lidarr_enabled: true

lidarr_hostname: lidarr.example.com

# To mount additional data directories, use `lidarr_container_additional_volumes_custom`
#
# Example:
# lidarr_container_additional_volumes_custom:
#   - type: bind
#     src: /path/on/the/host
#     dst: /data
#   - type: bind
#     src: /another-path/on/the/host
#     dst: /read-only
#     options: readonly

########################################################################
#                                                                      #
# /lidarr                                                              #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the Lidarr instance becomes available at the URL specified with `lidarr_hostname`. With the configuration above, the service is hosted at `https://lidarr.example.com`.

>[!NOTE]
> The `lidarr_path_prefix` variable can be adjusted to host under a subpath (e.g. `lidarr_path_prefix: /lidarr`), but this hasn't been tested yet.

To get started, open the URL with a web browser to create an account. The recommended authentication method is `Forms (Login Page)`.

For additional configuration options, refer to `defaults/main.yml` file.

## Related services

- "* Arr" applications — [Autobrr](autobrr.md) / [Homarr](homarr.md) / [Radarr](radarr.md) / [Sonarr](sonarr.md)
- [Jellyfin](jellyfin.md)
- [Plex](plex.md)
- [qBittorrent](qbittorrent.md)
  - For qBittorrent integration instructions, see the [setup guide](qbittorrent.md#integration-with-sonarrradarr)
