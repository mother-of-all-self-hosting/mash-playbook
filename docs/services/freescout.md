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
SPDX-FileCopyrightText: 2024 Nikita Chernyi
SPDX-FileCopyrightText: 2024 Thomas Miceli
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# FreeScout

The playbook can install and configure [FreeScout](https://freescout.net/) for you.

FreeScout is a free open-source helpdesk and shared inbox solution.

See the project's [documentation](https://github.com/freescout-help-desk/freescout/wiki) to learn what FreeScout does and why it might be useful to you.

For details about configuring the [Ansible role for FreeScout](https://github.com/mother-of-all-self-hosting/ansible-role-freescout), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-freescout/blob/main/docs/configuring-freescout.md) online
- 📁 `roles/galaxy/freescout/docs/configuring-freescout.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Postgres](postgres.md) / MySQL / [MariaDB](mariadb.md) database
- [Traefik](traefik.md) reverse-proxy server
- (optional) [exim-relay](exim-relay.md) mailer — FreeScout is compatible with other email delivery services

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# freescout                                                            #
#                                                                      #
########################################################################

freescout_enabled: true

freescout_hostname: freescout.example.com

freescout_environment_variables_admin_email: your-email-here
freescout_environment_variables_admin_password: a-strong-password-here

########################################################################
#                                                                      #
# /freescout                                                           #
#                                                                      #
########################################################################
```

### Select database to use

It is necessary to select a database used by FreeScout from a MySQL compatible database and Postgres. See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-freescout/blob/main/docs/configuring-freescout.md#specify-database) on the role's documentation for details.

### Configuring the mailer

On FreeScout it is necessary to add configuration settings for sending and fetching emails.

There are three methods available for sending emails: PHP's mail() function, Sendmail, and SMTP. If you enable the [exim-relay](exim-relay.md) service in your inventory configuration, the playbook will automatically connect it to the FreeScout service.

As the FreeScout instance does not support configuring the mailer with environment variables, you can add default options for it on its UI. Refer to [this page](https://github.com/freescout-help-desk/freescout/wiki/Sending-emails) on the official documentation as well about how to configure it.

To set up with the default exim-relay settings, navigate to "Connection Settings" to add the following configuration:

- **Method**: SMTP
- **SMTP Server**: `mash-exim-relay`
- **Port**: 8025
- **Username**: (Empty)
- **Password**: (Empty)

After setting the configuration, you can have the FreeScout instance send a test mail.

>[!WARNING]
> Without setting an authentication method such as DKIM, SPF, and DMARC for your hostname, emails are most likely to be quarantined as spam at recipient's mail servers. The worst scenario is that your server's IP address or hostname will be included in the spam list such as the one managed by [Spamhaus](https://www.spamhaus.org/), depending on the reputation. As the exim-relay service supports DKIM signing, refer to [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay/blob/main/docs/configuring-exim-relay.md#enable-dkim-support-optional) for details about how to set it up.

## Usage

After running the command for installation, the FreeScout instance becomes available at the URL specified with `freescout_hostname`. With the configuration above, the service is hosted at `https://freescout.example.com`.

To get started, open the URL with a web browser to log in to the instance. You can log in to the instance with the administrator email address (`freescout_admin_email`) and password (`freescout_admin_password`).

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-freescout/blob/main/docs/configuring-freescout.md#troubleshooting) on the role's documentation for details.
