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
SPDX-FileCopyrightText: 2024 - 2025 MASH project contributors
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara
SPDX-FileCopyrightText: 2024 noah

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Readeck

The playbook can install and configure [Readeck](https://readeck.org) for you.

Readeck is a simple web application that lets you save the precious readable content of web pages you like and want to keep forever.

See the project's [documentation](https://readeck.org/en/docs/) to learn what Readeck does and why it might be useful to you.

For details about configuring the [Ansible role for Readeck](https://github.com/mother-of-all-self-hosting/ansible-role-readeck), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-readeck/blob/main/docs/configuring-readeck.md) online
- 📁 `roles/galaxy/readeck/docs/configuring-readeck.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Postgres](postgres.md) / [SQLite](https://www.sqlite.org/) database
- [Traefik](traefik.md) reverse-proxy server
- (optional) [exim-relay](exim-relay.md) mailer

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# readeck                                                              #
#                                                                      #
########################################################################

readeck_enabled: true

readeck_hostname: mash.example.com
readeck_path_prefix: /readeck

########################################################################
#                                                                      #
# /readeck                                                             #
#                                                                      #
########################################################################
```

### Select database to use

It is necessary to select a database used by Readeck from Postgres and SQLite. See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-readeck/blob/main/docs/configuring-readeck.md#specify-database) on the role's documentation for details.

### Configuring the mailer (optional)

On Readeck you can set up a mailer for functions such as bookmark sharing and password recovery. If you enable the [exim-relay](exim-relay.md) service in your inventory configuration, the playbook will automatically configure it as a mailer for the service.

>[!WARNING]
> Without setting an authentication method such as DKIM, SPF, and DMARC for your hostname, emails are most likely to be quarantined as spam at recipient's mail servers. The worst scenario is that your server's IP address or hostname will be included in the spam list such as the one managed by [Spamhaus](https://www.spamhaus.org/), depending on the reputation. As the exim-relay service supports DKIM signing, refer to [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay/blob/main/docs/configuring-exim-relay.md#enable-dkim-support-optional) for details about how to set it up.

## Usage

After running the command for installation, the Readeck instance becomes available at the URL specified with `readeck_hostname`. With the configuration above, the service is hosted at `https://readeck.example.com`.

To get started, open the URL with a web browser to create an account.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-readeck/blob/main/docs/configuring-readeck.md#troubleshooting) on the role's documentation for details.

## Related services

- [Karakeep](karakeep.md) — Self-hosted, open-source bookmark manager to collect, organize and archive webpages
- [linkding](linkding.md) — Bookmark manager designed to be minimal and fast
- [Linkwarden](linkwarden.md) — Self-hosted, open-source collaborative bookmark manager to collect, organize and archive webpages
