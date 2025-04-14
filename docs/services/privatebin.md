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
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-privatebin/blob/main/docs/configuring-privatebin.md) online
- 📁 `roles/galaxy/privatebin/docs/configuring-privatebin.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server
- (optional) MySQL / [MariaDB](mariadb.md) database
- (optional) [Postgres](postgres.md) database — required on the default configuration
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

### Configure a storage for pastes (optional)

PrivateBin instance requires a storage backend to work. The available options: PostgreSQL (default), local filesystem, MySQL, SQLite, Google Cloud Storage, and Amazon S3.

As the playbook enables the [PostgreSQL service](postgres.md) on `vars.yml` by default, it is configured to use it as the default backend. If it is fine for you, you do not have to add configuration for the storage.

See below for the instruction to use one of the others.

#### Local filesystem

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

#### MySQL

To use MySQL for a storage, add the following configuration to your `vars.yml` file:

```yaml
privatebin_config_model: MySQL
```

See [here](mariadb.md) on the role's documentation for details about how to configure a MariaDB instance with the playbook.

#### Google Cloud Storage / Amazon S3

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-privatebin/blob/main/docs/configuring-privatebin.md#configure-a-storage-for-pastes) on the role's documentation for details about how to configure a storage at Google Cloud Storage or Amazon S3.

### Configure a URL shortener (optional)

It is possible to have the PrivateBin instance use a URL shortener such as Bit.ly and a [YOURLS](https://yourls.org) instance, so that users can shorten a URL of a paste with it. **It is recommended to use a self-hosted shortener only and set a password to a paste, as the shortener will leak the paste's encryption key.**

YOURLS is available on the playbook. See [here](yourls.md) for details about how to install it.

**Notes**
- YOURLS requires a MariaDB instance (see [here](mariadb.md) for details about configuring it with the playbook); if PostgreSQL is going to be used for PrivateBin (or other services), you need to use both of them.
- If you are going to install PrivateBin and YOURLS at the same time, **you need to complete installation of YOURLS at first** by visiting its admin UI available at the specified hostname with `/admin/` such as `yourls.example.com/admin/`. Otherwise the function to shorten a paste's URL does not work. See [here](yourls.md#usage) for the instruction to complete instalation.

#### Use a private YOURLS instance with API access key

If you are using the private YOURLS instance, you might probably want to disallow a third party to use it without credentials. You can configure authentication by adding the following configuration to your `vars.yml` file:

```yaml
privatebin_config_yourlsapi_enabled: true

# Set the "signature" (access key) issued by the YOURLS instance for using the account
privatebin_config_yourlsapi_signature: ''

# Set URL of the YOURLS instance's API, called to shorten a paste URL
privatebin_config_yourlsapi_url: https://yourls.example.com/yourls-api.php
```

You can find the "signature" and API's URL on the "Tools" page of the YOURLS instance.

### Extending the configuration

There are some additional things you may wish to configure about the component.

Take a look at:

- [PrivateBin](https://github.com/mother-of-all-self-hosting/ansible-role-privatebin)'s [`defaults/main.yml`](https://github.com/mother-of-all-self-hosting/ansible-role-privatebin/blob/main/defaults/main.yml) for some variables that you can customize via your `vars.yml` file.

See its [configuration sample file](https://github.com/PrivateBin/PrivateBin/blob/master/cfg/conf.sample.php) and the [documentation](https://github.com/PrivateBin/PrivateBin/wiki/Configuration) for a complete list of PrivateBin's config options such as [discussion](https://github.com/mother-of-all-self-hosting/ansible-role-privatebin/blob/main/docs/configuring-privatebin.md#configure-the-discussion-feature-optional), [password](https://github.com/mother-of-all-self-hosting/ansible-role-privatebin/blob/main/docs/configuring-privatebin.md#configure-the-password-feature-optional), [file upload](https://github.com/mother-of-all-self-hosting/ansible-role-privatebin/blob/main/docs/configuring-privatebin.md#configure-the-file-upload-feature-optional), and [default theme](https://github.com/mother-of-all-self-hosting/ansible-role-privatebin/blob/main/docs/configuring-privatebin.md#configure-the-default-template-optional) features.

## Usage

After running the command for installation, PrivateBin becomes available at the specified hostname with the prefix (`mash.example.com/bin`).

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-privatebin/blob/main/docs/configuring-privatebin.md#troubleshooting) on the role's documentation for details.
