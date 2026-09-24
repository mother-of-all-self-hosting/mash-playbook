<!--
SPDX-FileCopyrightText: 2025 MASH project contributors
SPDX-FileCopyrightText: 2025, 2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Sonarr

The playbook can install and configure [Sonarr](https://sonarr.tv/) for you.

Sonarr is a smart PVR for newsgroup and BitTorrent users.

See the project's [documentation](https://wiki.servarr.com/sonarr) to learn what Sonarr does and why it might be useful to you.

For details about configuring the [Ansible role for Sonarr](https://github.com/spatterIight/ansible-role-sonarr), you can check them via:

- 🌐 [the role's documentation](https://github.com/spatterIight/ansible-role-sonarr/blob/main/docs/configuring-sonarr.md) online
- 📁 `roles/galaxy/sonarr/docs/configuring-sonarr.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# sonarr                                                               #
#                                                                      #
########################################################################

sonarr_enabled: true

sonarr_hostname: sonarr.example.com

########################################################################
#                                                                      #
# /sonarr                                                              #
#                                                                      #
########################################################################
```

Refer to [this section](https://github.com/spatterIight/ansible-role-sonarr/blob/main/docs/configuring-sonarr.md#adjusting-the-playbook-configuration) on the role's documentation for details about other settings such as configuring trusted networks.

## Usage

After running the command for installation, the Sonarr instance becomes available at the URL specified with `sonarr_hostname`. With the configuration above, the service is hosted at `https://sonarr.example.com`.

To get started, open the URL with a web browser to create an account.

## Related services

- "* Arr" applications — [Autobrr](autobrr.md) / [Homarr](homarr.md) / [Radarr](radarr.md)
- [Jackett](jackett.md)
  - For Jackett integration instructions, refer to the [setup guide](https://github.com/spatterIight/ansible-role-jackett/blob/main/docs/configuring-jackett.md#integration-with-sonarrradarr) on the role's documentation
- [Jellyfin](jellyfin.md)
- [Seerr](seerr.md)
- [Plex](plex.md)
- [qBittorrent](qbittorrent.md)
  - For qBittorrent integration instructions, refer to the [setup guide](https://github.com/mother-of-all-self-hosting/ansible-role-qbittorrent/blob/main/docs/configuring-qbittorrent.md#integration-with-sonarrradarr) on the role's documentation
