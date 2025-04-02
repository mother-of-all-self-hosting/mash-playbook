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

# PrivateBin

The playbook can install and configure [PrivateBin](https://privatebin.info) for you.

PrivateBin is a minimalist, open source online pastebin where the server has zero knowledge of pasted data.

See the project's [documentation](https://github.com/PrivateBin/PrivateBin/tree/master/doc) to learn what PrivateBin does and why it might be useful to you.

For details about configuring the [Ansible role for PrivateBin](https://codeberg.org/acioustick/ansible-role-privatebin), you can check them via:
- 🌐 [the role's documentation](https://codeberg.org/acioustick/ansible-role-privatebin/src/branch/master/docs/configuring-privatebin.md) online
- 📁 `roles/galaxy/privatebin/docs/configuring-privatebin.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server
- (optional) MySQL / [MariaDB](mariadb.md) database
- (optional) [Postgres](postgres.md) database
- (optional) [YOURLS](yourls.md)

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# privatebin                                                           #
#                                                                      #
########################################################################

privatebin_enabled: true

privatebin_hostname: mash.example.com
privatebin_path_prefix: bin

########################################################################
#                                                                      #
# /privatebin                                                          #
#                                                                      #
########################################################################
```

### Configure a storage for pastes

PrivateBin instance requires a storage backend to work. The available options: local filesystem (default), PostgreSQL, MySQL, SQLite, Google Cloud Storage, and Amazon S3.

#### Local filesystem (default)

To use local filesystem database for a storage, you need to add a Docker volume to mount in the container, so that the directory for storing files is shared with the host machine.

To add the volume, prepare a directory on the host machine and add the following configuration to your `vars.yml` file, setting the directory path to `src`:

```yaml
privatebin_container_additional_volumes:
  - type: bind
    src: /path/on/the/host
    dst: /srv/data
    options:
```

Make sure permissions of the directory specified to `src`. If not correctly specified, the service returns a permission error while trying to put data to it.

#### PostgreSQL

To use PostgreSQL for a storage, add the following configuration to your `vars.yml` file:

```yaml
privatebin_config_model: PostgreSQL
```

Make sure that PostgreSQL is enabled on `vars.yml`.

#### MySQL

To use MySQL for a storage, add the following configuration to your `vars.yml` file:

```yaml
privatebin_config_model: MySQL
```

You can enable a [MariaDB](mariadb.md) instance by adding the following configuration:

```yaml
########################################################################
#                                                                      #
# mariadb                                                              #
#                                                                      #
########################################################################

mariadb_enabled: true

# Put a strong password below, generated with `pwgen -s 64 1` or in another way
mariadb_root_password: ''

########################################################################
#                                                                      #
# /mariadb                                                             #
#                                                                      #
########################################################################
```

#### Google Cloud Storage / Amazon S3

See [this section](https://codeberg.org/acioustick/ansible-role-privatebin/src/branch/master/docs/configuring-privatebin.md#configure-a-storage-for-pastes) on the role's documentation for details about how to configure a storage at Google Cloud Storage or Amazon S3.

### Set the admin username and password

You also need to create an instance's user to access to the admin UI after installation. To create one, add the following configuration to your `vars.yml` file. Make sure to replace `YOUR_ADMIN_USERNAME_HERE` and `YOUR_ADMIN_PASSWORD_HERE`.

```yaml
privatebin_environment_variable_user: YOUR_ADMIN_USERNAME_HERE
privatebin_environment_variable_pass: YOUR_ADMIN_PASSWORD_HERE
```

## Usage

After running the command for installation, PrivateBin's admin UI is available at the specified hostname with `/admin/` such as `privatebin.example.com/admin/`.

First, open the page with a web browser to complete installation on the server by clicking "Install PrivateBin" button. After that, click the anchor link "PrivateBin Administration Page" to log in with the username (`privatebin_environment_variable_user`) and password (`privatebin_environment_variable_pass`).

The help file is available at `privatebin.example.com/readme.html`.

## Troubleshooting

See [this section](https://codeberg.org/acioustick/ansible-role-privatebin/src/branch/master/docs/configuring-privatebin.md#troubleshooting) on the role's documentation for details.
