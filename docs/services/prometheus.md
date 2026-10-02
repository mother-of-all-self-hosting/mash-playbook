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
SPDX-FileCopyrightText: 2023 Nikita Chernyi
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 Tiz
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Prometheus

The playbook can install and configure [Prometheus](https://prometheus.io/) for you.

Prometheus is a metrics collection and alerting monitoring solution.

See the project's [documentation](https://prometheus.io/docs/introduction/overview/) to learn what Prometheus does and why it might be useful to you.

For details about configuring the [Ansible role for the Prometheus](https://github.com/mother-of-all-self-hosting/ansible-role-prometheus), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-prometheus/blob/main/docs/configuring-prometheus.md) online
- 📁 `roles/galaxy/prometheus/docs/configuring-prometheus.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- (optional) [Grafana](grafana.md) — Web-based tool for visualizing your Prometheus metrics (time-series)
- (optional) [Traefik](traefik.md) — Reverse-proxy server for exposing Prometheus

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# prometheus                                                           #
#                                                                      #
########################################################################

prometheus_enabled: true

########################################################################
#                                                                      #
# /prometheus                                                          #
#                                                                      #
########################################################################
```

Refer to the role's documentation for details about configuring Prometheus per your preference (such as [Prometheus Node Exporter integration](https://github.com/mother-of-all-self-hosting/ansible-role-prometheus/blob/main/docs/configuring-prometheus.md#integrating-with-prometheus-node-exporter), [scraping other exporter services](https://github.com/mother-of-all-self-hosting/ansible-role-prometheus/blob/main/docs/configuring-prometheus.md#scraping-other-exporter-services), and [exposing the web interface](https://github.com/mother-of-all-self-hosting/ansible-role-prometheus/blob/main/docs/configuring-prometheus.md#exposing-the-web-interface-optional)).

## Related services

- [Grafana](grafana.md) — Web-based tool for visualizing your Prometheus metrics (time-series)
- [Grafana Loki](grafana-loki.md) — Log aggregation system that helps collect, store, and analyze logs in a scalable and efficient manner
- [Prometheus Alertmanager](prometheus-alertmanager.md) — Handle alerts sent by client applications such as the Prometheus server
- [Prometheus Blackbox Exporter](prometheus-blackbox-exporter.md) — Blackbox probing of HTTP/HTTPS/DNS/TCP/ICMP and gRPC endpoints
- [Prometheus Node Exporter](prometheus-node-exporter.md) — Exporter for machine metrics
- [Prometheus Postgres Exporter](prometheus-postgres-exporter.md) — PostgreSQL metric exporter for Prometheus
- [Healthchecks](healthchecks.md) — Cron job monitoring solution
