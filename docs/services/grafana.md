# Grafana

[Grafana](https://grafana.com/) is an open and composable observability and data visualization platform, often used with [Prometheus](prometheus.md).


## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# grafana                                                              #
#                                                                      #
########################################################################

grafana_enabled: true

grafana_hostname: mash.example.com
grafana_path_prefix: /grafana

grafana_default_admin_user: admin
# Generating a strong password (e.g. `pwgen -s 64 1`) is recommended
grafana_default_admin_password: ''

########################################################################
#                                                                      #
# /grafana                                                             #
#                                                                      #
########################################################################
```

In the example configuration above, we configure the service to be hosted at `https://mash.example.com/grafana`.

You can remove the `grafana_path_prefix` variable definition, to make it default to `/`, so that the service is served at `https://mash.example.com/`.

### Configuring data sources

Grafana is merely a visualization tool. It needs to pull data from a metrics (time-series) database, like [Prometheus](prometheus.md).

You can add multiple data sources to Grafana.

#### Integrating with a local Prometheus instance

If you're installing [Prometheus](prometheus.md) on the same server, you can hook Grafana to it over the container network with the following **additional** configuration:

```yaml
grafana_provisioning_datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: "http://{{ prometheus_identifier }}:9090"

# Prometheus runs in another container network, so we need to connect to it.
grafana_container_additional_networks_additional:
  - "{{ prometheus_container_network }}"
```

For connecting to a **remote** Prometheus instance, you may need to adjust this configuration somehow.


### Integrating with Prometheus Node Exporter

If you've installed [Prometheus Node Exporter](prometheus-node-exporter.md) on any host (target) scraped by Prometheus, you may wish to install a dashboard for Prometheus Node Exporter.

The Prometheus Node Exporter role exposes a list of URLs containing dashboards (JSON files) in its `prometheus_node_exporter_dashboard_urls` variable.

You can add this **additional** configuration to make the Grafana service pull these dashboards:

```yaml
grafana_dashboard_download_urls: |
  {{
    prometheus_node_exporter_dashboard_urls
  }}
```


## Usage

After installation, you should be able to access your new Gitea instance at the configured URL (see above).

Going there, you'll be taken to the initial setup wizard, which will let you assign some paswords and other configuration.


## Recommended other services

Grafana is just a visualization tool which requires pulling data from a metrics (time-series) database like.

You may be interested in combining it with [Prometheus](prometheus.md).
