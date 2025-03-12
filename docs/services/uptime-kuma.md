<!--
SPDX-FileCopyrightText: 2023 Slavi Pantaleev
SPDX-FileCopyrightText: 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Uptime-kuma

[Uptime-kuma](https://uptime.kuma.pet/) is a fancy self-hosted monitoring tool. You can add a monitor for various web services like HTTP, TCP port, Docker Container, PostgreSQL, and so on.


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

# For now, hosting uptime-kuma under a path is not supported.
# See: https://github.com/louislam/uptime-kuma/issues/147
# uptime_kuma_path_prefix: /uptime-kuma

########################################################################
#                                                                      #
# /uptime-kuma                                                         #
#                                                                      #
########################################################################
```

## Usage

When you open the Uptime-kuma Web UI for the first time, it starts a setup wizard where you'll create your admin credentials. You can then add monitors for web services as many as you like.

If you have enabled a self-hosted [ntfy](ntfy.md) server, it is possible to set up the Uptime-kuma instance to have it send notifications to a ntfy's "topic" (channel) when the monitored web service is down, without relaying the notifications through servers owned and controlled by third parties.
