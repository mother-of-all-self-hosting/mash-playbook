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
SPDX-FileCopyrightText: 2024 Thomas Miceli
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Kanboard

The playbook can install and configure [Kanboard](https://kanboard.org/) for you.

Kanboard is a free and open source Kanban project management software.

See the project's [documentation](https://docs.kanboard.org/) to learn what Kanboard does and why it might be useful to you.

For details about configuring the [Ansible role for Kanboard](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az2LZH9TGMxYbGBaGoMHNFX5HymEL3), you can check them via:
- 🌐 [the role's documentation](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az2LZH9TGMxYbGBaGoMHNFX5HymEL3/tree/docs/configuring-kanboard.md) online
- 📁 `roles/galaxy/kanboard/docs/configuring-kanboard.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Postgres](postgres.md) / MySQL / [MariaDB](mariadb.md) / [SQLite](https://www.sqlite.org/) database
- [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# kanboard                                                             #
#                                                                      #
########################################################################

kanboard_enabled: true

kanboard_hostname: kanboard.example.com

########################################################################
#                                                                      #
# /kanboard                                                            #
#                                                                      #
########################################################################
```

**Note**: hosting Kanboard under a subpath (by configuring the `kanboard_path_prefix` variable) does not seem to be possible due to Kanboard's technical limitations.

### Select database to use

It is necessary to select a database used by Kanboard from a MySQL compatible database, Postgres, and SQLite. See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az2LZH9TGMxYbGBaGoMHNFX5HymEL3/tree/docs/configuring-kanboard.md#specify-database) on the role's documentation for details.

### Configuring the mailer (optional)

On Kanboard you can set up a mailer for functions such as password recovery. If you enable the [exim-relay](exim-relay.md) service in your inventory configuration, the playbook will automatically configure it as a mailer for the service.

>[!NOTE]
> Without setting an authentication method such as DKIM, SPF, and DMARC for your hostname, emails are most likely to be quarantined as spam at recipient's mail servers. If you have set up a mail server with the [exim-relay Ansible role](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay), you can enable DKIM signing with it. Refer [its documentation](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay/blob/main/docs/configuring-exim-relay.md#enable-dkim-support-optional) for details.

## Usage

After running the command for installation, the Kanboard instance becomes available at the URL specified with `kanboard_hostname`. With the configuration above, the service is hosted at `https://kanboard.example.com`.

To get started, open the URL with a web browser to log in to the instance.

The initial username and password of the administrator is both `admin` (refer to [this page](https://docs.kanboard.org/v1/admin/installation/) on the documentation). Make sure to change them at `https://kanboard.example.com/user/show/1`.

## Troubleshooting

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az2LZH9TGMxYbGBaGoMHNFX5HymEL3/tree/docs/configuring-kanboard.md#troubleshooting) on the role's documentation for details.
