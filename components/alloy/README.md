<!--
SPDX-FileCopyrightText: 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2026 Suguru Hirahara
SPDX-FileCopyrightText: 2026 sudo-Tiz

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Grafana Alloy

The playbook can install and configure [Grafana Alloy](https://grafana.com/docs/alloy/latest/) for you.

Alloy is Grafana's OpenTelemetry Collector distribution and the successor to Promtail, which reached end of life on March 2, 2026. This role can collect systemd journal entries and files under `/var/log`, then forward them to Loki-compatible endpoints.

For details about configuring the [Ansible role for Alloy](https://github.com/mother-of-all-self-hosting/ansible-role-alloy), see its [configuration guide](https://github.com/mother-of-all-self-hosting/ansible-role-alloy/blob/main/docs/configuring-alloy.md) or `roles/galaxy/alloy/docs/configuring-alloy.md` locally after [fetching the Ansible roles](../../docs/installing.md).

## Dependencies

- (optional; recommended) [Grafana Loki](../loki/README.md) — When both components are enabled, Alloy is automatically configured to send logs to the local Loki instance. Otherwise, configure `alloy_config_clients_custom` with a Loki-compatible endpoint.
- (optional) [Traefik](../traefik/README.md) — Reverse proxy for exposing Alloy metrics. The Alloy API and UI are not exposed by default.

## Configuration

Enable Alloy in `vars.yml` and rerun the [installation](../../docs/installing.md):

```yaml
alloy_enabled: true
```

No log sources are enabled by default. To collect the systemd journal, set `alloy_journald_scraper_enabled: true`; to collect files under `/var/log`, set `alloy_varlog_scraper_enabled: true`. Review the source filters first: enabling the journal scraper includes all units by default, so logs may contain sensitive data. This role does not discover Docker container logs automatically.

## Related services

- [Grafana](../grafana/README.md) — Visualizes metrics and logs
- [Grafana Loki](../loki/README.md) — Stores and queries logs
- [Promtail](../promtail/README.md) — Legacy log agent; migrate to Alloy
