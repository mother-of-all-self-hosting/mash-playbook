<!--
SPDX-FileCopyrightText: 2025 MASH project contributors
SPDX-FileCopyrightText: 2025, 2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Radarr

The playbook can install and configure [Radarr](https://radarr.video/) for you.

Radarr is a movie organizer/manager for Usenet and BitTorrent users.

See the project's [documentation](https://wiki.servarr.com/radarr) to learn what Radarr does and why it might be useful to you.

## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# radarr                                                               #
#                                                                      #
########################################################################

radarr_enabled: true

radarr_hostname: radarr.example.com

# To mount additional data directories, use `radarr_container_additional_volumes`
#
# Example:
# radarr_container_additional_volumes:
#   - type: bind
#     src: /path/on/the/host
#     dst: /data
#   - type: bind
#     src: /another-path/on/the/host
#     dst: /read-only
#     options: readonly

########################################################################
#                                                                      #
# /radarr                                                              #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the Autobrr instance becomes available at the URL specified with `radarr_hostname`. With the configuration above, the service is hosted at `https://radarr.example.com`.

>[!NOTE]
> The `radarr_path_prefix` variable can be adjusted to host under a subpath (e.g. `radarr_path_prefix: /radarr`), but this hasn't been tested yet.

To get started, open the URL with a web browser to create an account. The recommended authentication method is `Forms (Login Page)`.

For additional configuration options, refer to [ansible-role-radarr](https://github.com/spatterIight/ansible-role-radarr)'s `defaults/main.yml` file.

## Related services

- "* Arr" applications — [Autobrr](autobrr.md) / [FlareSolverr](flaresolverr.md) / [Homarr](homarr.md) / [Jellyseerr](jellyseerr.md) / [Overseerr](overseerr.md) / [Sonarr](sonarr.md)
- [Jackett](jackett.md)
  - For Jackett integration instructions, see the [setup guide](jackett.md#intergration-with-sonarrradarr)
- [Jellyfin](jellyfin.md)
- [Plex](plex.md)
- [qBittorrent](qbittorrent.md)
  - For qBittorrent integration instructions, see the [setup guide](qbittorrent.md#intergration-with-sonarrradarr)
