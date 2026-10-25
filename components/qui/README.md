<!--
SPDX-FileCopyrightText: 2026 spatterlight

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# qui

The playbook can install and configure [qui](https://getqui.com/) for you.

qui is a fast, modern web interface for [qBittorrent](../qbittorrent/README.md), which can manage multiple qBittorrent instances from a single place.

See the project's [documentation](https://getqui.com/docs/intro/) to learn what qui does and why it might be useful to you.

For details about configuring the [Ansible role for qui](https://github.com/mother-of-all-self-hosting/ansible-role-qui), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-qui/blob/main/docs/configuring-qui.md) online
- 📁 `roles/galaxy/qui/docs/configuring-qui.md` locally, if you have [fetched the Ansible roles](../../docs/installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](../traefik/README.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../../docs/installing.md) process:

```yaml
########################################################################
#                                                                      #
# qui                                                                  #
#                                                                      #
########################################################################

qui_enabled: true

qui_hostname: qui.example.com

########################################################################
#                                                                      #
# /qui                                                                 #
#                                                                      #
########################################################################
```

### Connecting to qBittorrent

If [qBittorrent](../qbittorrent/README.md) is enabled as well, the playbook wires qui to it automatically: qui joins qBittorrent's container network and starts along with it.

qui's Local Filesystem Access features additionally need qBittorrent's download directory mounted into qui. Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-qui/blob/main/docs/configuring-qui.md#enabling-local-filesystem-access-optional) on the role's documentation for details.

## Usage

After running the command for installation, the qui instance becomes available at the URL specified with `qui_hostname`. With the configuration above, the service is hosted at `https://qui.example.com`.

To get started, open the URL with a web browser to create an account. As whoever opens it first can claim the instance, it is recommended to do so immediately after installing.

To add the qBittorrent instance installed by the playbook, open `Settings > Instances`, click `Add Instance` and set the `URL` field to `http://mash-qbittorrent:8080`.

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-qui/blob/main/docs/configuring-qui.md#usage) on the role's documentation for details about the usage.

## Troubleshooting

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-qui/blob/main/docs/configuring-qui.md#troubleshooting) on the role's documentation for details.

## Related services

- [Autobrr](../autobrr/README.md) — Download automation for torrents and Usenet
- [qBittorrent](../qbittorrent/README.md) — A BitTorrent client
- [Radarr](../radarr/README.md) — Movie organizer/manager for Usenet and BitTorrent users
- [Sonarr](../sonarr/README.md) — PVR for newsgroup and BitTorrent users
