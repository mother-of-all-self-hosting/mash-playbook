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
- 📁 `roles/galaxy/semaphore/docs/configuring-semaphore.md` locally, if you have [fetched the Ansible roles](../../docs/installing.md)

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

### Set administrator's account details

You also need to specify administrator's account details. Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-semaphore/blob/main/docs/configuring-semaphore.md#set-administrators-account-details) on the role's documentation for details.

### Set a random string

You also have to set a random string used for encrypting access keys. Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-semaphore/blob/main/docs/configuring-semaphore.md#set-a-string-for-encrypting-access-keys) on the role's documentation for details.

### Select database to use

Semaphore UI can use a MySQL compatible database, Postgres, or SQLite, and you need to choose one. Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-semaphore/blob/main/docs/configuring-semaphore.md#specify-database) on the role's documentation for details.

>[!NOTE]
> If you have not disabled Postgres explicitly with this playbook, the database for your existing installation is most likely to be `postgres`.

### Configuring the mailer (optional)

On Semaphore UI you can set up a mailer for functions such as password recovery. If you enable the [exim-relay](../exim_relay/README.md) service in your inventory configuration, the playbook will automatically configure it as a mailer for the service.

To actually have the service use (and get messages sent through the exim-relay service), you will need to adjust settings on the service's UI after the service is installed.

>[!WARNING]
> Without setting an authentication method such as DKIM, SPF, and DMARC for your hostname, emails are most likely to be quarantined as spam at recipient's mail servers. The worst scenario is that your server's IP address or hostname will be included in the spam list such as the one managed by [Spamhaus](https://www.spamhaus.org/), depending on the reputation. As the exim-relay service supports DKIM signing, refer to [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay/blob/main/docs/configuring-exim-relay.md#enable-dkim-support-optional) for details about how to set it up.

## Usage

After running the command for installation, the Semaphore UI instance becomes available at the URL specified with `semaphore_hostname`. With the configuration above, the service is hosted at `https://semaphore.example.com`.

To get started, open the URL with a web browser to log in to the instance. Refer to [this official guide](https://docs.semaphoreui.com/user-guide/projects/) for details about how to use it.

## Troubleshooting

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-semaphore/blob/main/docs/configuring-semaphore.md#troubleshooting) on the role's documentation for details.
