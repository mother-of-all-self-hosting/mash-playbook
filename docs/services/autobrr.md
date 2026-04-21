<!--
SPDX-FileCopyrightText: 2025 MASH project contributors
SPDX-FileCopyrightText: 2025, 2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Autobrr

The playbook can install and configure [Autobrr](https://autobrr.com/) for you.

Autobrr is a modern autodl-irssi replacement, an easy to use download automator for torrents and Usenet.

See the project's [documentation](https://autobrr.com/introduction) to learn what Autobrr does and why it might be useful to you.

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

## Usage

After running the command for installation, the Autobrr instance becomes available at the URL specified with `autobrr_hostname`. With the configuration above, the service is hosted at `https://autobrr.example.com`.

>[!NOTE]
> The `autobrr_path_prefix` variable can be adjusted to host under a subpath (e.g. `autobrr_path_prefix: /autobrr`), but this hasn't been tested yet.

To get started, open the URL with a web browser to create an account.

![Autobrr Create Account](../assets/autobrr/setup-1.webp)

## Related services

- "* Arr" applications — [FlareSolverr](flaresolverr.md) / [Homarr](homarr.md) / [Jellyseerr](jellyseerr.md) / [Overseerr](overseerr.md) / [Radarr](radarr.md) / [Sonarr](sonarr.md)
- [Jackett](jackett.md)
- [Jellyfin](jellyfin.md)
- [Plex](plex.md)
- [qBittorrent](qbittorrent.md)
