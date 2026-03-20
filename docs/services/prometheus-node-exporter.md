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

# Prometheus Node Exporter

The playbook can install and configure [Prometheus Node Exporter](https://github.com/prometheus/node_exporter) for you.

Prometheus Node Exporter is a Prometheus exporter for hardware and OS metrics exposed by *NIX kernels.

See the project's [documentation](https://github.com/prometheus/node_exporter/blob/master/README.md) to learn what Prometheus Node Exporter does and why it might be useful to you.

## Dependencies

This service requires the following other services:

- [Prometheus](prometheus.md) — database for storing metrics
- (optional) [Grafana](grafana.md) — web UI that can query the Prometheus datasource (connection) and display the logs
- (optional) [Traefik](traefik.md) — reverse-proxy server for exposing Prometheus Node Exporter

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# prometheus_node_exporter                                             #
#                                                                      #
########################################################################

prometheus_node_exporter_enabled: true

# To expose the metrics publicly, enable and configure the lines below:
# prometheus_node_exporter_hostname: mash.example.com
# prometheus_node_exporter_path_prefix: /metrics/mash-prometheus-node-exporter

# To protect the metrics with HTTP Basic Auth, enable and configure the lines below.
# See: https://doc.traefik.io/traefik/middlewares/http/basicauth/#users
# prometheus_node_exporter_container_labels_metrics_middleware_basic_auth_enabled: true
# prometheus_node_exporter_container_labels_metrics_middleware_basic_auth_users: ''

########################################################################
#                                                                      #
# /prometheus_node_exporter                                            #
#                                                                      #
########################################################################
```

Unless you're scraping the Prometheus Node Exporter metrics from a local [Prometheus](prometheus.md) instance, as described in [Integrating with Prometheus Node Exporter](prometheus.md#integrating-with-prometheus-node-exporter), you will probably wish to expose the metrics publicly so that a remote Prometheus instance can fetch them.

## Usage

After you installed the node exporter, your node stats will be available on `mash.example.com/metrics/mash-prometheus-node-exporter` with the basic auth credentials you configured.

To integrate Prometheus Node Exporter with a [Prometheus](prometheus.md) instance, see the [Integrating with Prometheus Node Exporter](prometheus.md#integrating-with-prometheus-node-exporter) section of the documentation.


## Recommended other services

- [Promtail](promtail.md) — an agent which ships the contents of local logs to a private [Grafana Loki](grafana-loki.md) instance
