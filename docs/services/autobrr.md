# Autobrr

[Autobrr](https://autobrr.com/) is a modern autodl-irssi replacement, an easy to use download automator for torrents and usenet.

## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# autobrr                                                              #
#                                                                      #
########################################################################

autobrr_enabled: true

autobrr_hostname: autobrr.example.com

########################################################################
#                                                                      #
# /autobrr                                                             #
#                                                                      #
########################################################################
```

### URL

In the example configuration above, we configure the service to be hosted at `https://autobrr.example.com`.

A `autobrr_path_prefix` variable can be adjusted to host under a subpath (e.g. `autobrr_path_prefix: /autobrr`), but this hasn't been tested yet.

## Usage

After [installation](../installing.md), you should access your new Autobrr instance at the URL you've chosen. Follow the prompts to finish setup:

![Autobrr Create Account](../assets/autobrr/setup-1.png)

## Recommended other services

Consider these other related services:

- [Radarr](radarr.md)
- [Sonarr](sonarr.md)
- [Jackett](jackett.md)
- [qBittorrent](qbittorrent.md)
- [Plex](plex.md)
- [Jellyfin](jellyfin.md)
- [Overseerr](overseerr.md)
