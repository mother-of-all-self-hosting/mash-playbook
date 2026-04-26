<!--
SPDX-FileCopyrightText: 2025 MASH project contributors
SPDX-FileCopyrightText: 2025 Sudo-Tiz

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Bazarr

[Bazarr](https://www.bazarr.media/) is a companion application to Sonarr and Radarr that manages and downloads subtitles based on your requirements.

## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# bazarr                                                               #
#                                                                      #
########################################################################

bazarr_enabled: true

bazarr_hostname: bazarr.example.com

# To mount additional data directories, use `bazarr_container_additional_volumes`
#
# Example:
# bazarr_container_additional_volumes:
#   - type: bind
#     src: /path/on/the/host
#     dst: /data
#   - type: bind
#     src: /another-path/on/the/host
#     dst: /read-only
#     options: readonly

########################################################################
#                                                                      #
# /bazarr                                                              #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the Bazarr instance becomes available at the URL specified with `bazarr_hostname`. With the configuration above, the service is hosted at `https://bazarr.example.com`.

>[!NOTE]
> The `bazarr_path_prefix` variable can be adjusted to host under a subpath (e.g. `bazarr_path_prefix: /bazarr`), but this hasn't been tested yet.

To get started, open the URL with a web browser to configure Bazarr. The recommended authentication method is `Forms`.

For additional configuration options, refer to [ansible-role-bazarr](https://github.com/sudo-Tiz/ansible-role-bazarr)'s `defaults/main.yml` file.

## Integration with Sonarr/Radarr

To integrate Bazarr with [Sonarr](sonarr.md) and/or [Radarr](radarr.md), you need to ensure that:

1. All services can access the same media directories via `bazarr_container_additional_volumes`, `sonarr_container_additional_volumes`, and/or `radarr_container_additional_volumes`
2. The services are connected to each other's networks:

```yaml
# Connect Bazarr to Sonarr's network
bazarr_container_additional_networks_custom:
  - "{{ sonarr_container_network }}"

# Connect Bazarr to Radarr's network
bazarr_container_additional_networks_custom:
  - "{{ radarr_container_network }}"
```

After setup, configure the integrations in Bazarr's web interface under Settings → Sonarr/Radarr.

## Related services

- "* Arr" applications — [Autobrr](autobrr.md) / [FlareSolverr](flaresolverr.md) / [Homarr](homarr.md) / [Jellyseerr](jellyseerr.md) / [Overseerr](overseerr.md) / [Radarr](radarr.md) / [Sonarr](sonarr.md)
- [Jackett](jackett.md)
- [Jellyfin](jellyfin.md)
- [Plex](plex.md)
- [qBittorrent](qbittorrent.md)
