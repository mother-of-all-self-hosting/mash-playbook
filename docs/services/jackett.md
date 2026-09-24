<!--
SPDX-FileCopyrightText: 2025 MASH project contributors
SPDX-FileCopyrightText: 2025, 2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Jackett

The playbook can install and configure [Jackett](https://github.com/Jackett/Jackett) for you.

Jackett is an API for your favorite Torrent trackers. It translates queries from apps ([Sonarr](https://github.com/Sonarr/Sonarr), [Radarr](https://github.com/Radarr/Radarr), etc.) into tracker-site-specific HTTP queries, parses the HTML or JSON response, and then sends results back to the requesting software.

See the project's [documentation](https://github.com/Jackett/Jackett/blob/master/README.md) to learn what Jackett does and why it might be useful to you.

For details about configuring the [Ansible role for Jackett](https://github.com/spatterIight/ansible-role-jackett), you can check them via:

- 🌐 [the role's documentation](https://github.com/spatterIight/ansible-role-jackett/blob/main/docs/configuring-jackett.md) online
- 📁 `roles/galaxy/jackett/docs/configuring-jackett.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# jackett                                                              #
#                                                                      #
########################################################################

jackett_enabled: true

jackett_hostname: jackett.example.com

########################################################################
#                                                                      #
# /jackett                                                             #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the Jackett instance becomes available at the URL specified with `jackett_hostname`. With the configuration above, the service is hosted at `https://jackett.example.com`.

To get started, open the URL with a web browser to create an administrator account.

## Related services

- "* Arr" applications — [Autobrr](autobrr.md) / [Homarr](homarr.md) / [Radarr](radarr.md) / [Sonarr](sonarr.md)
- [Jellyfin](jellyfin.md)
- [Seerr](seerr.md)
- [Plex](plex.md)
- [qBittorrent](qbittorrent.md)
