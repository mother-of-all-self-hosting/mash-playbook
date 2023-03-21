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
# prometheus_node_exporter_path_prefix: /metrics/node-exporter

# To protect the metrics with HTTP Basic Auth, enable and configure the lines below:
# prometheus_node_exporter_basicauth_enabled: true
# prometheus_node_exporter_basicauth_user: your_username
# prometheus_node_exporter_basicauth_password: your password

########################################################################
#                                                                      #
# /prometheus-node-exporter                                            #
#                                                                      #
########################################################################
```

Unless you're scraping the Prometheus Node Exporter metrics from a local [Prometheus](prometheus.md) instance, as described in [Integrating with Prometheus Node Exporter](prometheus.md#integrating-with-prometheus-node-exporter), you will probably wish to expose the metrics publicly so that a remote Prometheus instance can fetch them.

## Usage

After you installed the node exporter, your node stats will be available on `mash.example.com/metrics/node-exporter` with basic auth credentials you configured

To integrate Prometheus Node Exporter with a [Prometheus](prometheus.md) instance, see the [Integrating with Prometheus Node Exporter](prometheus.md#integrating-with-prometheus-node-exporter) section of the documentation.
