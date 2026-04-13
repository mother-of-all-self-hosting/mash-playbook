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

## Dependencies

This service requires the following other services:

- (optional) [Grafana](grafana.md) — web UI that can query the Prometheus datasource (connection) and display the logs
- (optional) [Traefik](traefik.md) — reverse-proxy server for exposing Prometheus

## Adjusting the playbook configuration

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

### Integrating with Prometheus Node Exporter

If you've installed [Prometheus Node Exporter](prometheus-node-exporter.md) on the same host, you can make Prometheus scrape its metrics by adding the following configuration to your `vars.yml` file:

```yaml
prometheus_self_node_scraper_enabled: true
prometheus_self_node_scraper_static_configs_target: "{{ prometheus_node_exporter_identifier }}:9100"
```

>[!NOTE]
> To scrape a *remote* Prometheus Node Exporter instance, add the configuration to `prometheus_config_scrape_configs_additional` described below.

### Scraping other exporter services

To make Prometheus useful, you'll need to get it scrape one or more hosts by adjusting the configuration. You can add your own scrape configuration to `prometheus_config_scrape_configs_additional` as below (adapt to your needs):

```yaml
prometheus_config_scrape_configs_additional:
  - job_name: some_job
    metrics_path: /metrics
    scrape_interval: 120s
    scrape_timeout: 120s
    static_configs:
      - targets:
          - some-host:8080

  - job_name: another_job
    metrics_path: /metrics
    scrape_interval: 120s
    scrape_timeout: 120s
    static_configs:
      - targets:
          - another-host:8080
```

### Disabling scraping from own process

By default, Prometheus is configured to scrape (collect metrics from) its own process. You can disable this behavior by adding the following configuration to your `vars.yml` file:

```yaml
prometheus_self_process_scraper_enabled: false
```

### Exposing the web interface

To expose the Prometheus web interface publicly, add the following configuration to your `vars.yml` file (adapt to your needs).

```yaml
prometheus_hostname: prometheus.example.com
```

When exposing it, you should consider to set up [HTTP Basic Authentication](https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication) **or anyone would be able to read your metrics**. To enable the HTTP Basic authentication, add the following configuration to your `vars.yml` file:

```yaml
prometheus_container_labels_metrics_middleware_basic_auth_enabled: true

# See https://doc.traefik.io/traefik/middlewares/http/basicauth/#users for details.
prometheus_container_labels_metrics_middleware_basic_auth_users: ""
```

## Related services

- [Grafana](grafana.md) — a web-based tool for visualizing your Prometheus metrics (time-series)
- [Grafana Loki](grafana-loki.md) — a log aggregation system that helps collect, store, and analyze logs in a scalable and efficient manner (like Prometheus, but for logs)
- [Prometheus Alertmanager](prometheus-alertmanager.md) — Handle alerts sent by client applications such as the Prometheus server
- [prometheus-blackbox-exporter](prometheus-blackbox-exporter.md) — Blackbox probing of HTTP/HTTPS/DNS/TCP/ICMP and gRPC endpoints
- [prometheus-node-exporter](prometheus-node-exporter.md) — an exporter for machine metrics
- [prometheus-postgres-exporter](prometheus-postgres-exporter.md) — an exporter for monitoring a [Postgres](postgres.md) database server
- [Healthchecks](healthchecks.md) — a simple and Effective Cron Job Monitoring solution
