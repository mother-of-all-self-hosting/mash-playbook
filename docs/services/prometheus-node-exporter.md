# Prometheus Node Exporter

This playbook can configure [Prometheus Node Exporter](https://github.com/prometheus/node_exporter).


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# prometheus-node-exporter                                             #
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
# /prometheus-node-exporter                                            #
#                                                                      #
########################################################################
```

Unless you're scraping the Prometheus Node Exporter metrics from a local [Prometheus](prometheus.md) instance, as described in [Integrating with Prometheus Node Exporter](prometheus.md#integrating-with-prometheus-node-exporter), you will probably wish to expose the metrics publicly so that a remote Prometheus instance can fetch them.

## Usage

After you installed the node exporter, your node stats will be available on `mash.example.com/metrics/mash-prometheus-node-exporter` with the basic auth credentials you configured.

To integrate Prometheus Node Exporter with a [Prometheus](prometheus.md) instance, see the [Integrating with Prometheus Node Exporter](prometheus.md#integrating-with-prometheus-node-exporter) section of the documentation.


## Recommended other services

- [Promtail](promtail.md) — an agent which ships the contents of local logs to a private [Grafana Loki](grafana-loki.md) instance
