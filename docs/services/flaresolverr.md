<!--
SPDX-FileCopyrightText: 2025 MASH project contributors
SPDX-FileCopyrightText: 2025 sudo-Tiz

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Flaresolverr

[Flaresolverr](https://github.com/FlareSolverr/FlareSolverr) is an open-source proxy server to bypass Cloudflare protection.

## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# flaresolverr                                                         #
#                                                                      #
########################################################################

flaresolverr_enabled: true
########################################################################
#                                                                      #
# /flaresolverr                                                        #
#                                                                      #
########################################################################
```

## Usage

After running the installation command, the Flaresolverr instance becomes available internally at the `flaresolverr_container_http_port` value (default is **8191**) and is reachable from any other media service like [Jackett](jackett.md). If you need the container to be accessible from outside, you can use `flaresolverr_container_http_bind_port` or `flaresolverr_hostname`.

> **Note:**
> The `flaresolverr_path_prefix` variable can be adjusted to host under a subpath (e.g., `flaresolverr_path_prefix: /flaresolverr`), but this configuration has not been tested yet.

For additional configuration options, refer to the [ansible-role-flaresolverr](https://github.com/sudo-Tiz/ansible-role-flaresolverr)'s `defaults/main.yml` file.

## Recommended other services

Consider these other related services:

- [Autobrr](autobrr.md)
- [Jackett](jackett.md)
- [Jellyfin](jellyfin.md)
- [Jellyseerr](jellyseerr.md)
- [qBittorrent](qbittorrent.md)
- [Radarr](radarr.md)
- [Sonarr](sonarr.md)
