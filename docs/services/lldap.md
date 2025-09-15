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
SPDX-FileCopyrightText: 2023 - 2024 MASH project contributors
SPDX-FileCopyrightText: 2023 Antonis Christofides
SPDX-FileCopyrightText: 2023 Felix Stupp
SPDX-FileCopyrightText: 2023 Gergely Horváth
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara
SPDX-FileCopyrightText: 2024 Philipp Homann

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# LLDAP

The playbook can install and configure [LLDAP](https://github.com/lldap/lldap/) for you.

LLDAP is a lightweight authentication server that provides an opinionated, simplified LDAP interface for authentication.

See the project's [documentation](https://github.com/lldap/lldap/blob/main/README.md) to learn what LLDAP does and why it might be useful to you.

For details about configuring the [Ansible role for LLDAP](https://github.com/mother-of-all-self-hosting/ansible-role-lldap), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-lldap/blob/main/docs/configuring-lldap.md) online
- 📁 `roles/galaxy/lldap/docs/configuring-lldap.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server
- (optional) [Postgres](postgres.md) / MySQL / [MariaDB](mariadb.md) database — LLDAP will default to [SQLite](https://www.sqlite.org/) if Postgres is not enabled

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

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

### Specify the username and password for the initial admin user

It is necessary to create an initial user with admin privileges by adding the following configuration to your `vars.yml` file:

```yaml
lldap_environment_variables_lldap_ldap_user_dn: ADMIN_USER_USERNAME_HERE

lldap_environment_variables_lldap_ldap_user_pass: ADMIN_USER_PASSWORD_HERE
```

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-lldap/blob/main/docs/configuring-lldap.md#specify-the-username-and-password-for-the-initial-admin-user) on the role's documentation for details.

### Select database to use (optional)

By default LLDAP is configured to use Postgres, but you can choose other databases such as MySQL (MariaDB) and SQLite. See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-lldap/blob/main/docs/configuring-lldap.md#specify-database-optional) on the role's documentation for details.

### Configure the mailer (optional)

On LLDAP you can set up a mailer for functions such as sending a password reset mail. **You can use Exim-relay as the mailer, which is enabled on this playbook by default.** See [this page about Exim-relay configuration](exim-relay.md) for details about how to set it up.

>[!NOTE]
> Without setting an authentication method such as DKIM, SPF, and DMARC for your hostname, emails are most likely to be quarantined as spam at recipient's mail servers. If you have set up a mail server with the [exim-relay Ansible role](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay), you can enable DKIM signing with it. Refer [its documentation](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay/blob/main/docs/configuring-exim-relay.md#enable-dkim-support-optional) for details.

## Usage

After running the command for installation, the LLDAP instance becomes available at the URL specified with `lldap_hostname`. With the configuration above, the service is hosted at `https://lldap.example.com`.

To get started, open the URL with a web browser, and log in to the instance with the administrator account. You can create additional users (admin-privileged or not) after that via the web frontend. See [this section](https://github.com/lldap/lldap/blob/main/README.md#usage) on the documentation for details about usage, including a recommended architecture.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-lldap/blob/main/docs/configuring-lldap.md#troubleshooting) on the role's documentation for details.

## Related services

- [YOURLS](yourls.md) — Your Own URL Shortener, on your server
