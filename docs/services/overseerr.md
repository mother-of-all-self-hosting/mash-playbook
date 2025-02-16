# Overseerr

[Overseerr](https://www.overseerr.org/) is a request management and media discovery tool for the Plex ecosystem.

## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# overseerr                                                          #
#                                                                      #
########################################################################

overseerr_enabled: true

overseerr_hostname: overseerr.example.com

########################################################################
#                                                                      #
# /overseerr                                                         #
#                                                                      #
########################################################################
```

### URL

In the example configuration above, we configure the service to be hosted at `https://overseerr.example.com`.

A `overseerr_path_prefix` variable can be adjusted to host under a subpath (e.g. `overseerr_path_prefix: /overseerr`), but this hasn't been tested yet.

## Usage

After [installation](../installing.md), you should access your new Overseerr instance at the URL you've chosen.

For additional configuration options, refer to [ansible-role-overseerr](https://github.com/spatterIight/ansible-role-overseerr)'s `defaults/main.yml` file.

## Intergration with Sonarr/Radarr

## Intergration with Plex

## Recommended other services

Consider these other supported services that are also in the [*Arr stack](https://wiki.servarr.com/) of media automation tools:

- [Radarr](radarr.md)
- [Sonarr](sonarr.md)
- [Jackett](jackett.md)
- [Overseerr](overseerr.md)
