# Prometheus Node Expoter

This playbook can configure [Prometheus Node Exporter](https://github.com/prometheus/node_exporter).

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# prometheus-node-expoter                                              #
#                                                                      #
########################################################################

prometheus_node_exporter_enabled: true
prometheus_node_exporter_basicauth_user: your_username
prometheus_node_exporter_basicauth_password: your password

########################################################################
#                                                                      #
# /prometheus-node-expoter                                             #
#                                                                      #
########################################################################
```
