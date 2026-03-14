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
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Uptime Kuma

The playbook can install and configure [Uptime Kuma](https://uptime.kuma.pet/) for you.

Uptime Kuma is a fancy self-hosted monitoring tool similar to [Uptime Robot](https://uptimerobot.com/). It has functions such as monitoring uptime for HTTP(s), TCP, DNS Record, Steam Game Server, and Docker Containers, etc.

See the project's [documentation](https://github.com/louislam/uptime-kuma/wiki) to learn what Uptime Kuma does and why it might be useful to you.

For details about configuring the [Ansible role for Uptime Kuma](https://github.com/mother-of-all-self-hosting/ansible-role-uptime_kuma), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-uptime_kuma/blob/main/docs/configuring-uptime-kuma.md) online
- 📁 `roles/galaxy/uptime_kuma/docs/configuring-uptime-kuma.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server
- (optional) [Apprise API](apprise.md)
- (optional) [exim-relay](exim-relay.md) mailer
- (optional) [Gotify](gotify.md)
- (optional) [ntfy](ntfy.md)

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# uptime_kuma                                                          #
#                                                                      #
########################################################################

uptime_kuma_enabled: true

uptime_kuma_hostname: uptime-kuma.example.com

########################################################################
#                                                                      #
# /uptime_kuma                                                         #
#                                                                      #
########################################################################
```

**Note**: hosting Uptime Kuma under a subpath (by configuring the `uptime_kuma_path_prefix` variable) does not seem to be possible due to Uptime Kuma's technical limitations.

## Usage

After running the command for installation, the Uptime Kuma instance becomes available at the URL specified with `uptime_kuma_hostname`. With the configuration above, the service is hosted at `https://uptime-kuma.example.com`.

To get started, open the URL with a web browser, and follow the set up wizard where you can create your admin user and configure the service. You can add monitors as many as you like.

### Adding monitors types

Uptime Kuma does not only support web services but also databases. As the service is internally connected to the ones which this playbook supports, i.e., [Postgres](postgres.md), [MariaDB](mariadb.md), and [MongoDB](mongodb.md), you can set up monitors for them by specifying a connection string for each of them.

### Adding notifications

If you have enabled [Apprise API](apprise.md), [ntfy](ntfy.md), and/or [Gotify](gotify.md) services, it is possible to set up the Uptime Kuma instance to have it send notifications to them internally when the monitored service is down, without relaying them through servers owned and controlled by third parties.

It is also possible to have the Uptime Kuma instance send notifications with a SMTP server. If you enable the [exim-relay](exim-relay.md) service in your inventory configuration, the playbook will automatically configure it as a mailer for the service. To actually have the service use (and get messages sent through the exim-relay service), you will need to adjust settings on the service's UI after the service is installed.

>[!WARNING]
> Without setting an authentication method such as DKIM, SPF, and DMARC for your hostname, emails are most likely to be quarantined as spam at recipient's mail servers. The worst scenario is that your server's IP address or hostname will be included in the spam list such as the one managed by [Spamhaus](https://www.spamhaus.org/), depending on the reputation. As the exim-relay service supports DKIM signing, refer to [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay/blob/main/docs/configuring-exim-relay.md#enable-dkim-support-optional) for details about how to set it up.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting//ansible-role-uptime_kuma/blob/main/docs/configuring-uptime-kuma.md#troubleshooting) on the role's documentation for details.

## Related services

- [Gotify](gotify.md) — Simple server for sending and receiving messages
- [ntfy](ntfy.md) — Simple HTTP-based pub-sub notification service to send you push notifications from any computer
- [Statusnook](statusnook.md) — Self-hosted status page deployment service
