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
SPDX-FileCopyrightText: 2024 shukon
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# DokuWiki

The playbook can install and configure [DokuWiki](https://www.dokuwiki.org/dokuwiki) for you.

DokuWiki is a lightweight, file-based wiki engine with intuitive syntax and no database requirements.

See the project's [documentation](https://www.dokuwiki.org/manual) to learn what DokuWiki does and why it might be useful to you.

For details about configuring the [Ansible role for DokuWiki](https://github.com/mother-of-all-self-hosting/ansible-role-dokuwiki), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-dokuwiki/blob/main/docs/configuring-dokuwiki.md) online
- 📁 `roles/galaxy/dokuwiki/docs/configuring-dokuwiki.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server
- (optional) [exim-relay](exim-relay.md) mailer — DokuWiki is compatible with other email delivery services

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# dokuwiki                                                             #
#                                                                      #
########################################################################

dokuwiki_enabled: true

dokuwiki_hostname: dokuwiki.example.com

########################################################################
#                                                                      #
# /dokuwiki                                                            #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the DokuWiki instance becomes available at the URL specified with `dokuwiki_hostname`. With the configuration above, the service is hosted at `https://dokuwiki.example.com`.

To get started, open the URL `https://dokuwiki.example.com/install.php` with a web browser to complete installation on the server. The instruction is available at <https://www.dokuwiki.org/installer>.

### Configuring the SMTP server (optional)

On DokuWiki you can add a plugin to have the service connect to a SMTP server for password recovery function. If you enable the [exim-relay](exim-relay.md) service in your inventory configuration, the playbook will automatically configure it as a mailer for the service.

As the DokuWiki instance does not support configuring the mailer with environment variables, you can add default options for it on its UI. Refer to [this page](https://www.dokuwiki.org/plugin:smtp) on the official documentation as well about how to configure it.

To set up with the default exim-relay settings, install the plugin, navigate to "Configuration Manager", and add the following configuration:

- **SMTP Server**: `mash-exim-relay`
- **Port**: 8025
- **SSL setting**: none

After setting the configuration, you can have the DokuWiki instance send a test mail on the administration page.

>[!WARNING]
> Without setting an authentication method such as DKIM, SPF, and DMARC for your hostname, emails are most likely to be quarantined as spam at recipient's mail servers. The worst scenario is that your server's IP address or hostname will be included in the spam list such as the one managed by [Spamhaus](https://www.spamhaus.org/), depending on the reputation. As the exim-relay service supports DKIM signing, refer to [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay/blob/main/docs/configuring-exim-relay.md#enable-dkim-support-optional) for details about how to set it up.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-dokuwiki/blob/main/docs/configuring-dokuwiki.md#troubleshooting) on the role's documentation for details.

## Related services

- [An Otter Wiki](otterwiki.md) — Minimalistic wiki powered by Python, Markdown and Git
- [MediaWiki](mediawiki.md) — Popular free and open-source wiki software
