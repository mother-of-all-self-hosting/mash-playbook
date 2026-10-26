<!--
SPDX-FileCopyrightText: 2025 MASH project contributors
SPDX-FileCopyrightText: 2025 spatterlight
SPDX-FileCopyrightText: 2025, 2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Radarr

The playbook can install and configure [Radarr](https://radarr.video/) for you.

Radarr is a movie organizer/manager for Usenet and BitTorrent users.

See the project's [documentation](https://wiki.servarr.com/radarr) to learn what Radarr does and why it might be useful to you.

For details about configuring the [Ansible role for Radarr](https://github.com/mother-of-all-self-hosting/ansible-role-radarr), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-radarr/blob/main/docs/configuring-radarr.md) online
- 📁 `roles/galaxy/radarr/docs/configuring-radarr.md` locally, if you have [fetched the Ansible roles](../../docs/installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](../traefik/README.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../../docs/installing.md) process:

```yaml
########################################################################
#                                                                      #
# radarr                                                               #
#                                                                      #
########################################################################

radarr_enabled: true

radarr_hostname: radarr.example.com

########################################################################
#                                                                      #
# /radarr                                                              #
#                                                                      #
########################################################################
```

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-radarr/blob/main/docs/configuring-radarr.md#adjusting-the-playbook-configuration) on the role's documentation for details about other settings such as configuring trusted networks.

## Usage

After running the command for installation, the Radarr instance becomes available at the URL specified with `radarr_hostname`. With the configuration above, the service is hosted at `https://radarr.example.com`.

To get started, open the URL with a web browser to create an account.

## Related services

- "* Arr" applications — [Autobrr](../autobrr/README.md) / [Homarr](../homarr/README.md) / [Prowlarr](../prowlarr/README.md) / [Sonarr](../sonarr/README.md)
- [Jackett](../jackett/README.md)
  - For Jackett integration instructions, refer to the [setup guide](https://github.com/mother-of-all-self-hosting/ansible-role-jackett/blob/main/docs/configuring-jackett.md#integration-with-sonarrradarr) on the role's documentation
- [Jellyfin](../jellyfin/README.md)
- [Seerr](../seerr/README.md)
- [Plex](../plex/README.md)
- [qBittorrent](../qbittorrent/README.md)
  - For qBittorrent integration instructions, refer to the [setup guide](https://github.com/mother-of-all-self-hosting/ansible-role-qbittorrent/blob/main/docs/configuring-qbittorrent.md#integration-with-sonarrradarr) on the role's documentation
- [Unpackerr](../unpackerr/README.md)
