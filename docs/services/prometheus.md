# Prometheus

[Prometheus](https://prometheus.io/) is a metrics collection and alerting monitoring solution.


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

By default, Prometheus is configured to scrape (collect metrics from) its own process. If you wish to disable this behavior, use `prometheus_self_process_scraper_enabled: false`.

To make Prometheus useful, you'll need to make it scrape one or more hosts by adjusting the configuration.


### Integrating with Prometheus Node Exporter

If you've installed [Prometheus Node Exporter](prometheus-node-exporter.md) on the same host, you can make Prometheus scrape its metrics with the following **additional configuration**:

```yaml
prometheus_self_node_scraper_enabled: true
prometheus_self_node_scraper_static_configs_target: "{{ prometheus_node_exporter_identifier }}:9100"

# node-exporter runs in another container network, so we need to connect to it.
prometheus_container_additional_networks:
  - "{{ prometheus_node_exporter_container_network }}"
```

To scrape a **remote** Prometheus Node Exporter instance, do not use `prometheus_self_node_scraper_*`, but rather follow the [Scraping any other exporter service](#scraping-any-other-exporter-service) guide below.


### Scraping any other exporter service

To inject your own scrape configuration, use the `prometheus_config_scrape_configs_additional` variable that's part of the [ansible-role-prometheus](https://github.com/mother-of-all-self-hosting/ansible-role-prometheus) Ansible role.

Example **additional** configuration:

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

If you're scraping others services running in containers over the container network, make sure the Prometheus container is connected to their own network by adjusting `prometheus_container_additional_networks` as demonstrated above for [Integrating with Prometheus Node Exporter](#integrating-with-prometheus-node-exporter).


### Exposing the web interface

By setting a hostname you will expose prometheus on this domain.
Usually you should also set up basic_auth in this case, otherwise everyone will be able to access your metrics

```yaml
prometheus_hostname: prometheus.example.com

# Uncommenting the following lines allows you to configure basic auth
# prometheus_container_labels_metrics_middleware_basic_auth_enabled: true
# Use `htpasswd -nb USERNAME PASSSWORD` to generate the users below.
# prometheus_container_labels_metrics_middleware_basic_auth_users: ''
```

## Recommended other services

- [Grafana](grafana.md) — a web-based tool for visualizing your Prometheus metrics (time-series)
- [Grafana Loki](grafana-loki.md) — a log aggregation system that helps collect, store, and analyze logs in a scalable and efficient manner (like Prometheus, but for logs)
- [prometheus-blackbox-exporter](prometheus-blackbox-exporter.md) — Blackbox probing of HTTP/HTTPS/DNS/TCP/ICMP and gRPC endpoints
- [prometheus-node-exporter](prometheus-node-exporter.md) — an exporter for machine metrics
- [prometheus-postgres-exporter](prometheus-postgres-exporter.md) — an exporter for monitoring a [Postgres](postgres.md) database server
- [Healthchecks](healthchecks.md) — a simple and Effective Cron Job Monitoring solution
