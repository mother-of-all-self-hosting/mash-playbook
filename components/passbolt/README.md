<!--
SPDX-FileCopyrightText: 2026 spatterlight

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Passbolt

The playbook can install and configure [Passbolt](https://www.passbolt.com/) for you.

Passbolt is an open source password manager for teams, built around OpenPGP.

See the project's [documentation](https://www.passbolt.com/docs/) to learn what Passbolt does and why it might be useful to you.

For details about configuring the [Ansible role for Passbolt](https://github.com/mother-of-all-self-hosting/ansible-role-passbolt), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-passbolt/blob/main/docs/configuring-passbolt.md) online
- 📁 `roles/galaxy/passbolt/docs/configuring-passbolt.md` locally, if you have [fetched the Ansible roles](../../docs/installing.md)

## Dependencies

This service requires the following other services:

- [Postgres](../postgres/README.md) / MySQL / [MariaDB](../mariadb/README.md) database
- [Traefik](../traefik/README.md) reverse-proxy server
- (optional) [exim-relay](../exim_relay/README.md) mailer

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../../docs/installing.md) process:

```yaml
########################################################################
#                                                                      #
# passbolt                                                             #
#                                                                      #
########################################################################

passbolt_enabled: true

passbolt_hostname: passbolt.example.com

########################################################################
#                                                                      #
# /passbolt                                                            #
#                                                                      #
########################################################################
```

**Note**: hosting Passbolt under a subpath (by configuring the `passbolt_path_prefix` variable) does not seem to be possible due to Passbolt's technical limitations.

### Select database to use

Passbolt can use either a MySQL compatible database or Postgres, and you need to choose one. Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-passbolt/blob/main/docs/configuring-passbolt.md#specify-database) on the role's documentation for details.

### Configuring the mailer (optional)

On Passbolt you can set up a mailer for sending links to set up accounts and notifications. If you enable the [exim-relay](../exim_relay/README.md) service in your inventory configuration, the playbook will automatically configure it as a mailer for the service.

>[!WARNING]
> Without setting an authentication method such as DKIM, SPF, and DMARC for your hostname, emails are most likely to be quarantined as spam at recipient's mail servers. The worst scenario is that your server's IP address or hostname will be included in the spam list such as the one managed by [Spamhaus](https://www.spamhaus.org/), depending on the reputation. As the exim-relay service supports DKIM signing, refer to [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay/blob/main/docs/configuring-exim-relay.md#enable-dkim-support-optional) for details about how to set it up.

## Usage

After running the command for installation, the Passbolt instance becomes available at the URL specified with `passbolt_hostname`. With the configuration above, the service is hosted at `https://passbolt.example.com`.

To get started, create the first administrator by running the command below on the server (replace the values with your own):

```sh
docker exec mash-passbolt bin/cake passbolt register_user -u EMAIL_ADDRESS_HERE -f FIRST_NAME_HERE -l LAST_NAME_HERE -r admin
```

The command prints a link to finish setting up the account, which needs the [Passbolt browser extension](https://www.passbolt.com/download). The same link is sent by email if the mailer is configured.

## Troubleshooting

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-passbolt/blob/main/docs/configuring-passbolt.md#troubleshooting) on the role's documentation for details.

## Related services

- [Vaultwarden](../vaultwarden/README.md) — A lightweight unofficial and compatible implementation of the Bitwarden password manager
