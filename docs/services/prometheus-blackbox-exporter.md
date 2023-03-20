# Prometheus Blackbox Exporter

This playbook can configure [Prometheus Blackbox Exporter](https://github.com/prometheus/blackbox_exporter).

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# prometheus-blackbox-exporter                                         #
#                                                                      #
########################################################################

prometheus_blackbox_exporter_enabled: true

# if you want to export blackbox's probe endpoint, uncomment and adjust the following vars

# prometheus_blackbox_exporter_hostname: mash.example.com
# prometheus_blackbox_exporter_path_prefix: /metrics/blackbox-exporter
# prometheus_blackbox_exporter_basicauth_user: your_username
# prometheus_blackbox_exporter_basicauth_password: your password

########################################################################
#                                                                      #
# /prometheus-blackbox-exporter                                        #
#                                                                      #
########################################################################
```

## Usage

After you've installed the blackbox exporter, your blackbox prober will be available on `mash.example.com/metrics/blackbox-exporter` with the basic auth credentials you've configured if hostname and path prefix where provided
