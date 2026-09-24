<!--
SPDX-FileCopyrightText: 2025 MASH project contributors
SPDX-FileCopyrightText: 2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Plex Media Server

The playbook can install and configure a standalone [Plex Media Server](https://docs.linuxserver.io/images/docker-plex) for you.

Plex is a personal media server that allows you to organize and stream your collection of movies, TV shows, music, and photos.

See the project's [documentation](https://docs.linuxserver.io/images/docker-plex/) to learn what Plex Media Server does and why it might be useful to you.

For details about configuring the [Ansible role for Plex Media Server](https://github.com/spatterIight/ansible-role-plex), you can check them via:

- 🌐 [the role's documentation](https://github.com/spatterIight/ansible-role-plex/blob/main/docs/configuring-plex.md) online
- 📁 `roles/galaxy/plex/docs/configuring-plex.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# plex                                                                 #
#                                                                      #
########################################################################

plex_enabled: true

plex_hostname: plex.example.com

########################################################################
#                                                                      #
# /plex                                                                #
#                                                                      #
########################################################################
```

Refer to [this section](https://github.com/spatterIight/ansible-role-plex/blob/main/docs/configuring-plex.md#adjusting-the-playbook-configuration) on the role's documentation for details about other settings.

## Usage

After running the command for installation, the Plex instance becomes available at the URL specified with `plex_hostname`. With the configuration above, the service is hosted at `https://plex.example.com`.

## Related services

- "* Arr" applications — [Autobrr](autobrr.md) / [Homarr](homarr.md) / [Radarr](radarr.md) / [Sonarr](sonarr.md)
- [Jackett](jackett.md)
- [Jellyfin](jellyfin.md)
- [Seerr](seerr.md)
- [qBittorrent](qbittorrent.md)
