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
SPDX-FileCopyrightText: 2023 Alejandro AR
SPDX-FileCopyrightText: 2023 Antonis Christofides
SPDX-FileCopyrightText: 2023 Felix Stupp
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 MASH project contributors
SPDX-FileCopyrightText: 2024 Thomas Miceli
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# WriteFreely

The playbook can install and configure [WriteFreely](https://writefreely.org) for you.

WriteFreely is free and open source software for easily publishing writing on the web.

See the project's [documentation](https://writefreely.org/docs) to learn what WriteFreely does and why it might be useful to you.

For details about configuring the [Ansible role for WriteFreely](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az2i8BkHXzRvK1ZtGwHuvLACRswXgA), you can check them via:

- 🌐 [the role's documentation](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az2i8BkHXzRvK1ZtGwHuvLACRswXgA/tree/docs/configuring-writefreely.md) online
- 📁 `roles/galaxy/writefreely/docs/configuring-writefreely.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- MySQL / [MariaDB](mariadb.md) / [SQLite](https://www.sqlite.org/) database
- [Traefik](traefik.md) reverse-proxy server
- (optional) [exim-relay](exim-relay.md) mailer

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# writefreely                                                          #
#                                                                      #
########################################################################

writefreely_enabled: true

writefreely_hostname: writefreely.example.com

########################################################################
#                                                                      #
# /writefreely                                                         #
#                                                                      #
########################################################################
```

**Note**: hosting WriteFreely under a subpath (by configuring the `writefreely_path_prefix` variable) does not seem to be possible due to WriteFreely's technical limitations. See [this issue](https://github.com/mother-of-all-self-hosting/mash-playbook/issues/116) for details.

### Specify database

It is necessary to select database used by WriteFreely from a MySQL compatible database and SQLite.

To use a MySQL compatible database, add the following configuration to your `vars.yml` file:

```yaml
writefreely_database_type: mysql
```

Set `sqlite3` to use SQLite. The SQLite database is stored in the directory specified with `writefreely_data_path`.

### Configuring the mailer (optional)

On WriteFreely you can set up a mailer for functions such as password recovery. If you enable the [exim-relay](exim-relay.md) service in your inventory configuration, the playbook will automatically configure it as a mailer for the service.

To actually have the service use (and get messages sent through the exim-relay service), you will need to adjust settings on the service's UI after the service is installed.

>[!WARNING]
> Without setting an authentication method such as DKIM, SPF, and DMARC for your hostname, emails are most likely to be quarantined as spam at recipient's mail servers. The worst scenario is that your server's IP address or hostname will be included in the spam list such as the one managed by [Spamhaus](https://www.spamhaus.org/), depending on the reputation. As the exim-relay service supports DKIM signing, refer to [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay/blob/main/docs/configuring-exim-relay.md#enable-dkim-support-optional) for details about how to set it up.

### Using an unofficial Docker image (optional)

By default the service is configured to use the Docker image locally built on the source code using [this Dockerfile](https://github.com/writefreely/writefreely/blob/develop/Dockerfile) provided by the author.

As the official Docker image is not available, the role to install the service supports [this unofficial Docker image](https://hub.docker.com/r/jrasanen/writefreely) for user's convenience. See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az2i8BkHXzRvK1ZtGwHuvLACRswXgA/tree/docs/configuring-writefreely.md#using-an-unofficial-docker-image-optional) for details about how to use it.

## Usage

After running the command for installation, the WriteFreely instance becomes available at the URL specified with `writefreely_hostname`. With the configuration above, the service is hosted at `https://writefreely.example.com`.

To get started, you need to create an account on the instance. See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az2i8BkHXzRvK1ZtGwHuvLACRswXgA/tree/docs/configuring-writefreely.md#creating-a-user) on the role's documentation for details about how to create an account.

After creating one, open the URL with a web browser to log in to the instance with the account.

## Maintenance

It is possible to run maintenance tasks as documented in [this manual page](https://writefreely.org/docs/main/admin/commands) by running the `command-writefreely` tag, setting the `command` extra variable.

For example, you can execute `user --help` by running the command below (mind quotes):

```sh
ansible-playbook -i inventory/hosts setup.yml --tags=command-writefreely -e command="'user --help'"
```

## Related services

- [WordPress](wordpress.md) — Web content management system
