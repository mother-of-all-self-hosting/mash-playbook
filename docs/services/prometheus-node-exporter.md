# Prometheus Node Expoter

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
prometheus_node_exporter_hostname: mash.example.com
prometheus_node_exporter_path_prefix: /metrics/node-exporter
prometheus_node_exporter_basicauth_user: your_username
prometheus_node_exporter_basicauth_password: your password

########################################################################
#                                                                      #
# /prometheus-node-exporter                                            #
#                                                                      #
########################################################################
```

## Usage

After you installed the node exporter, your node stats will be available on `mash.example.com/metrics/node-exporter` with basic auth credentials you configured
