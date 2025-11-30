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

# An Otter Wiki

The playbook can install and configure [An Otter Wiki](https://otterwiki.com/) for you.

An Otter Wiki is a minimalistic wiki powered by Python, Markdown and Git.

See the project's [documentation](https://otterwiki.com/-/help) to learn what An Otter Wiki does and why it might be useful to you.

For details about configuring the [Ansible role for An Otter Wiki](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3AzvzJe15VMBkGd2CMBctvpVZgmQG5), you can check them via:
- 🌐 [the role's documentation](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3AzvzJe15VMBkGd2CMBctvpVZgmQG5/tree/docs/configuring-otterwiki.md) online
- 📁 `roles/galaxy/otterwiki/docs/configuring-otterwiki.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server
- (optional) [exim-relay](exim-relay.md) mailer

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# otterwiki                                                            #
#                                                                      #
########################################################################

otterwiki_enabled: true

otterwiki_hostname: otterwiki.example.com

########################################################################
#                                                                      #
# /otterwiki                                                           #
#                                                                      #
########################################################################
```

**Note**: hosting An Otter Wiki under a subpath (by configuring the `otterwiki_path_prefix` variable) does not seem to be possible due to An Otter Wiki's technical limitations.

### Enabling signing up

By default account registration for the service is disabled. To enable it, add the following configuration to your `vars.yml` file:

```yaml
otterwiki_environment_variables_disable_registration: false
```

### Configuring the mailer (optional)

On An Otter Wiki you can set up a mailer for functions such as password recovery. If you enable the [exim-relay](exim-relay.md) service in your inventory configuration, the playbook will automatically configure it as a mailer for the service.

>[!NOTE]
> Without setting an authentication method such as DKIM, SPF, and DMARC for your hostname, emails are most likely to be quarantined as spam at recipient's mail servers. If you have set up a mail server with the [exim-relay Ansible role](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay), you can enable DKIM signing with it. Refer [its documentation](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay/blob/main/docs/configuring-exim-relay.md#enable-dkim-support-optional) for details.

## Usage

After installation, the An Otter Wiki instance becomes available at the URL specified with `otterwiki_hostname`. With the configuration above, the service is hosted at `https://otterwiki.example.com`.

To get started, open the URL with a web browser, and register the account. **Note that the first registered user becomes an administrator automatically.**

Since account registration is disabled by default, you need to enable it first by setting `otterwiki_environment_variables_disable_registration` to `false` temporarily in order to create your own account.

## Troubleshooting

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3AzvzJe15VMBkGd2CMBctvpVZgmQG5/tree/docs/configuring-otterwiki.md#troubleshooting) on the role's documentation for details.

## Related services

- [DokuWiki](dokuwiki.md) — Lightweight, file-based wiki engine
- [MediaWiki](mediawiki.md) — Popular free and open-source wiki software
