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

# Pocket ID

The playbook can install and configure [Pocket ID](https://pocket_id.dev) for you.

Pocket ID is a highly customizable dashboard for management of your favorite applications and services with a drag-and-drop grid system, which integrates with various self-hosted applications.

See the project's [documentation](https://pocket_id.dev/docs/getting-started) to learn what Pocket ID does and why it might be useful to you.

For details about configuring the [Ansible role for Pocket ID](https://github.com/mother-of-all-self-hosting/ansible-role-pocket_id), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-pocket_id/blob/main/docs/configuring-pocket_id.md) online
- 📁 `roles/galaxy/pocket_id/docs/configuring-pocket_id.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server
- (optional) [Postgres](postgres.md) / MySQL database — Pocket ID will default to [SQLite](https://www.sqlite.org/) if Postgres is not enabled

>[!NOTE]
> Currently (as of v1.35.0) MariaDB is not supported but planned. See [this issue at GitHub](https://github.com/pocket_id-labs/pocket_id/issues/2305) for the latest information.

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# pocket_id                                                            #
#                                                                      #
########################################################################

pocket_id_enabled: true

pocket_id_hostname: pocket_id.example.com

########################################################################
#                                                                      #
# /pocket_id                                                           #
#                                                                      #
########################################################################
```

**Note**: hosting Pocket ID under a subpath (by configuring the `pocket_id_path_prefix` variable) does not seem to be possible due to Pocket ID's technical limitations.

### Set 32-byte hex digits for secret key

You also need to specify **32-byte hex digits** to encrypt integration secrets on the database. To do so, add the following configuration to your `vars.yml` file. The value can be generated with `openssl rand -hex 32` or in another way.

```yaml
pocket_id_environment_variables_secret_encryption_key: YOUR_SECRET_KEY_HERE
```

>[!NOTE]
> Other type of values such as one generated with `pwgen -s 64 1` does not work.

### Select database to use (optional)

By default Pocket ID is configured to use Postgres, but you can choose other database such as SQLite and MySQL.

To use SQLite, add the following configuration to your `vars.yml` file:

```yaml
forgejo_database_type: better-sqlite3
```

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-pocket_id/blob/main/docs/configuring-pocket_id.md#specify-database-optional) on the role's documentation for details.

## Usage

After running the command for installation, the Pocket ID instance becomes available at the URL specified with `pocket_id_hostname`. With the configuration above, the service is hosted at `https://pocket_id.example.com`.

You can open the page with a web browser to start the onboarding process. See [this official guide](https://pocket_id.dev/docs/getting-started/after-the-installation/) for details.

### Playbook's services on Pocket ID

On Pocket ID's board it is possible to create and add icons of many services, including the ones which can be installed with this playbook such as [Nextcloud](nextcloud.md), [PeerTube](peertube.md), [PrivateBin](privatebin.md), [Syncthing](syncthing.md), etc.

Pocket ID also integrates with various software, to which you can connect your applications to interact via widgets. Here is a list of integrations which are also available on this playbook:

- **Torrent client**: [qBittorent](qbittorrent.md)
- **Media server**: [Plex](plex.md)
- **Media collection managers**: [Sonarr](sonarr.md) and [Radarr](radarr.md)
- **Media request manager**: [Overseerr](overseerr.md)
- **DNS ad-blocker**: [AdGuard Home](adguard-home.md)

See [this page](https://pocket_id.dev/docs/category/integrations) on the official documentation for the latest information about integrations.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-pocket_id/blob/main/docs/configuring-pocket_id.md#troubleshooting) on the role's documentation for details.
