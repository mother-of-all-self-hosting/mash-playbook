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

- [Postgres](postgres.md) / MySQL / [MariaDB](mariadb.md) / [CockroachDB](https://www.cockroachlabs.com/) / [SQLite](https://www.sqlite.org/) database — SFTPGo will default to Postgres
- [Traefik](traefik.md) reverse-proxy server
- (optional) [exim-relay](exim-relay.md) mailer

## Configuration

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

Please note that it is necessary to add environment variables to `sftpgo_environment_variables_additional_variables` manually for database other than Postgres and MySQL (MariaDB). Refer to [this section](https://docs.sftpgo.com/latest/config-file/#data-provider) on the official documentation for options to be configured.

### Configuring the mailer (optional)

On SFTPGo you can set up a mailer for functions such as password recovery. If you enable the [exim-relay](exim-relay.md) service in your inventory configuration, the playbook will automatically configure it as a mailer for the service.

To actually have the service use (and get messages sent through the exim-relay service), you will need to adjust settings on the service's UI after the service is installed.

>[!WARNING]
> Without setting an authentication method such as DKIM, SPF, and DMARC for your hostname, emails are most likely to be quarantined as spam at recipient's mail servers. The worst scenario is that your server's IP address or hostname will be included in the spam list such as the one managed by [Spamhaus](https://www.spamhaus.org/), depending on the reputation. As the exim-relay service supports DKIM signing, refer to [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay/blob/main/docs/configuring-exim-relay.md#enable-dkim-support-optional) for details about how to set it up.

### Integrating with Prometheus (optional)

SFTPGo can natively expose metrics to [Prometheus](prometheus.md).

#### Expose metrics internally

If SFTPGo and Prometheus do not share a network (like Traefik), you can connect the SFTPGo container network to Prometheus by adding the following configuration to your `vars.yml` file:

```yaml
prometheus_container_additional_networks_custom:
  - "{{ sftpgo_container_network }}"
```

#### Expose metrics publicly

If SFTPGo metrics are not scraped from a local Prometheus instance, you can expose the metrics publicly so that a remote instance can fetch them.

When exposing metrics publicly, you should consider to set up [HTTP Basic Authentication](https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication) **or anyone would be able to read your metrics**.

To expose the metrics publicly, add the following configuration to your `vars.yml` file (adapt to your needs):

```yaml
mash_playbook_metrics_exposure_enabled: true
mash_playbook_metrics_exposure_hostname: mash.example.com
```

It will expose the metrics at `https://mash.example.com/metrics/mash-sftpgo`.

To enable the HTTP Basic authentication, add the following configuration to your `vars.yml` file (adapt to your needs):

```yaml
sftpgo_container_labels_traefik_metrics_middleware_basic_auth_enabled: true

# See https://doc.traefik.io/traefik/middlewares/http/basicauth/#users for details.
sftpgo_container_labels_traefik_metrics_middleware_basic_auth_users: ""
```

## Usage

After running the command for installation, the SFTPGo instance becomes available at the URL specified with `sftpgo_hostname`. With the configuration above, the service is hosted at `https://sftpgo.example.com`. By default you can connect to the SFTP server on the port `2022`.

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-sftpgo/blob/main/docs/configuring-sftpgo.md#adjusting-the-playbook-configuration) on the role's documentation for details about how to enable web interfaces and create the first admin account, including the configuration to enable WebDAV server.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-sftpgo/blob/main/docs/configuring-sftpgo.md#troubleshooting) on the role's documentation for details.
