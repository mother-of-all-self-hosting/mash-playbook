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

# DocuSeal

The playbook can install and configure [DocuSeal](https://github.com/docusealco/docuseal) for you.

DocuSeal is a web application for digital document signing and processing.

See the project's [documentation](https://www.docuseal.com/docs/) to learn what DocuSeal does and why it might be useful to you.

For details about configuring the [Ansible role for DocuSeal](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az2HG5jWufCQfA8cYAFkJ9GmZyRcCs), you can check them via:
- 🌐 [the role's documentation](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az2HG5jWufCQfA8cYAFkJ9GmZyRcCs/tree/docs/configuring-docuseal.md) online
- 📁 `roles/galaxy/docuseal/docs/configuring-docuseal.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Postgres](postgres.md) / MySQL / [MariaDB](mariadb.md) / [SQLite](https://www.sqlite.org/) database
- [Traefik](traefik.md) reverse-proxy server
- (optional) [exim-relay](exim-relay.md) mailer — DocuSeal is compatible with other email delivery services

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# docuseal                                                             #
#                                                                      #
########################################################################

docuseal_enabled: true

docuseal_hostname: docuseal.example.com

########################################################################
#                                                                      #
# /docuseal                                                            #
#                                                                      #
########################################################################
```

**Note**: hosting DocuSeal under a subpath (by configuring the `docuseal_path_prefix` variable) does not seem to be possible due to DocuSeal's technical limitations.

### Select database to use

It is necessary to select a database used by DocuSeal from a MySQL compatible database, Postgres, and SQLite. See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az2HG5jWufCQfA8cYAFkJ9GmZyRcCs/tree/docs/configuring-docuseal.md#specify-database) on the role's documentation for details.

### Configuring the mailer (optional)

On Docuseal you can set up a mailer for functions such as password recovery. If you enable the [exim-relay](exim-relay.md) service in your inventory configuration, the playbook will automatically configure it as a mailer for the service.

To actually have the service use (and get messages sent through the exim-relay service), you will need to adjust settings on the service's UI after the service is installed.

>[!WARNING]
> Without setting an authentication method such as DKIM, SPF, and DMARC for your hostname, emails are most likely to be quarantined as spam at recipient's mail servers. The worst scenario is that your server's IP address or hostname will be included in the spam list such as the one managed by [Spamhaus](https://www.spamhaus.org/), depending on the reputation. As the exim-relay service supports DKIM signing, refer to [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay/blob/main/docs/configuring-exim-relay.md#enable-dkim-support-optional) for details about how to set it up.

## Usage

After running the command for installation, the DocuSeal instance becomes available at the URL specified with `docuseal_hostname`. With the configuration above, the service is hosted at `https://docuseal.example.com`.

To get started, open the URL with a web browser, and follow the set up wizard.

## Troubleshooting

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3AzeEwXM9Fp4C8NU4oQfNg474Vivwu/tree/docs/configuring-docuseal.md#troubleshooting) on the role's documentation for details.
