<!--
SPDX-FileCopyrightText: 2026 MASH project contributors
SPDX-FileCopyrightText: 2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Vector

The playbook can install and configure [Vector](https://vector.dev/) for you.

Vector is a high-performance observability data pipeline that lets you collect, transform, and route logs and metrics from many sources to many destinations (sinks).

See the project's [documentation](https://vector.dev/docs/) to learn what Vector does and why it might be useful to you.

For details about configuring the [Ansible role for Vector](https://github.com/spatterIight/ansible-role-vector), you can check them via:

- 🌐 [the role's documentation](https://github.com/spatterIight/ansible-role-vector/blob/main/docs/configuring-vector.md) online
- 📁 `roles/galaxy/vector/docs/configuring-vector.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- (optional) [Traefik](traefik.md) — Reverse-proxy server for exposing Vector's API publicly
- (optional) [Grafana Loki](grafana-loki.md) — Log aggregation system that Vector can ship logs to (via a `loki` sink)
- (optional) [Prometheus](prometheus.md) — Metrics collection solution that can scrape Vector's `prometheus_exporter` sink
- (optional) [Grafana](grafana.md) — Web-based tool for visualizing the resulting logs and metrics

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# vector                                                               #
#                                                                      #
########################################################################

vector_enabled: true

########################################################################
#                                                                      #
# /vector                                                              #
#                                                                      #
########################################################################
```

Refer to [this section](https://github.com/spatterIight/ansible-role-vector/blob/main/docs/configuring-vector.md#adjusting-the-playbook-configuration) on the role's documentation for details about integrating Vector with Grafana Loki and Prometheus, and exposing its GraphQL API, etc.

## Usage

After running the command for installation, the Vector instance becomes available.

Refer to [this section](https://github.com/spatterIight/ansible-role-vector/blob/main/docs/configuring-vector.md#usage) on the role's documentation for more details about how to use it.

## Related services

- [Grafana](grafana.md) — Web-based tool for visualizing your Prometheus metrics (time-series)
- [Grafana Loki](grafana-loki.md) — Log aggregation system that helps collect, store, and analyze logs in a scalable and efficient manner
- [Prometheus](prometheus.md) — Metrics collection and alerting monitoring solution
- [Promtail](promtail.md) — Agent which ships the contents of local logs to a private Grafana Loki instance
- [Telegraf](telegraf.md) — A server agent to help you collect metrics from your stacks, sensors, and systems
