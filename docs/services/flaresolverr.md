<!--
SPDX-FileCopyrightText: 2025 MASH project contributors
SPDX-FileCopyrightText: 2025 sudo-Tiz
SPDX-FileCopyrightText: 2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# FlareSolverr

The playbook can install and configure [FlareSolverr](https://github.com/FlareSolverr/FlareSolverr) for you.

FlareSolverr is an open-source proxy server to bypass Cloudflare protection.

See the project's [documentation](https://github.com/FlareSolverr/FlareSolverr/blob/master/README.md) to learn what FlareSolverr does and why it might be useful to you.

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

After running the installation command, the FlareSolverr instance becomes available internally at the `flaresolverr_container_http_port` value (default is **8191**) and is reachable from any other media service like [Jackett](jackett.md). If you need the container to be accessible from outside, you can use `flaresolverr_container_http_bind_port` or `flaresolverr_hostname`.

> **Note:**
> The `flaresolverr_path_prefix` variable can be adjusted to host under a subpath (e.g., `flaresolverr_path_prefix: /flaresolverr`), but this configuration has not been tested yet.

For additional configuration options, refer to the [ansible-role-flaresolverr](https://github.com/sudo-Tiz/ansible-role-flaresolverr)'s `defaults/main.yml` file.

## Related services

- "* Arr" applications — [Autobrr](autobrr.md) / [Homarr](homarr.md) / [Jellyseerr](jellyseerr.md) / [Overseerr](overseerr.md) / [Radarr](radarr.md) / [Sonarr](sonarr.md)
