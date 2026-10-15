<!--
SPDX-FileCopyrightText: 2026 spatterlight

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Prowlarr

The playbook can install and configure [Prowlarr](https://prowlarr.com/) for you.

Prowlarr is an indexer manager/proxy for Usenet and BitTorrent users. It manages your indexers in one place and syncs them to applications such as [Sonarr](sonarr.md) and [Radarr](radarr.md).

See the project's [documentation](https://wiki.servarr.com/prowlarr) to learn what Prowlarr does and why it might be useful to you.

For details about configuring the [Ansible role for Prowlarr](https://github.com/mother-of-all-self-hosting/ansible-role-prowlarr), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-prowlarr/blob/main/docs/configuring-prowlarr.md) online
- 📁 `roles/galaxy/prowlarr/docs/configuring-prowlarr.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# prowlarr                                                             #
#                                                                      #
########################################################################

prowlarr_enabled: true

prowlarr_hostname: prowlarr.example.com

########################################################################
#                                                                      #
# /prowlarr                                                            #
#                                                                      #
########################################################################
```

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-prowlarr/blob/main/docs/configuring-prowlarr.md#adjusting-the-playbook-configuration) on the role's documentation for details about other settings such as configuring trusted networks and HTTP Basic authentication.

### Connecting to Sonarr, Radarr and Lidarr

Prowlarr shares the container network of Traefik with the [Sonarr](sonarr.md), [Radarr](radarr.md) and [Lidarr](lidarr.md) instances installed by the playbook, so they can reach each other by container name.

To add one of them, open `Settings > Apps` in Prowlarr and click the `+` button. Set the `Prowlarr Server` field to `http://mash-prowlarr:9696`, and the application's server field to `http://mash-sonarr:8989`, `http://mash-radarr:7878` or `http://mash-lidarr:8686`. If a path prefix is set for either side, append it to that URL.

If [FlareSolverr](flaresolverr.md) is enabled as well, it can be added as an indexer proxy under `Settings > Indexers` with the host `http://mash-flaresolverr:8191`.

## Usage

After running the command for installation, the Prowlarr instance becomes available at the URL specified with `prowlarr_hostname`. With the configuration above, the service is hosted at `https://prowlarr.example.com`.

To get started, open the URL with a web browser to create an account.

## Troubleshooting

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-prowlarr/blob/main/docs/configuring-prowlarr.md#troubleshooting) on the role's documentation for details.

## Related services

- "* Arr" applications — [Lidarr](lidarr.md) / [Radarr](radarr.md) / [Sonarr](sonarr.md)
- [FlareSolverr](flaresolverr.md)
- [Jackett](jackett.md)
- [qBittorrent](qbittorrent.md)
