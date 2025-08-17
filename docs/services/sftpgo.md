<!--
SPDX-FileCopyrightText: 2020 - 2024 MDAD project contributors
SPDX-FileCopyrightText: 2020 - 2024 Slavi Pantaleev
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
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# SFTPGo

The playbook can install and configure [SFTPGo](https://github.com/drakkan/sftpgo/) for you.

SFTPGo is a full-featured and highly configurable event-driven file transfer solution. It supports SFTP, HTTP/S, FTP/S and WebDAV, and can connect to storage backends including local filesystem, S3 (compatible) Object Storage, Google Cloud Storage, Azure Blob Storage, and other SFTP servers.

See the project's [documentation](https://docs.sftpgo.com/latest/) to learn what SFTPGo does and why it might be useful to you.

For details about configuring the [Ansible role for SFTPGo](https://github.com/mother-of-all-self-hosting/ansible-role-sftpgo), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-sftpgo/blob/main/docs/configuring-sftpgo.md) online
- 📁 `roles/galaxy/sftpgo/docs/configuring-sftpgo.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Prerequisites

You may need to open some ports to your server, if you use another firewall in front of the server. Refer to [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-sftpgo/blob/main/docs/configuring-sftpgo.md#prerequisites) to check which ones to be configured.

## Dependencies

This service requires the following other services:

- [Postgres](postgres.md) / MySQL / [MariaDB](mariadb.md) / [CockroachDB](https://www.cockroachlabs.com/) database — SFTPGo will default to [SQLite](https://www.sqlite.org/) if none of them is enabled
- [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# sftpgo                                                               #
#                                                                      #
########################################################################

sftpgo_enabled: true

sftpgo_hostname: sftpgo.example.com

########################################################################
#                                                                      #
# /sftpgo                                                              #
#                                                                      #
########################################################################
```

**Note**: hosting SFTPGo under a subpath (by configuring the `sftpgo_path_prefix` variable) does not seem to be possible due to SFTPGo's technical limitations.

### Select database to use (optional)

By default SFTPGo is configured to use Postgres, but you can choose other database such as SQLite, MySQL (MariaDB), and CockroachDB.

To use MariaDB, add the following configuration to your `vars.yml` file:

```yaml
sftpgo_environment_variables_data_provider_driver: mysql
```

Please note that it is necessary to add environment variables manually for database other than Postgres and MySQL (MariaDB).

Refer to [this section](https://docs.sftpgo.com/latest/config-file/#data-provider) on the official documentation for options to be configured.

## Usage

After running the command for installation, the SFTPGo instance becomes available at the URL specified with `sftpgo_hostname`. With the configuration above, the service is hosted at `https://sftpgo.example.com`. By default you can connect to the SFTP server on the port `2022`.

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-sftpgo/blob/main/docs/configuring-sftpgo.md#adjusting-the-playbook-configuration) on the role's documentation for details about how to enable web interfaces and create the first admin account, including the configuration to enable WebDAV server.

### Configure the mailer (optional)

On SFTPGo you can set up a mailer for functions such as sending a password reset mail. **You can use Exim-relay as the mailer, which is enabled on this playbook by default.** See [this page about Exim-relay configuration](exim-relay.md) for details about how to set it up.

>[!NOTE]
> Without setting an authentication method such as DKIM, SPF, and DMARC for your hostname, emails are most likely to be quarantined as spam at recipient's mail servers. If you have set up a mail server with the [exim-relay Ansible role](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay), you can enable DKIM signing with it. Refer [its documentation](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay/blob/main/docs/configuring-exim-relay.md#enable-dkim-support-optional) for details.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-sftpgo/blob/main/docs/configuring-sftpgo.md#troubleshooting) on the role's documentation for details.
