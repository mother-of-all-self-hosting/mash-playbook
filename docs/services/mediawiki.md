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
