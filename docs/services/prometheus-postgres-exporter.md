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

# Prometheus Postgres Exporter

The playbook can install and configure [Prometheus Postgres Exporter](https://github.com/prometheus-community/postgres_exporter) for you.

Prometheus Postgres Exporter is a Prometheus exporter for PostgreSQL server metrics.

See the project's [documentation](https://github.com/prometheus-community/postgres_exporter/blob/master/README.md) to learn what Prometheus Postgres Exporter does and why it might be useful to you.

## Dependencies

This service requires the following other services:

- [Prometheus](prometheus.md) — database for storing metrics
- (optional) [Grafana](grafana.md) — web UI that can query the Prometheus datasource (connection) and display the logs
- (optional) [Traefik](traefik.md) — reverse-proxy server for exposing Prometheus Postgres Exporter

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# prometheus_postgres_exporter                                         #
#                                                                      #
########################################################################

prometheus_postgres_exporter_enabled: true

# To expose the metrics publicly, enable and configure the lines below:
# prometheus_postgres_exporter_hostname: mash.example.com
# prometheus_postgres_exporter_path_prefix: /metrics/mash-prometheus-postgres-exporter

# To protect the metrics with HTTP Basic Auth, enable and configure the lines below.
# See: https://doc.traefik.io/traefik/middlewares/http/basicauth/#users
# prometheus_postgres_exporter_container_labels_metrics_middleware_basic_auth_enabled: true
# prometheus_postgres_exporter_container_labels_metrics_middleware_basic_auth_users: ''

########################################################################
#                                                                      #
# /prometheus_postgres_exporter                                        #
#                                                                      #
########################################################################
```

Unless you're scraping the Postgres Exporter metrics from a local [Prometheus](prometheus.md) instance, as described in [Integrating with Postgres Exporter](prometheus.md#integrating-with-postgres-exporter), you will probably wish to expose the metrics publicly so that a remote Prometheus instance can fetch them.

## Usage

After you installed the exporter, your stats will be available on `mash.example.com/metrics/mash-prometheus-postgres-exporter` with basic auth credentials you configured
