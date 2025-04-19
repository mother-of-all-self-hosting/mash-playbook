<!--
SPDX-FileCopyrightText: 2020 - 2024 MDAD project contributors
SPDX-FileCopyrightText: 2020 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2020 Aaron Raimist
SPDX-FileCopyrightText: 2020 Chris van Dijk
SPDX-FileCopyrightText: 2020 Dominik Zajac
SPDX-FileCopyrightText: 2020 Mickaël Cornière
SPDX-FileCopyrightText: 2022 François Darveau
SPDX-FileCopyrightText: 2022 Julian Foad
SPDX-FileCopyrightText: 2022 Warren Bailey
SPDX-FileCopyrightText: 2023 Antonis Christofides
SPDX-FileCopyrightText: 2023 Felix Stupp
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Homarr

The playbook can install and configure [Homarr](https://homarr.dev) for you.

Homarr is a highly customizable dashboard for management of your favorite applications and services with a drag-and-drop grid system, which integrates with various self-hosted applications.

See the project's [documentation](https://homarr.dev/docs/getting-started) to learn what Homarr does and why it might be useful to you.

For details about configuring the [Ansible role for Homarr](https://github.com/mother-of-all-self-hosting/ansible-role-homarr), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-homarr/blob/main/docs/configuring-homarr.md) online
- 📁 `roles/galaxy/homarr/docs/configuring-homarr.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# homarr                                                               #
#                                                                      #
########################################################################

homarr_enabled: true

homarr_hostname: homarr.example.com

########################################################################
#                                                                      #
# /homarr                                                              #
#                                                                      #
########################################################################
```

**Note**: hosting Homarr under a subpath (by configuring the `homarr_path_prefix` variable) does not seem to be possible due to Homarr's technical limitations.

### Set 32-byte hex digits for secret key

You also need to specify **32-byte hex digits** to encrypt integration secrets on the database. To do so, add the following configuration to your `vars.yml` file. The value can be generated with `openssl rand -hex 32` or in another way.

```yaml
homarr_environment_variables_secret_encryption_key: YOUR_SECRET_KEY_HERE
```

>[!NOTE]
> Other type of values such as one generated with `pwgen -s 64 1` does not work.

### Mount a directory for storing data

The service requires a Docker volume to be mounted, so that the directory for storing files is shared with the host machine.

To add the volume, prepare a directory on the host machine and add the following configuration to your `vars.yml` file, setting the directory path to `src`:

```yaml
homarr_data_path: /path/on/the/host
```

Make sure permissions of the directory specified to `src` (`/path/on/the/host`).

## Usage

After running the command for installation, Homarr becomes available at the specified hostname like `https://homarr.example.com`.

You can open the page with a web browser to start the onboarding process. See [this official guide](https://homarr.dev/docs/getting-started/after-the-installation/) for details.

### Playbook's services on Homarr

On Homarr's board it is possible to create and add icons of many services, including the ones which can be installed with this playbook such as [Nextcloud](nextcloud.md), [PeerTube](peertube.md), [PrivateBin](privatebin.md), [Syncthing](syncthing.md), etc.

Homarr also integrates with various software, to which you can connect your applications to interact via widgets. Here is a list of integrations which are also available on this playbook:

- **Torrent client**: [qBittorent](qbittorrent.md)
- **Media server**: [Plex](plex.md)
- **Media collection managers**: [Sonarr](sonarr.md) and [Radarr](radarr.md)
- **Media request manager**: [Overseerr](overseerr.md)
- **DNS ad-blocker**: [AdGuard Home](adguard-home.md)

See [this page](https://homarr.dev/docs/category/integrations) on the official documentation for the latest information about integrations.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-homarr/blob/main/docs/configuring-homarr.md#troubleshooting) on the role's documentation for details.
