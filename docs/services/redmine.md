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
SPDX-FileCopyrightText: 2023 Nikita Chernyi
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 Thomas Miceli
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Redmine

The playbook can install and configure [Redmine](https://redmine.org/) for you.

Redmine is a project management web application.

See the project's [documentation](https://www.redmine.org/projects/redmine/wiki) to learn what Redmine does and why it might be useful to you.

## Dependencies

This service requires the following other services:

- [Postgres](postgres.md) / MySQL / [MariaDB](mariadb.md) / [SQLite](https://www.sqlite.org/) / SQL Server database — Redmine will default to Postgres
- [Traefik](traefik.md) reverse-proxy server
- (optional) [exim-relay](exim-relay.md) mailer

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# redmine                                                              #
#                                                                      #
########################################################################

redmine_enabled: true

redmine_hostname: redmine.example.com

# If you'll be installing Redmine plugins which pull Ruby gems,
# which need to compile native code, consider installing build tools in the container image,
# by uncommenting the line below.
# redmine_container_image_customizations_build_tools_installation_enabled: true

########################################################################
#                                                                      #
# /redmine                                                             #
#                                                                      #
########################################################################
```

### Select database to use (optional)

By default Redmine is configured to use Postgres, but you can choose other database such as a MySQL compatible database, SQLite, and SQL Server.

To use MySQL, add the following configuration to your `vars.yml` file:

```yaml
redmine_database_type: mysql
```

Set `sqlite` to use SQLite, and `sqlserver` to use SQL Server.

### Configuring the mailer (optional)

On Redmine you can set up a mailer for functions such as password recovery. If you enable the [exim-relay](exim-relay.md) service in your inventory configuration, the playbook will automatically configure it as a mailer for the service.

To actually have the service use (and get messages sent through the exim-relay service), you will need to adjust settings on the service's UI after the service is installed.

>[!WARNING]
> Without setting an authentication method such as DKIM, SPF, and DMARC for your hostname, emails are most likely to be quarantined as spam at recipient's mail servers. The worst scenario is that your server's IP address or hostname will be included in the spam list such as the one managed by [Spamhaus](https://www.spamhaus.org/), depending on the reputation. As the exim-relay service supports DKIM signing, refer to [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay/blob/main/docs/configuring-exim-relay.md#enable-dkim-support-optional) for details about how to set it up.

## Usage

After running the command for installation, the Redmine instance becomes available at the URL specified with `redmine_hostname`. With the configuration above, the service is hosted at `https://redmine.example.com`.

To get started, open the URL with a web browser to log in to the instance with the administrator account, registered automatically on the initial run. Its credentials can be found at <https://hub.docker.com/_/redmine#accessing-the-application>. When logging in, you are required to reset the default password.
