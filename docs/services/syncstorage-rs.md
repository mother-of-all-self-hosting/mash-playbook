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

# syncstorage-rs

The playbook can install and configure [syncstorage-rs](https://github.com/mozilla-services/syncstorage-rs), Mozilla Sync Storage server in Rust used to power Firefox Sync, for you.

See the project's [documentation](https://github.com/mozilla-services/syncstorage-rs/blob/master/README.md) to learn what syncstorage-rs does and [syncstorage-rs-docker](https://codeberg.org/acioustick/syncstorage-rs-docker)'s documentation about how to set it up.

For details about configuring the [Ansible role for syncstorage-rs](https://github.com/mother-of-all-self-hosting/ansible-role-syncstorage-rs-docker), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-syncstorage-rs-docker/blob/main/docs/configuring-syncstorage-rs-docker.md) online
- 📁 `roles/galaxy/syncstorage_rs_docker/docs/configuring-syncstorage-rs-docker.md` locally, if you have [fetched the Ansible roles](../installing.md)

>[!NOTE]
> The role is configured to build the Docker image by default, as it is not provided by the upstream project. Before proceeding, make sure that the machine which you are going to run the Ansible commands against has sufficient computing power to build it.

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server
- MySQL / [MariaDB](mariadb.md) database

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# syncstorage-rs-docker                                                #
#                                                                      #
########################################################################

syncstorage_rs_docker_enabled: true

syncstorage_rs_docker_hostname: syncstorage.example.com

########################################################################
#                                                                      #
# /syncstorage-rs-docker                                               #
#                                                                      #
########################################################################
```

**Notes**:

- Hosting syncstorage-rs under a subpath (by configuring the `syncstorage_rs_docker_path_prefix` variable) does not seem to be possible due to syncstorage-rs's technical limitations.

## Usage

After running the command for installation, syncstorage-rs becomes available at the specified hostname such as `syncstorage.example.com`.

See [this section](https://codeberg.org/acioustick/syncstorage-rs-docker/src/branch/main#adjusting-firefox-setting) on the documentation for details about how to configure Firefox to have it use your server for data synchronization.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-syncstorage-rs-docker/blob/main/docs/configuring-syncstorage-rs-docker.md#troubleshooting) on the role's documentation for details.
