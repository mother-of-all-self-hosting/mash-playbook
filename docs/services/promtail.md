<!--
SPDX-FileCopyrightText: 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Promtail

>[!WARNING]
> Promtail has reached end-of-life status on March 2, 2026. If you are currently using Promtail, you should plan your [migration to Alloy](https://grafana.com/docs/loki/latest/setup/migrate/migrate-to-alloy/).

The playbook can install and configure [Promtail](https://grafana.com/docs/loki/latest/send-data/promtail/) for you.

Promtail agent is a log aggregation system designed to store and query logs from all your applications and infrastructure. It integrates nicely with [Grafana Loki](grafana-loki.md).

See the project's [documentation](https://grafana.com/docs/loki/latest/send-data/promtail/) to learn what Promtail does and why it might be useful to you.

For details about configuring the [Ansible role for Promtail](https://github.com/mother-of-all-self-hosting/ansible-role-promtail), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-promtail/blob/main/docs/configuring-promtail.md) online
- 📁 `roles/galaxy/promtail/docs/configuring-promtail.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Grafana Loki](grafana-loki.md) — Log aggregation system that helps collect, store, and analyze logs in a scalable and efficient manner
- (optional) [Traefik](traefik.md) — Reverse-proxy server for exposing Promtail's metrics or API

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# promtail                                                             #
#                                                                      #
########################################################################

promtail_enabled: true

########################################################################
#                                                                      #
# /promtail                                                            #
#                                                                      #
########################################################################
```

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-promtail/blob/main/docs/configuring-promtail.md#adjusting-the-playbook-configuration) on the role's documentation for other settings such as the one for scrapers.

>[!NOTE]
> Because no scrapers are enabled by default, Promtail does not do anything in its default configuration.

## Related services

- [Grafana](grafana.md) — Web-based tool for visualizing your Prometheus metrics (time-series)
- [Grafana Loki](grafana-loki.md) — Log aggregation system that helps collect, store, and analyze logs in a scalable and efficient manner
