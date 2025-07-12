# Postgres Exporter

This playbook can configure [Postgres Exporter](https://github.com/prometheus-community/postgres_exporter) by utilizing [mother-of-all-self-hosting/ansible-role-postgres-exporter](https://github.com/mother-of-all-self-hosting/ansible-role-prometheus-postgres-exporter.git).


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
