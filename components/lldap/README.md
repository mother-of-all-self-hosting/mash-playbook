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
SPDX-FileCopyrightText: 2023 Gergely Horváth
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2023, 2024 MASH project contributors
SPDX-FileCopyrightText: 2024 Philipp Homann
SPDX-FileCopyrightText: 2024 Thomas Miceli
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# LLDAP

The playbook can install and configure [LLDAP](https://github.com/lldap/lldap/) for you.

LLDAP is a lightweight authentication server that provides an opinionated, simplified LDAP interface for authentication.

See the project's [documentation](https://github.com/lldap/lldap/blob/main/README.md) to learn what LLDAP does and why it might be useful to you.

For details about configuring the [Ansible role for LLDAP](https://github.com/mother-of-all-self-hosting/ansible-role-lldap), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-lldap/blob/main/docs/configuring-lldap.md) online
- 📁 `roles/galaxy/lldap/docs/configuring-lldap.md` locally, if you have [fetched the Ansible roles](../../docs/installing.md)

## Dependencies

This service requires the following other services:

- [Postgres](../postgres/README.md) / MySQL / [MariaDB](../mariadb/README.md) / [SQLite](https://www.sqlite.org/) database
- [Traefik](../traefik/README.md) reverse-proxy server
- (optional) [exim-relay](../exim_relay/README.md) mailer

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../../docs/installing.md) process:

```yaml
########################################################################
#                                                                      #
# lldap                                                                #
#                                                                      #
########################################################################

lldap_enabled: true

lldap_hostname: lldap.example.com

########################################################################
#                                                                      #
# /lldap                                                               #
#                                                                      #
########################################################################
```

**Note**: hosting LLDAP under a subpath (by configuring the `lldap_path_prefix` variable) does not seem to be possible due to LLDAP's technical limitations.

### Set administrator's account details

It is necessary to create an initial user with admin privileges. Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-lldap/blob/main/docs/configuring-lldap.md#set-administrators-account-details) on the role's documentation for details.

### Select database to use

LLDAP can use a MySQL compatible database, Postgres, or SQLite, and you need to choose one. Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-lldap/blob/main/docs/configuring-lldap.md#specify-database) on the role's documentation for details.

>[!NOTE]
> If you have not disabled Postgres explicitly with this playbook, the database for your existing installation is most likely to be `postgres`.

### Configuring the mailer (optional)

On LLDAP you can set up a mailer for functions such as password recovery. If you enable the [exim-relay](../exim_relay/README.md) service in your inventory configuration, the playbook will automatically configure it as a mailer for the service.

To actually have the service use (and get messages sent through the exim-relay service), you will need to adjust settings on the service's UI after the service is installed.

>[!WARNING]
> Without setting an authentication method such as DKIM, SPF, and DMARC for your hostname, emails are most likely to be quarantined as spam at recipient's mail servers. The worst scenario is that your server's IP address or hostname will be included in the spam list such as the one managed by [Spamhaus](https://www.spamhaus.org/), depending on the reputation. As the exim-relay service supports DKIM signing, refer to [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay/blob/main/docs/configuring-exim-relay.md#enable-dkim-support-optional) for details about how to set it up.

## Usage

After running the command for installation, the LLDAP instance becomes available at the URL specified with `lldap_hostname`. With the configuration above, the service is hosted at `https://lldap.example.com`.

To get started, open the URL with a web browser to log in to the instance with the administrator account. You can create additional users (admin-privileged or not) after that via the web frontend. Refer to [this section](https://github.com/lldap/lldap/blob/main/README.md#usage) on the documentation for details about the usage, including a recommended architecture.

## Troubleshooting

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-lldap/blob/main/docs/configuring-lldap.md#troubleshooting) on the role's documentation for details.

## Related services

- [Pocket ID](../pocket_id/README.md) — OIDC provider for passkey-only authentication
- [Tinyauth](../tinyauth/README.md) — Authentication middleware that adds a login screen or OAuth with providers to Docker services
