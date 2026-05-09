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
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 Thomas Miceli
SPDX-FileCopyrightText: 2024 Tiz
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Mobilizon

The playbook can install and configure [Mobilizon](https://joinmobilizon.org/en/) for you.

Mobilizon is a ActivityPub/Fediverse server to create and share events.

See the project's [documentation](https://docs.mobilizon.org/) to learn what Mobilizon does and why it might be useful to you.

For details about configuring the [Ansible role for Mobilizon](https://github.com/mother-of-all-self-hosting/ansible-role-mobilizon), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-mobilizon/blob/main/docs/configuring-mobilizon.md) online
- 📁 `roles/galaxy/mobilizon/docs/configuring-mobilizon.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Postgres database with PostGIS extensions installed](postgis.md)
- [Traefik](traefik.md) reverse-proxy server
- (optional) [exim-relay](exim-relay.md) mailer

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# mobilizon                                                            #
#                                                                      #
########################################################################

mobilizon_enabled: true

mobilizon_hostname: mobilizon.example.com

########################################################################
#                                                                      #
# /mobilizon                                                           #
#                                                                      #
########################################################################
```

>[!WARNING]
> Do not change the hostname after the instance has already run once. If changed, the Mobilizon instance stops working properly!

### Set a random string

You also need to set a random string to the variable as below by adding the following configuration to your `vars.yml` file. The value can be generated with `pwgen -s 64 1` or in another way.

```yaml
mobilizon_environment_variables_secret_key_base: YOUR_SECRET_KEY_HERE
```

### Enabling signing up

By default account registration for the service is disabled. To enable it, add the following configuration to your `vars.yml` file:

```yaml
mobilizon_environment_variables_registrations_open: true
```

### Configuring the mailer (optional)

On Mobilizon you can set up a mailer for functions such as password recovery. If you enable the [exim-relay](exim-relay.md) service in your inventory configuration, the playbook will automatically configure it as a mailer for the service.

>[!WARNING]
> Without setting an authentication method such as DKIM, SPF, and DMARC for your hostname, emails are most likely to be quarantined as spam at recipient's mail servers. The worst scenario is that your server's IP address or hostname will be included in the spam list such as the one managed by [Spamhaus](https://www.spamhaus.org/), depending on the reputation. As the exim-relay service supports DKIM signing, refer to [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay/blob/main/docs/configuring-exim-relay.md#enable-dkim-support-optional) for details about how to set it up.

### Usage

After running the command for installation, the Mobilizon instance becomes available at the URL specified with `mobilizon_hostname`. With the configuration above, the service is hosted at `https://mobilizon.example.com`.

To get started, create a user first and open the URL with a web browser to log in to the instance. You can create one on the web UI if `mobilizon_environment_variables_registrations_open` is set to `true`.

Alternatively, you can run the playbook with the `create-user-mobilizon` or `ensure-mobilizon-users-created` tag to create users. See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-mobilizon/blob/main/docs/configuring-mobilizon.md#creating-users) on the role's documentation for details.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-mobilizon/blob/main/docs/configuring-mobilizon.md#troubleshooting) on the role's documentation for details.
