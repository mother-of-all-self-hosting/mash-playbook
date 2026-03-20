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

########################################################################
#                                                                      #
# /prometheus_postgres_exporter                                        #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the Prometheus Postgres Exporter instance becomes available.

### Expose metrics internally

If Prometheus Postgres Exporter and Prometheus do not share a network (like Traefik), you can connect the Prometheus Postgres Exporter container network to Prometheus by adding the following configuration to your `vars.yml` file:

```yaml
prometheus_container_additional_networks_custom:
  - "{{ prometheus_postgres_exporter_container_network }}"
```

### Expose metrics publicly

If Prometheus Postgres Exporter metrics are not scraped from a local Prometheus instance, you can expose the metrics publicly so that a remote instance can fetch them.

When exposing metrics publicly, you should consider to set up [HTTP Basic Authentication](https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication) **or anyone would be able to read your metrics**.

To expose the metrics publicly, add the following configuration to your `vars.yml` file (adapt to your needs):

```yaml
mash_playbook_metrics_exposure_enabled: true
mash_playbook_metrics_exposure_hostname: mash.example.com
```

It will expose the metrics at `https://mash.example.com/metrics/mash-prometheus-postgres-exporter`.

To enable the HTTP Basic authentication, add the following configuration to your `vars.yml` file (adapt to your needs):

```yaml
prometheus_postgres_exporter_container_labels_metrics_middleware_basic_auth_enabled: true

# See https://doc.traefik.io/traefik/middlewares/http/basicauth/#users for details.
prometheus_postgres_exporter_container_labels_metrics_middleware_basic_auth_users: ""
```
