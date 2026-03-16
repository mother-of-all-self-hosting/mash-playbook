<!--
SPDX-FileCopyrightText: 2020 Aaron Raimist
SPDX-FileCopyrightText: 2020 Chris van Dijk
SPDX-FileCopyrightText: 2020 Dominik Zajac
SPDX-FileCopyrightText: 2020 Mickaël Cornière
SPDX-FileCopyrightText: 2020-2024 MDAD project contributors
SPDX-FileCopyrightText: 2020-2025 Slavi Pantaleev
SPDX-FileCopyrightText: 2022 François Darveau
SPDX-FileCopyrightText: 2022 Julian Foad
SPDX-FileCopyrightText: 2022 Warren Bailey
SPDX-FileCopyrightText: 2023 Antonis Christofides
SPDX-FileCopyrightText: 2023 Felix Stupp
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 MASH project contributors
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 Sergio Durigan Junior
SPDX-FileCopyrightText: 2024 Thomas Miceli
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Healthchecks

The playbook can install and configure [Healthchecks](https://healthchecks.io/) for you.

Healthchecks is a cron job monitoring software.

See the project's [documentation](https://healthchecks.io/docs/) to learn what Healthchecks does and why it might be useful to you.

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server
- (optional) [exim-relay](exim-relay.md) mailer
- (optional) [Gotify](gotify.md)
- (optional) [ntfy](ntfy.md)
- (optional) [Postgres](postgres.md) / MySQL / [MariaDB](mariadb.md) database — Healthchecks will default to [SQLite](https://www.sqlite.org/) if Postgres is not enabled

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# healthchecks                                                         #
#                                                                      #
########################################################################

healthchecks_enabled: true

healthchecks_hostname: mash.example.com
healthchecks_path_prefix: /healthchecks

########################################################################
#                                                                      #
# /healthchecks                                                        #
#                                                                      #
########################################################################
```

### Select database to use (optional)

By default Healthchecks is configured to use Postgres, but you can choose other database such as SQLite and MySQL (MariaDB).

To use MariaDB, add the following configuration to your `vars.yml` file:

```yaml
healthchecks_database_type: mysql
```

### Configuring notification services (optional)

On Healthchecks you can add configuration settings of notification services. If you enable [exim-relay](exim-relay.md), [ntfy](ntfy.md), and/or [Gotify](gotify.md) services in your inventory configuration, the playbook will automatically connect them to the Healthchecks service.

As the Healthchecks instance does not support configuring the self-hosted ntfy or Gotify instances with environment variables, you can add default options for them on its UI. Refer to [this page](https://healthchecks.io/docs/configuring_notifications/) on the official documentation as well about how to configure them.

To set up other supported services, refer to the [upstream `.env.example` file](https://github.com/healthchecks/healthchecks/blob/master/docker/.env.example) for environment variables. You can pass those variables to the Healthchecks container with the `healthchecks_environment_variables_additional_variables` variable as below:

```yml
healthchecks_environment_variables_additional_variables: |
  DISCORD_CLIENT_ID=123
  DISCORD_CLIENT_SECRET=456
```

To actually have the services use (and get messages sent through them), you will need to adjust settings on the service's UI after the service is installed.

>[!WARNING]
> Without setting an authentication method such as DKIM, SPF, and DMARC for your hostname, emails are most likely to be quarantined as spam at recipient's mail servers. The worst scenario is that your server's IP address or hostname will be included in the spam list such as the one managed by [Spamhaus](https://www.spamhaus.org/), depending on the reputation. As the exim-relay service supports DKIM signing, refer to [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay/blob/main/docs/configuring-exim-relay.md#enable-dkim-support-optional) for details about how to set it up.

### Extending the configuration

There are some additional things you may wish to configure about the component.

Take a look at:

- [Healthcheck's](https://github.com/mother-of-all-self-hosting/ansible-role-healthchecks) [`defaults/main.yml`](https://github.com/mother-of-all-self-hosting/ansible-role-healthchecks/blob/main/defaults/main.yml) for some variables that you can customize via your `vars.yml` file.

## Usage

After running the command for installation, the Healthchecks instance becomes available at the URL specified with `healthchecks_hostname` and `healthchecks_path_prefix`. With the configuration above, the service is hosted at `https://mash.example.com/healthchecks`.

To get started, create a superuser account by running the command as below:

```sh
ansible-playbook -i inventory/hosts setup.yml --tags=createsuperuser-healthchecks -e email=EMAIL_ADDRESS_HERE -e password=PASSWORD_HERE
```

After creating the superuser account, you can open the URL to log in and start setting up monitoring tasks. You can create as many accounts as you wish.

## Recommended other services

- [Prometheus](prometheus.md) — a metrics collection and alerting monitoring solution
