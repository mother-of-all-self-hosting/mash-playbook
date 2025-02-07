# Radarr

[Radarr](https://radarr.video/) is a movie organizer/manager for usenet and torrent users.

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

### URL

In the example configuration above, we configure the service to be hosted at `https://radarr.example.com`.

A `radarr_path_prefix` variable can be adjusted to host under a subpath (e.g. `radarr_path_prefix: /radarr`), but this hasn't been tested yet.

## Usage

After [installation](../installing.md), you should access your new Radarr instance at the URL you've chosen and configure a username and password. The recommended authenticaton method is `Forms (Login Page)`.

For additional configuration options, refer to [ansible-role-radarr](https://github.com/spatterIight/ansible-role-radarr)'s `defaults/main.yml` file.

## Recommended other services

You may also wish to look into [Sonarr](sonarr.md) and [Jackett](jackett.md), which are similar applications that are also apart of the [*Arr stack](https://wiki.servarr.com/) of media automation tools. For information on intergrating Jackett into your Sonarr instance, see the [relevant Jackett documentation](jackett.md#intergration-with-sonarrradarr).
