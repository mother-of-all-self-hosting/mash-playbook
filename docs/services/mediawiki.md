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
SPDX-FileCopyrightText: 2024 Thomas Miceli
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# MediaWiki

The playbook can install and configure [MediaWiki](https://www.mediawiki.org/) for you.

MediaWiki is a popular free and open-source wiki software.

See the project's [documentation](https://www.mediawiki.org/wiki/MediaWiki) to learn what MediaWiki does and why it might be useful to you.

For details about configuring the [Ansible role for MediaWiki](https://github.com/mother-of-all-self-hosting/ansible-role-mediawiki), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-mediawiki/blob/main/docs/configuring-mediawiki.md) online
- 📁 `roles/galaxy/mediawiki/docs/configuring-mediawiki.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server
- [Postgres](postgres.md) / MySQL / [MariaDB](mariadb.md) / [SQLite](https://www.sqlite.org/) database

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file:

```yaml
########################################################################
#                                                                      #
# mediawiki                                                            #
#                                                                      #
########################################################################

mediawiki_enabled: true

mediawiki_hostname: mediawiki.example.com

########################################################################
#                                                                      #
# /mediawiki                                                           #
#                                                                      #
########################################################################
```

**Note**: hosting MediaWiki under a subpath (by configuring the `mediawiki_path_prefix` variable) does not seem to be possible due to MediaWiki's technical limitations.

### Set wiki's name

You also need to specify wiki's name by adding the following configuration to your `vars.yml` file:

```yaml
mediawiki_config_sitename: YOUR_WIKI_NAME_HERE
```

### Select database to use

It is necessary to select a database used by MediaWiki from a MySQL compatible database, Postgres, and SQLite. See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-mediawiki/blob/main/docs/configuring-mediawiki.md#specify-database) on the role's documentation for details.

>[!NOTE]
> It is [not recommended](https://www.mediawiki.org/wiki/Compatibility#Database) to use Postgres, as [this page](https://www.mediawiki.org/wiki/Postgres) on the manual describes that the Postgres support is "second-class" and you may run into some bugs.

#### Setting up a dedicated MariaDB instance

If you are going to use MariaDB, it is recommended to set up a dedicated MariaDB instance for MediaWiki to pin the MariaDB version for it, letting another instance on the latest version used by other services, as MariaDB 12.0.0+ is not supported by MediaWiki 1.44 due to [this bug](https://phabricator.wikimedia.org/T401570).

To create a dedicated instance for MediaWiki, you can follow the steps below:

1. Adjust the `hosts` file
2. Create a new `vars.yml` file for the dedicated instance
3. Edit the existing `vars.yml` file for the main host

##### Adjust `hosts`

At first, you need to adjust `inventory/hosts` file to add a supplementary host for MediaWiki.

The content should be something like below. Make sure to replace `mash.example.com` with your hostname and `YOUR_SERVER_IP_ADDRESS_HERE` with the IP address of the host, respectively. The same IP address should be set to both, unless the MariaDB instance will be served from a different machine.

```ini
[mash_servers]
[mash_servers:children]
mash_example_com

[mash_example_com]
mash.example.com ansible_host=YOUR_SERVER_IP_ADDRESS_HERE
mash.example.com-mediawiki-deps ansible_host=YOUR_SERVER_IP_ADDRESS_HERE
…
```

`mash_example_com` can be any string and does not have to match with the hostname.

You can just add an entry for the supplementary host to `[mash_example_com]` if there are other entries there already.

##### Create `vars.yml` for the dedicated instance

Then, create a new directory where `vars.yml` for the supplementary host is stored. If `mash.example.com` is your main host, name the directory as `mash.example.com-mediawiki-deps`. Its path therefore will be `inventory/host_vars/mash.example.com-mediawiki-deps`.

After creating the directory, add a new `vars.yml` file inside it with a content below. It will have running the playbook create a `mash-mediawiki-mariadb` instance on the new host, setting `/mash/mediawiki-mariadb` to the base directory of the dedicated MariaDB instance.

```yaml
# This is vars.yml for the supplementary host of MediaWiki.

---

########################################################################
#                                                                      #
# Playbook                                                             #
#                                                                      #
########################################################################

# Put a strong secret below, generated with `pwgen -s 64 1` or in another way
mash_playbook_generic_secret_key: RANDOM_STRING_HERE

# Override service names and directory path prefixes
mash_playbook_service_identifier_prefix: "mash-mediawiki-"
mash_playbook_service_base_directory_name_prefix: "mediawiki-"

########################################################################
#                                                                      #
# /Playbook                                                            #
#                                                                      #
########################################################################


########################################################################
#                                                                      #
# Various other overrides                                              #
#                                                                      #
########################################################################

# See: docs/configuring-ipv6.md
devture_systemd_docker_base_ipv6_enabled: true

########################################################################
#                                                                      #
# /Various other overrides                                             #
#                                                                      #
########################################################################


########################################################################
#                                                                      #
# mariadb                                                              #
#                                                                      #
########################################################################

mariadb_enabled: true

# Put a strong secret below, generated with `pwgen -s 64 1` or in another way
mariadb_root_password: RANDOM_STRING_FOR_MARIADB_HERE

# Pin the version because MariaDB 12.0.0+ is not supported by MediaWiki 1.44.
# See: https://phabricator.wikimedia.org/T401570
mariadb_container_image_latest: "{{ mariadb_container_image_v11_8 }}"

# Create a database for the MediaWiki instance
mariadb_managed_databases_custom:
  - name: "{{ mediawiki_database_name }}"
    username: "{{ mediawiki_database_mysql_username }}"
    password: "{{ mediawiki_database_mysql_password }}"

########################################################################
#                                                                      #
# /mariadb                                                             #
#                                                                      #
########################################################################


########################################################################
#                                                                      #
# mediawiki                                                            #
#                                                                      #
########################################################################

mediawiki_database_mysql_hostname: "{{ mariadb_connection_hostname }}"
mediawiki_database_mysql_port: "{{ mariadb_connection_port }}"

# Put a strong secret below, generated with `pwgen -s 64 1` or in another way
mediawiki_database_mysql_password: MARIADB_FOR_MEDIAWIKI_PASSWORD_HERE

########################################################################
#                                                                      #
# /mediawiki                                                           #
#                                                                      #
########################################################################
```

##### Edit the main `vars.yml` file

Having configured `vars.yml` for the dedicated instance, add the following configuration to `vars.yml` for the main host, whose path should be `inventory/host_vars/mash.example.com/vars.yml` (replace `mash.example.com` with yours).

```yaml
########################################################################
#                                                                      #
# mediawiki                                                            #
#                                                                      #
########################################################################

# Add the base configuration as specified above

mediawiki_database_type: mysql

# Point MediaWiki to its dedicated MariaDB instance
mediawiki_database_mysql_hostname: mash-mediawiki-mariadb

# Set the same value specified on vars.yml for the supplementary host
mediawiki_database_mysql_password: MARIADB_FOR_MEDIAWIKI_PASSWORD_HERE

# Make sure the MediaWiki service (mash-mediawiki.service) starts after its dedicated MariaDB service (mash-mediawiki-mariadb.service)
mediawiki_systemd_required_services_list_custom:
  - "mash-mediawiki-mariadb.service"

# Make sure the MediaWiki container is connected to the container network of its dedicated MariaDB service (mash-mediawiki-mariadb)
mediawiki_container_additional_networks_custom:
  - "mash-mediawiki-mariadb"

########################################################################
#                                                                      #
# /mediawiki                                                           #
#                                                                      #
########################################################################
```

After replacing strings with your values, running the installation command will create the dedicated MariaDB instance named `mash-mediawiki-mariadb`, and the MediaWiki instance will keep using the pinned MariaDB version.

### Set wiki's logos (recommended)

The default installation sets the placeholder icons for your wiki. Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-mediawiki/blob/main/docs/configuring-mediawiki.md#set-wikis-logos-recommended) on the role's documentation about how to replace them with yours.

### Extending the configuration

As the configuration settings specified on that file are basic despite being sufficient for starting up the instance, you would probably want to add other standard settings listed on [this section](https://www.mediawiki.org/wiki/Manual:LocalSettings.php#Standard_settings) on the manual to `mediawiki_config_additional_configurations` such as disabling user registration and enabling email functions, for example. See [this setcion](https://github.com/mother-of-all-self-hosting/ansible-role-mediawiki/blob/main/docs/configuring-mediawiki.md#extending-the-configuration) for details.

## Installation

Because installing a MediaWiki instance requires to invoke [`run.php install`](https://www.mediawiki.org/wiki/Manual:Install.php) and load the generated `LocalSettings.php` file on the container, installation process consists of multiple steps. **Running the [installing](../installing.md) command solely does not start up the MediaWiki instance.** Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-mediawiki/blob/main/docs/configuring-mediawiki.md#installing) for the instruction.

## Usage

After completing the steps for installation, the MediaWiki instance becomes available at the URL specified with `mediawiki_hostname`. With the configuration above, the service is hosted at `https://mediawiki.example.com`.

To get started, open the URL with a web browser to log in to the instance. **Note that the first registered user becomes an administrator automatically.**

## Maintenance

Some specific operations such as updating MediaWiki's configurations on [`LocalSettings.php`](https://www.mediawiki.org/wiki/Manual:LocalSettings.php) and upgrading the MediaWiki instance requires invoking specific commands with [`run.php`](https://www.mediawiki.org/wiki/Manual:Run.php) inside the container, which can be executed by running the playbook with special tags. Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-mediawiki/blob/main/docs/configuring-mediawiki.md#maintenance) for details.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-mediawiki/blob/main/docs/configuring-mediawiki.md#troubleshooting) on the role's documentation for details.

## Related services

- [An Otter Wiki](otterwiki.md) — Minimalistic wiki powered by Python, Markdown and Git
- [DokuWiki](dokuwiki.md) — Lightweight, file-based wiki engine
