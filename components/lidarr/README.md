<!--
SPDX-FileCopyrightText: 2025 MASH project contributors
SPDX-FileCopyrightText: 2025, 2026 Suguru Hirahara
SPDX-FileCopyrightText: 2026 Sudo-Tiz
SPDX-FileCopyrightText: 2026 sudo-Tiz

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Lidarr

The playbook can install and configure [Lidarr](https://lidarr.audio/) for you.

Lidarr is a music collection manager for Usenet and BitTorrent users.

See the project's [documentation](https://wiki.servarr.com/lidarr) to learn what Lidarr does and why it might be useful to you.

## Dependencies

This service requires the following other services:

- [Traefik](../traefik/README.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../../docs/installing.md) process:

```yaml
########################################################################
#                                                                      #
# lidarr                                                               #
#                                                                      #
########################################################################

lidarr_enabled: true

lidarr_hostname: lidarr.example.com

# To mount additional data directories, use `lidarr_container_additional_volumes_custom`
#
# Example:
# lidarr_container_additional_volumes_custom:
#   - type: bind
#     src: /path/on/the/host
#     dst: /data
#   - type: bind
#     src: /another-path/on/the/host
#     dst: /read-only
#     options: readonly

########################################################################
#                                                                      #
# /lidarr                                                              #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the Lidarr instance becomes available at the URL specified with `lidarr_hostname`. With the configuration above, the service is hosted at `https://lidarr.example.com`.

>[!NOTE]
> The `lidarr_path_prefix` variable can be adjusted to host under a subpath (e.g. `lidarr_path_prefix: /lidarr`).

Lidarr starts without authentication and does not prompt you to create an account. Before exposing the hostname, [configure authentication as described by the Lidarr role](https://github.com/mother-of-all-self-hosting/ansible-role-lidarr/blob/v3.1.0.4875-3/docs/configuring-lidarr.md#protecting-the-web-interface).

For additional configuration options, refer to `defaults/main.yml` file.

## Related services

- "* Arr" applications — [Autobrr](../autobrr/README.md) / [Homarr](../homarr/README.md) / [Prowlarr](../prowlarr/README.md) / [Radarr](../radarr/README.md) / [Sonarr](../sonarr/README.md)
- [Jellyfin](../jellyfin/README.md)
- [Plex](../plex/README.md)
- [qBittorrent](../qbittorrent/README.md)
- [Unpackerr](../unpackerr/README.md)
