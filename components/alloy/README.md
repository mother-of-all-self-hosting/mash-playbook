<!--
SPDX-FileCopyrightText: 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2026 Suguru Hirahara
SPDX-FileCopyrightText: 2026 spatterlight
SPDX-FileCopyrightText: 2026 sudo-Tiz

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Grafana Alloy

The playbook can install and configure [Grafana Alloy](https://grafana.com/docs/alloy/latest/) for you.

Alloy is Grafana's OpenTelemetry Collector distribution and the successor to Promtail, which reached end of life on March 2, 2026. It can collect systemd journal entries and files under `/var/log`, then forward them to Loki-compatible endpoints.

See the project's [documentation](https://grafana.com/docs/alloy/latest/) to learn what Alloy does and why it might be useful to you.

For details about configuring the [Ansible role for Alloy](https://github.com/mother-of-all-self-hosting/ansible-role-alloy), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-alloy/blob/main/docs/configuring-alloy.md) online
- 📁 `roles/galaxy/alloy/docs/configuring-alloy.md` locally, if you have [fetched the Ansible roles](../../docs/installing.md)

## Dependencies

This service requires the following other services:

- (optional; recommended) [Grafana Loki](../loki/README.md) — Log aggregation system that Alloy is automatically configured to send logs to, when it is enabled. Otherwise, configure `alloy_config_clients_custom` with a Loki-compatible endpoint
- (optional) [Traefik](../traefik/README.md) — Reverse-proxy server for exposing Alloy's metrics or UI

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../../docs/installing.md) process:

```yaml
########################################################################
#                                                                      #
# alloy                                                                #
#                                                                      #
########################################################################

alloy_enabled: true

########################################################################
#                                                                      #
# /alloy                                                               #
#                                                                      #
########################################################################
```

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-alloy/blob/main/docs/configuring-alloy.md#adjusting-the-playbook-configuration) on the role's documentation for other settings such as the ones for log sources.

>[!NOTE]
> Because no log sources are enabled by default, Alloy does not do anything in its default configuration.

## Usage

After running the command for installation, the Alloy instance becomes available.

## Related services

- [Grafana](../grafana/README.md) — Web-based tool for visualizing your Prometheus metrics (time-series)
- [Grafana Loki](../loki/README.md) — Log aggregation system that helps collect, store, and analyze logs in a scalable and efficient manner
- [Promtail](../promtail/README.md) — End-of-life log agent; migrate to Alloy
