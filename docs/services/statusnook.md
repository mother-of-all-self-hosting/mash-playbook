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

# Statusnook

The playbook can install and configure [Statusnook](https://statusnook.com/) for you.

Statusnook is a self-hosted status page deployment service.

See the project's [documentation](https://statusnook.com/) to learn what Statusnook does and why it might be useful to you.

For details about configuring the [Ansible role for Statusnook](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az4Ki52caKbH1y9jFNdKzQnc8WH1Jd), you can check them via:

- 🌐 [the role's documentation](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az4Ki52caKbH1y9jFNdKzQnc8WH1Jd/tree/docs/configuring-statusnook.md) online
- 📁 `roles/galaxy/statusnook/docs/configuring-statusnook.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server
- (optional) [exim-relay](exim-relay.md) mailer

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# statusnook                                                           #
#                                                                      #
########################################################################

statusnook_enabled: true

statusnook_hostname: statusnook.example.com

########################################################################
#                                                                      #
# /statusnook                                                          #
#                                                                      #
########################################################################
```

**Note**: hosting Statusnook under a subpath (by configuring the `statusnook_path_prefix` variable) does not seem to be possible due to Statusnook's technical limitations.

### Configuring the mailer (optional)

On Statusnook you can set up a mailer for functions such as password recovery. If you enable the [exim-relay](exim-relay.md) service in your inventory configuration, the playbook will automatically configure it as a mailer for the service.

To actually have the service use (and get messages sent through the exim-relay service), you will need to adjust settings on the service's UI after the service is installed.

>[!WARNING]
> Without setting an authentication method such as DKIM, SPF, and DMARC for your hostname, emails are most likely to be quarantined as spam at recipient's mail servers. The worst scenario is that your server's IP address or hostname will be included in the spam list such as the one managed by [Spamhaus](https://www.spamhaus.org/), depending on the reputation. As the exim-relay service supports DKIM signing, refer to [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay/blob/main/docs/configuring-exim-relay.md#enable-dkim-support-optional) for details about how to set it up.

## Usage

After running the command for installation, the Statusnook instance becomes available at the URL specified with `statusnook_hostname`. With the configuration above, the service is hosted at `https://statusnook.example.com`.

To get started, open the URL with a web browser, and follow the set up wizard.

## Troubleshooting

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az4Ki52caKbH1y9jFNdKzQnc8WH1Jd/tree/docs/configuring-statusnook.md#troubleshooting) on the role's documentation for details.

## Related services

- [Uptime Kuma](uptime-kuma.md) — Fancy self-hosted monitoring tool
