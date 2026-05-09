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
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Semaphore UI

The playbook can install and configure [Semaphore UI](https://semaphoreui.com) for you.

Semaphore UI is a modern UI for Ansible, Terraform/OpenTofu/Terragrunt, PowerShell and other DevOps tools.

See the project's [documentation](https://docs.semaphoreui.com/) to learn what Semaphore UI does and why it might be useful to you.

For details about configuring the [Ansible role for Semaphore UI](https://github.com/mother-of-all-self-hosting/ansible-role-semaphore), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-semaphore/blob/main/docs/configuring-semaphore.md) online
- 📁 `roles/galaxy/semaphore/docs/configuring-semaphore.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server
- (optional) [exim-relay](exim-relay.md) mailer
- (optional) [Postgres](postgres.md) / MySQL / [MariaDB](mariadb.md) database — Semaphore UI will default to [SQLite](https://www.sqlite.org/) if Postgres is not enabled

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# semaphore                                                            #
#                                                                      #
########################################################################

semaphore_enabled: true

semaphore_hostname: semaphore.example.com

########################################################################
#                                                                      #
# /semaphore                                                           #
#                                                                      #
########################################################################
```

### Set details for the admin user

You need to create an instance's admin user by setting values to the `semaphore_admin_*` variables. See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-semaphore/blob/main/docs/configuring-semaphore.md#set-details-for-the-admin-user) on the role's documentation for details.

### Set a string for encrypting access keys

You also have to set a string used for encrypting access keys in database to `semaphore_access_key_encryption`. Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-semaphore/blob/main/docs/configuring-semaphore.md#set-a-string-for-encrypting-access-keys) on the role's documentation for details.

### Select database to use (optional)

By default Semaphore UI is configured to use [Postgres](postgres.md) (if enabled), but you can choose other databases such as MySQL (MariaDB) and SQLite. If Postgres is not enabled, SQLite will be used. See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-semaphore/blob/main/docs/configuring-semaphore.md#configure-database) on the role's documentation for details.

### Configuring the mailer (optional)

On Semaphore UI you can set up a mailer for functions such as password recovery. If you enable the [exim-relay](exim-relay.md) service in your inventory configuration, the playbook will automatically configure it as a mailer for the service.

To actually have the service use (and get messages sent through the exim-relay service), you will need to adjust settings on the service's UI after the service is installed.

>[!WARNING]
> Without setting an authentication method such as DKIM, SPF, and DMARC for your hostname, emails are most likely to be quarantined as spam at recipient's mail servers. The worst scenario is that your server's IP address or hostname will be included in the spam list such as the one managed by [Spamhaus](https://www.spamhaus.org/), depending on the reputation. As the exim-relay service supports DKIM signing, refer to [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay/blob/main/docs/configuring-exim-relay.md#enable-dkim-support-optional) for details about how to set it up.

### Extending the configuration

There are some additional things you may wish to configure about the component.

Take a look at:

- [Semaphore UI](https://github.com/mother-of-all-self-hosting/ansible-role-semaphore)'s [`defaults/main.yml`](https://github.com/mother-of-all-self-hosting/ansible-role-semaphore/blob/main/defaults/main.yml) for some variables that you can customize via your `vars.yml` file.

See the [documentation](https://docs.semaphoreui.com/administration-guide/configuration/) for a complete list of Semaphore UI's config options such as [two-factor authentication with TOTP](https://github.com/mother-of-all-self-hosting/ansible-role-semaphore/blob/main/docs/configuring-semaphore.md#enable-2fa-authentication-with-totp-optional).

## Usage

After running the command for installation, the Semaphore UI instance becomes available at the URL specified with `semaphore_hostname`. With the configuration above, the service is hosted at `https://semaphore.example.com`.

To get started, open the URL with a web browser to log in to the instance. See [this official guide](https://docs.semaphoreui.com/user-guide/projects/) for details about how to use it.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-semaphore/blob/main/docs/configuring-semaphore.md#troubleshooting) on the role's documentation for details.
