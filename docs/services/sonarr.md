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

### URL

In the example configuration above, we configure the service to be hosted at `https://sonarr.example.com`.

A `sonarr_path_prefix` variable can be adjusted to host under a subpath (e.g. `sonarr_path_prefix: /sonarr`), but this hasn't been tested yet.

## Usage

After [installation](../installing.md), you should access your new Sonarr instance at the URL you've chosen and configure a username and password. The recommended authenticaton method is `Forms (Login Page)`.

For additional configuration options, refer to [ansible-role-sonarr](https://github.com/spatterIight/ansible-role-sonarr)'s `defaults/main.yml` file.

## Recommended other services

Consider these other supported services that are also in the [*Arr stack](https://wiki.servarr.com/) of media automation tools:

- [Radarr](radarr.md)
- [Jackett](jackett.md)
  - For Jackett integration instructions, see the [setup guide](jackett.md#intergration-with-sonarrradarr)
- [qBittorrent](qbittorrent.md)
  - For qBittorrent integration instructions, see the [setup guide](qbittorrent.md#intergration-with-sonarrradarr)
- [Overseerr](overseerr.md)
- [Plex](plex.md)
