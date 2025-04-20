<!--
SPDX-FileCopyrightText: 2023 Slavi Pantaleev
SPDX-FileCopyrightText: 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Uptime Kuma

[Uptime Kuma](https://uptime.kuma.pet/) is a fancy self-hosted monitoring tool similar to [Uptime Robot](https://uptimerobot.com/). It has functions such as below:

- Monitoring uptime for HTTP(s) / TCP / HTTP(s) Keyword / HTTP(s) Json Query / Ping / DNS Record / Push / Steam Game Server / Docker Containers
- Fancy, Reactive, Fast UI/UX
- Notifications via Matrix, Telegram, Discord, Gotify, Slack, Pushover, Email (SMTP), and [90+ notification services](https://github.com/louislam/uptime-kuma/tree/master/src/components/notifications)
- 20-second intervals
- [Multi-Language](https://github.com/louislam/uptime-kuma/tree/master/src/lang)
- Multiple status pages
- Map status pages to specific domains
- Ping chart
- Certificate info
- Proxy support
- 2FA support

✨ Kuma (くま/熊) means bear 🐻 in Japanese.


## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# uptime-kuma                                                          #
#                                                                      #
########################################################################

uptime_kuma_enabled: true

uptime_kuma_hostname: mash.example.com

# For now, hosting Uptime Kuma under a path is not supported.
# See: https://github.com/louislam/uptime-kuma/issues/147
# uptime_kuma_path_prefix: /uptime-kuma

########################################################################
#                                                                      #
# /uptime-kuma                                                         #
#                                                                      #
########################################################################
```

## Usage

When you open the Uptime Kuma's web UI for the first time, it starts a setup wizard where you'll create your admin credentials. You can then add monitors for web services as many as you like.

If you have enabled a self-hosted [ntfy](ntfy.md) server, it is possible to set up the Uptime Kuma instance to have it send notifications to a ntfy's "topic" (channel) when the monitored web service is down, without relaying them through servers owned and controlled by third parties.
