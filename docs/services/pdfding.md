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
SPDX-FileCopyrightText: 2024 Thomas Miceli

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# PdfDing

The playbook can install and configure [PdfDing](https://pdfding.com/) for you.

PdfDing is a self-hosted PDF manager, viewer and editor, which offers a seamless user experience on multiple devices.

See the project's [documentation](https://docs.pdfding.com/) to learn what PdfDing does and why it might be useful to you.

For details about configuring the [Ansible role for PdfDing](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az2cZCZP8Mu4LYMbHKaTdnP1otc46L), you can check them via:
- 🌐 [the role's documentation](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az2cZCZP8Mu4LYMbHKaTdnP1otc46L/tree/docs/configuring-pdfding.md) online
- 📁 `roles/galaxy/pdfding/docs/configuring-pdfding.md` locally, if you have [fetched the Ansible roles](../installing.md)

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
# pdfding                                                              #
#                                                                      #
########################################################################

pdfding_enabled: true

pdfding_hostname: pdfding.example.com

########################################################################
#                                                                      #
# /pdfding                                                             #
#                                                                      #
########################################################################
```

**Note**: hosting PdfDing under a subpath (by configuring the `pdfding_path_prefix` variable) does not seem to be possible due to PdfDing's technical limitations.

### Select database to use

It is necessary to select a database used by the service from Postgres and SQLite. See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az2cZCZP8Mu4LYMbHKaTdnP1otc46L/tree/docs/configuring-pdfding.md#specify-database) on the role's documentation for details.

### Enabling signing up

By default account registration for the service is disabled. To enable it, add the following configuration to your `vars.yml` file:

```yaml
pdfding_environment_variables_disable_user_signup: false
```

### Configuring the mailer (optional)

On PdfDing you can set up a mailer for functions such as password recovery. If you enable the [exim-relay](exim-relay.md) service in your inventory configuration, the playbook will automatically configure it as a mailer for the service.

>[!NOTE]
> Without setting an authentication method such as DKIM, SPF, and DMARC for your hostname, emails are most likely to be quarantined as spam at recipient's mail servers. If you have set up a mail server with the [exim-relay Ansible role](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay), you can enable DKIM signing with it. Refer [its documentation](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay/blob/main/docs/configuring-exim-relay.md#enable-dkim-support-optional) for details.

## Usage

After installation, the PdfDing instance becomes available at the URL specified with `pdfding_hostname`. With the configuration above, the service is hosted at `https://pdfding.example.com`.

To get started, open the URL with a web browser, and register the account.

Since account registration is disabled by default, you need to enable it first by setting `pdfding_environment_variables_disable_user_signup` to `false` temporarily in order to create your own account.

## Troubleshooting

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az2cZCZP8Mu4LYMbHKaTdnP1otc46L/tree/docs/configuring-pdfding.md#troubleshooting) on the role's documentation for details.
