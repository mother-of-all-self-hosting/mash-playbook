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

For details about configuring the [Ansible role for Healthchecks](https://github.com/mother-of-all-self-hosting/ansible-role-healthchecks/), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-healthchecks/blob/main/docs/configuring-healthchecks.md) online
- 📁 `roles/galaxy/healthchecks/docs/configuring-healthchecks.md` locally, if you have [fetched the Ansible roles](../installing.md)

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

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-healthchecks/blob/main/docs/configuring-healthchecks.md#configuring-notification-services-optional) on the role's documentation for details about configuring other services.

## Usage

After running the command for installation, the Healthchecks instance becomes available at the URL specified with `healthchecks_hostname` and `healthchecks_path_prefix`. With the configuration above, the service is hosted at `https://mash.example.com/healthchecks`.

To get started, create a superuser account by running the command as below:

```sh
ansible-playbook -i inventory/hosts setup.yml --tags=create-admin-healthchecks -e email=EMAIL_ADDRESS_HERE -e password=PASSWORD_HERE
```

After creating the superuser account, you can open the URL to log in and start setting up monitoring tasks. You can create as many accounts as you wish.

## Related services

- [Prometheus](prometheus.md) — a metrics collection and alerting monitoring solution
