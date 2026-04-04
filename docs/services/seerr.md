<!--
SPDX-FileCopyrightText: 2025 MASH project contributors

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Seerr

[Seerr](https://github.com/seerr-team/seerr) is a media request and discovery manager with support for [Jellyfin](jellyfin.md), [Plex](plex.md), and Emby.

## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# seerr                                                                #
#                                                                      #
########################################################################

seerr_enabled: true

seerr_hostname: seerr.example.com

########################################################################
#                                                                      #
# /seerr                                                               #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the Seerr instance becomes available at the URL specified with `seerr_hostname`. With the configuration above, the service is hosted at `https://seerr.example.com`.

> [!NOTE]
> The `seerr_path_prefix` variable can be adjusted to host under a subpath (e.g. `seerr_path_prefix: /seerr`), but this hasn't been tested yet.

For additional configuration options, refer to [ansible-role-seerr](https://github.com/spatterIight/ansible-role-seerr)'s `defaults/main.yml` file.

## Related services

## Related services

- "* Arr" applications — [Autobrr](autobrr.md) / [FlareSolverr](flaresolverr.md) / [Homarr](homarr.md) / [Overseerr](overseerr.md) / [Radarr](radarr.md) / [Sonarr](sonarr.md)
- [Jackett](jackett.md)
- [Jellyfin](jellyfin.md)
- [Plex](plex.md)
- [qBittorrent](qbittorrent.md)
