<!--
SPDX-FileCopyrightText: 2020 - 2024 MDAD project contributors
SPDX-FileCopyrightText: 2020 - 2025 Slavi Pantaleev
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
SPDX-FileCopyrightText: 2023 MASH project contributors
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara
SPDX-FileCopyrightText: 2024 Sergio Durigan Junior

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Healthchecks

[Healthchecks](https://healthchecks.io/) is simple and Effective **Cron Job Monitoring** solution.


## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server
- (optional) [Postgres](postgres.md) / MySQL / [MariaDB](mariadb.md) database — Healthchecks will default to [SQLite](https://www.sqlite.org/) if Postgres is not enabled
- (optional) the [exim-relay](exim-relay.md) mailer


## Configuration

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

### Authentication

The first superuser account is created after installation. See [Usage](#usage).
You can create as many accounts as you wish.

### Email integration

If you've enabled the [exim-relay](exim-relay.md) mailer service, Healthchecks will automatically be configured to send through it.

If you need to configure Healthchecks to send email directly, the [ansible.role.healthchecks](https://github.com/mother-of-all-self-hosting/ansible-role-healthchecks) Ansible role provides various variables for tweaking the email-sending configuration in its `default/main.yml` file (`healthchecks_environment_variable_default_from_email` and various `healthchecks_environment_variable_email_*` variables).

### Integrating with other services

Refer to the [upstream `.env.example` file](https://github.com/healthchecks/healthchecks/blob/master/docker/.env.example) for discovering additional environment variables.

You can pass these to the Healthchecks container using the `healthchecks_environment_variables_additional_variables` variable. Example:

```yml
healthchecks_environment_variables_additional_variables: |
  DISCORD_CLIENT_ID=123
  DISCORD_CLIENT_SECRET=456
```


## Usage

After running the command for installation, the Healthchecks instance becomes available at the URL specified with `healthchecks_hostname` and `healthchecks_path_prefix`. With the configuration above, the service is hosted at `https://mash.example.com/healthchecks`.

To get started, create a superuser account by running the command as below:

```sh
ansible-playbook -i inventory/hosts setup.yml --tags=createsuperuser-healthchecks -e email=EMAIL_ADDRESS_HERE -e password=PASSWORD_HERE`
```

After creating the superuser account, you can open the URL to log in and start setting up monitoring tasks.


## Recommended other services

- [Prometheus](prometheus.md) — a metrics collection and alerting monitoring solution
