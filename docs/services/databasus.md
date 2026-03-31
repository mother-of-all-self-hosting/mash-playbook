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

# Databasus

>[!CAUTION]
> The original author [declared](https://github.com/databasus/databasus/issues/199) that Databasus did not support running the service as non-root user because it is allegedly "very rare case needed for less than 1%< of users."

The playbook can install and configure [Databasus](https://databasus.com/) for you.

Databasus is free software for backing up database of PostgreSQL, MySQL, MariaDB, and MongoDB.

See the project's [documentation](https://databasus.com/installation) to learn what Databasus does and why it might be useful to you.

For details about configuring the [Ansible role for Databasus](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3AzeQ4hXq2LkbADcndSsjesgq9kDPf), you can check them via:
- 🌐 [the role's documentation](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3AzeQ4hXq2LkbADcndSsjesgq9kDPf/tree/docs/configuring-databasus.md) online
- 📁 `roles/galaxy/databasus/docs/configuring-databasus.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server
- (optional) [exim-relay](exim-relay.md) mailer

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# databasus                                                            #
#                                                                      #
########################################################################

databasus_enabled: true

databasus_hostname: databasus.example.com

########################################################################
#                                                                      #
# /databasus                                                           #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the Databasus instance becomes available at the URL specified with `databasus_hostname`. With the configuration above, the service is hosted at `https://databasus.example.com`.

To get started, open the URL with a web browser to create an account. **Note that the first registered user becomes an administrator automatically.**

Since MariaDB, PostgreSQL, and MongoDB are wired to the service, it is possible to set `mash-mariadb`, `mash-postgres`, or `mash-mongodb` to the input area for the host when adding a database to back up.

### Configuring the mailer (optional)

On Databasus you can add configuration settings of a SMTP server for sending notifications. If you enable the [exim-relay](exim-relay.md) service in your inventory configuration, the playbook will automatically connect it to the Databasus service.

As the Databasus instance does not support configuring the mailer with environment variables, you can add default options for it on its UI. Refer to [this page](https://databasus.com/notifiers) on the official documentation as well.

To set up with the default exim-relay settings, open `databasus.example.com` and navigate to the notifier setting's UI to add the following configuration:

- **Target email**: (Input an email address to send notifications)
- **SMTP host**: `mash-exim-relay`
- **SMTP port**: 8025
- **SMTP user**: (Empty)
- **SMTP password**: (Empty)
- **From**: (Input the email address specified to `exim_relay_sender_address` on your `vars.yml`)

After setting the configuration, you can have the Databasus instance send a test mail.

>[!WARNING]
> Without setting an authentication method such as DKIM, SPF, and DMARC for your hostname, emails are most likely to be quarantined as spam at recipient's mail servers. The worst scenario is that your server's IP address or hostname will be included in the spam list such as the one managed by [Spamhaus](https://www.spamhaus.org/), depending on the reputation. As the exim-relay service supports DKIM signing, refer to [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay/blob/main/docs/configuring-exim-relay.md#enable-dkim-support-optional) for details about how to set it up.

## Troubleshooting

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3AzeQ4hXq2LkbADcndSsjesgq9kDPf/tree/docs/configuring-databasus.md#troubleshooting) on the role's documentation for details.

## Related services

- [Postgres Backup](postgres-backup.md) — A solution for backing up PostgreSQL to local filesystem with periodic backups
