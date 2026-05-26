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

# BookStack

The playbook can install and configure [BookStack](https://www.bookstackapp.com) for you.

BookStack is a platform for organising and storing information.

See the project's [documentation](https://www.bookstackapp.com/docs/) to learn what BookStack does and why it might be useful to you.

For details about configuring the [Ansible role for BookStack](https://radicle.network/nodes/seed.radicle.garden/rad%3AzQdRwQ2s3FG5BZUjvSn1GYXbzVmw), you can check them via:

- 🌐 [the role's documentation](https://radicle.network/nodes/seed.radicle.garden/rad%3AzQdRwQ2s3FG5BZUjvSn1GYXbzVmw/tree/docs/configuring-bookstack.md) online
- 📁 `roles/galaxy/bookstack/docs/configuring-bookstack.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- MySQL / [MariaDB](mariadb.md) database
- [Traefik](traefik.md) reverse-proxy server
- (optional) [exim-relay](exim-relay.md) mailer

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# bookstack                                                            #
#                                                                      #
########################################################################

bookstack_enabled: true

bookstack_hostname: bookstack.example.com

########################################################################
#                                                                      #
# /bookstack                                                           #
#                                                                      #
########################################################################
```

### Enable MariaDB

BookStack requires a MySQL-compatible database to work. This playbook supports MariaDB, and you can set up a MariaDB instance by enabling it on `vars.yml`.

Refer to [this page](mariadb.md) for the instruction to enable it.

### Set a random string

You also need to set a random **32 character** string. To do so, add the following configuration to your `vars.yml` file. The value can be generated with `openssl rand -hex 16` or in another way.

```yaml
bookstack_environment_variables_app_key: YOUR_SECRET_KEY_HERE
```

### Configuring the mailer (optional)

On BookStack you can set up a mailer for functions such as password recovery. If you enable the [exim-relay](exim-relay.md) service in your inventory configuration, the playbook will automatically configure it as a mailer for the service.

>[!WARNING]
> Without setting an authentication method such as DKIM, SPF, and DMARC for your hostname, emails are most likely to be quarantined as spam at recipient's mail servers. The worst scenario is that your server's IP address or hostname will be included in the spam list such as the one managed by [Spamhaus](https://www.spamhaus.org/), depending on the reputation. As the exim-relay service supports DKIM signing, refer to [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay/blob/main/docs/configuring-exim-relay.md#enable-dkim-support-optional) for details about how to set it up.

## Usage

After running the command for installation, the BookStack instance becomes available at the URL specified with `bookstack_hostname`. With the configuration above, the service is hosted at `https://bookstack.example.com`.

To get started, open the URL `https://example.com` with a web browser, and log in to the instance with the administrator account credentials. The default login credentials can be checked at <https://github.com/solidnerd/docker-bookstack/blob/master/README.md>.

## Troubleshooting

See [this section](https://radicle.network/nodes/seed.radicle.garden/rad%3AzQdRwQ2s3FG5BZUjvSn1GYXbzVmw/tree/docs/configuring-bookstack.md#troubleshooting) on the role's documentation for details.

## Related services

- [Docmost](docmost.md) — Collaborative wiki and documentation software
- [Outline](outline.md) — Knowledge base for growing teams
