# Postgres Exporter

This playbook can configure [Postgres Exporter](https://github.com/prometheus-community/postgres_exporter) by utilizing [mother-of-all-self-hosting/ansible-role-postgres-exporter](https://github.com/mother-of-all-self-hosting/ansible-role-postgres-exporter.git).


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# postgres_exporter                                                    #
#                                                                      #
########################################################################

postgres_exporter_enabled: true

# To expose the metrics publicly, enable and configure the lines below:
# postgres_exporter_hostname: mash.example.com
# postgres_exporter_path_prefix: /metrics/postgres-exporter

# To protect the metrics with HTTP Basic Auth, enable and configure the lines below:
# postgres_exporter_basicauth_enabled: true
# postgres_exporter_basicauth_user: your_username
# postgres_exporter_basicauth_password: your password

########################################################################
#                                                                      #
# /postgres_exporter                                                   #
#                                                                      #
########################################################################
```

Unless you're scraping the Postgres Exporter metrics from a local [Prometheus](prometheus.md) instance, as described in [Integrating with Postgres Exporter](prometheus.md#integrating-with-postgres-exporter), you will probably wish to expose the metrics publicly so that a remote Prometheus instance can fetch them.

## Usage

After you installed the exporter, your stats will be available on `mash.example.com/metrics/postgres-exporter` with basic auth credentials you configured

