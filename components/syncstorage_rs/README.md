<!--
SPDX-FileCopyrightText: 2020 Aaron Raimist
SPDX-FileCopyrightText: 2020 Chris van Dijk
SPDX-FileCopyrightText: 2020 Dominik Zajac
SPDX-FileCopyrightText: 2020 Mickaël Cornière
SPDX-FileCopyrightText: 2020-2024 MDAD project contributors
SPDX-FileCopyrightText: 2020-2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2022 François Darveau
SPDX-FileCopyrightText: 2022 Julian Foad
SPDX-FileCopyrightText: 2022 Warren Bailey
SPDX-FileCopyrightText: 2023 Antonis Christofides
SPDX-FileCopyrightText: 2023 Felix Stupp
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Syncstorage-rs

The playbook can install and configure [Syncstorage-rs](https://mozilla-services.github.io/syncstorage-rs/) for you.

Syncstorage-rs is a Mozilla Sync Storage server in Rust used to power Firefox Sync.

See the project's [documentation](https://mozilla-services.github.io/syncstorage-rs/) to learn what Syncstorage-rs does and why it might be useful to you.

For details about configuring the [Ansible role for syncstorage-rs](https://radicle.network/nodes/progressiv.radicle.garden/rad%3Az2BgqgDV3M1WeX9V3Y21yersbiCx7), you can check them via:

- 🌐 [the role's documentation](https://radicle.network/nodes/progressiv.radicle.garden/rad%3Az2BgqgDV3M1WeX9V3Y21yersbiCx7/tree/docs/configuring-syncstorage-rs.md) online
- 📁 `roles/galaxy/syncstorage_rs/docs/configuring-syncstorage-rs.md` locally, if you have [fetched the Ansible roles](../../docs/installing.md)

## Dependencies

This service requires the following other services:

- [Postgres](../postgres/README.md) / MySQL / [MariaDB](../mariadb/README.md) database
- [Traefik](../traefik/README.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../../docs/installing.md) process:

```yaml
########################################################################
#                                                                      #
# syncstorage_rs                                                       #
#                                                                      #
########################################################################

syncstorage_rs_enabled: true

syncstorage_rs_hostname: syncstorage-rs.example.com

########################################################################
#                                                                      #
# /syncstorage_rs                                                      #
#                                                                      #
########################################################################
```

**Note**: hosting Syncstorage-rs under a subpath (by configuring the `syncstorage_rs_path_prefix` variable) does not seem to be possible due to syncstorage-rs's technical limitations.

### Select database to use

Syncstorage-rs can use a MySQL compatible database or Postgres, and you need to choose one. Refer to [this section](https://radicle.network/nodes/progressiv.radicle.garden/rad%253Az2BgqgDV3M1WeX9V3Y21yersbiCx7/tree/docs/configuring-syncstorage-rs.md#specify-database) on the role's documentation for details.

### Set a random string

You also need to set a random string to the variable as below by adding the following configuration to your `vars.yml` file. The value can be generated with `pwgen -s 64 1` or in another way.

```yaml
syncstorage_rs_environment_variables_sync_master_secret: YOUR_SECRET_KEY_HERE
```

## Usage

After running the command for installation, the Syncstorage-rs instance becomes available at the URL specified with `syncstorage_rs_hostname`. With the configuration above, the service is hosted at `https://syncstorage-rs.example.com`.

Refer to [this section](https://mozilla-services.github.io/syncstorage-rs/how-to/how-to-run-with-docker.html#configuring-firefox-desktop) on the documentation for details about how to configure Firefox to have it use your server for data synchronization.

## Troubleshooting

Refer to [this section](https://radicle.network/nodes/progressiv.radicle.garden/rad%3Az2BgqgDV3M1WeX9V3Y21yersbiCx7/tree/docs/configuring-syncstorage-rs.md#troubleshooting) on the role's documentation for details.
