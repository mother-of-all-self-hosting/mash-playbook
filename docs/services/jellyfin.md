<!--
SPDX-FileCopyrightText: 2025 MASH project contributors
SPDX-FileCopyrightText: 2025, 2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Jellyfin

The playbook can install and configure [Jellyfin](https://jellyfin.org/) for you.

Jellyfin is an open-source personal media server that allows you to organize and stream your collection of movies, TV shows, and music.

See the project's [documentation](https://jellyfin.org/docs/) to learn what Jellyfin does and why it might be useful to you.

For details about configuring the [Ansible role for Jellyfin](https://github.com/spatterIight/ansible-role-jellyfin), you can check them via:

- 🌐 [the role's documentation](https://github.com/spatterIight/ansible-role-jellyfin/blob/main/docs/configuring-jellyfin.md) online
- 📁 `roles/galaxy/jellyfin/docs/configuring-jellyfin.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# jellyfin                                                             #
#                                                                      #
########################################################################

jellyfin_enabled: true

jellyfin_hostname: jellyfin.example.com

########################################################################
#                                                                      #
# /jellyfin                                                            #
#                                                                      #
########################################################################
```

Refer to [this section](https://github.com/spatterIight/ansible-role-jellyfin/blob/main/docs/configuring-jellyfin.md#adjusting-the-playbook-configuration) on the role's documentation for details about other settings.

## Usage

After running the command for installation, the Jellyfin instance becomes available at the URL specified with `jellyfin_hostname`. With the configuration above, the service is hosted at `https://jellyfin.example.com`.

## Related services

- "* Arr" applications — [Autobrr](autobrr.md) / [Homarr](homarr.md) / [Radarr](radarr.md) / [Sonarr](sonarr.md)
- [Feishin](feishin.md) — Music player for Navidrome, Jellyfin, Funkwhale, etc.
- [Jackett](jackett.md)
- [Seerr](seerr.md)
- [Plex](plex.md)
- [qBittorrent](qbittorrent.md)
