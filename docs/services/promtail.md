# Promtail

[Promtail](https://grafana.com/oss/promtail/) agent is a log aggregation system designed to store and query logs from all your applications and infrastructure. It integrates nicely with [Grafana Loki](./grafana-loki.md).


## Dependencies

This service requires the following other services:

- [Grafana Loki](grafana-loki.md) — a log-storage server where you'd be sending the logs
- (optional) [Traefik](traefik.md) — a reverse-proxy server, if you're exposing Promtail's metrics or API


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# promtail                                                             #
#                                                                      #
########################################################################

promtail_enabled: true

# See "Configuring scrapers" below.
# You need to enable at least one scraper to have Promtail do anything.

# If you haven't enabled Grafana Loki on the same server, you will need
# to define some clients to push logs to.
# See "Configuring clients" below.

########################################################################
#                                                                      #
# /promtail                                                            #
#                                                                      #
########################################################################
```

### Configuring scrapers

**No scrapers are enabled by default**. As such, Promtail does not do anything in its default configuration.

Below, we show you a few built-in scrapers you can easily enable, as well as how to create your own custom ones.

#### Scraping systemd-journald logs

To scrape the [systemd Journal](https://wiki.archlinux.org/title/Systemd/Journal), enable the already-prepared scraper for this with this additional `vars.yml` configuration:

```yml
# Some distros only store a non-persistent (in-memory) journal in a path like in `/run/log/journal`.
# Others may be using a path different than `/var/log/journal`.
# Adjust accordingly.
promtail_journald_scraper_enabled: true
promtail_journald_scraper_host_path: /var/log/journal
```

#### Scraping textual log files (/var/log, etc.)

A lot of distros dump textual log files in `/var/log`. To scrape them, enable the already-prepared scraper for this with this additional `vars.yml` configuration:

```yml
promtail_varlog_scraper_enabled: true
# Consider adjusting this if you'd like to scrape a different path
# promtail_varlog_scraper_host_path: /var/log
```

You can see the configuration for this scraper in the `promtail_varlog_scraper_config` variable in [the `defaults/main.yml` file](https://github.com/mother-of-all-self-hosting/ansible-role-promtail/blob/main/defaults/main.yml) of the ansible-role-promtail Ansible role.

When using this scraper, beware that **log-rotation may lead to double-ingestion** as described [here](https://grafana.com/docs/loki/latest/send-data/promtail/configuration/#example-static-config) in the official documentation:

> If you are rotating logs, be careful when using a wildcard pattern like *.log, and make sure it doesn’t match the rotated log file. For example, if you move your logs from server.log to server.01-01-1970.log in the same directory every night, a static config with a wildcard search pattern like *.log will pick up that new file and read it, effectively causing the entire days logs to be re-ingested.

To work around it, you may wish to adjust `promtail_varlog_scraper_config_labels_path_suffix` which defaults to `/**/*log`.

#### Scraping other directories

Besides the predefined scrapers described above, you can also define your own additional ones with the help of these variables:

- `promtail_container_additional_mounts_custom`, to mount additional paths into the Promtail container
- `promtail_config_scrape_configs_custom`, to inject additional jobs into Promtail's `scrape_configs` configuration. See `promtail_journald_scraper_config` and `promtail_varlog_scraper_config` for an example

Here's an example for scraping some hypothethical SSH logs stored somewhere:

```yml
promtail_container_additional_mounts_custom:
  - "type=bind,source=</path/to/ssh/logs>,target=/data/ssh,readonly"

promtail_config_scrape_configs_custom:
  - job_name: ssh
    static_configs:
    - localhost
      __path__: /data/ssh
      labels:
        job: ssh
```

##### Scraping syslog

The following example demonstrates the use of rsyslog and promtail to scrape syslog logs.

**Prerequisites**: Edit your rsyslog configuration in order to send logs to `promtail.*``
This could be done by creating a `/etc/rsyslog.d/00-promtail-relay.conf` file with the following content:

```
*.* action(type="omfwd" protocol="tcp" target="<promtail_host>" port="<promtail_port>" Template="RSYSLOG_SyslogProtocol23Format" TCP_Framing="octet-counted" KeepAlive="on")
```

The port is a port number that you come up with yourself (e.g. `1234`).

First, you need a custom scrape configuration which tells Promtail to listen on this port (replace `SOME_PORT_NUMBER_IN_CONTAINER` with your port number of choice):

```yaml
promtail_config_scrape_configs_custom:
  - job_name: syslog
    syslog:
      listen_address: 0.0.0.0:SOME_PORT_NUMBER_IN_CONTAINER
      labels:
        job: syslog
    relabel_configs:
      - source_labels: [__syslog_message_hostname]
        target_label: host
      - source_labels: [__syslog_message_hostname]
        target_label: hostname
      - source_labels: [__syslog_message_severity]
        target_label: level
      - source_labels: [__syslog_message_app_name]
        target_label: application
      - source_labels: [__syslog_message_facility]
        target_label: facility
      - source_labels: [__syslog_connection_hostname]
        target_label: connection_hostname
```

You'd then need to expose this TCP port outside of the container, so that the local host (or remote host) can reach it.

To expose it on the loopback interface (reachable only from the same machine), use a configuration like this:
```yaml
promtail_container_extra_arguments_custom:
  - "-p 127.0.0.1:1234:1234"
```


### Configuring clients

If you've also enabled [Grafana Loki](./grafana-loki.md) on the same server, Promtail will automatically be configured to push logs to it.

Otherwise, you will need to extend the Promtail configuration by specifying clients to push to. Add something like this to your `vars.yml` configuration:

```yml
promtail_config_clients_custom:
  # Note the double /loki/loki.
  # This assumes Loki is installed at a `/loki` path-prefix.
  - url: https://mash.example.com/loki/loki/api/v1/push
    tenant_id: some-tenant-id-here
```

For more information about configuring clients, see the [Promtail `clients` configuration reference](https://grafana.com/docs/loki/latest/send-data/promtail/configuration/#clients).


### Exposing the web interface

There are 2 reasons to expose Promtail to the public web:

1. So that you can scrape its Prometheus-compatible `/metrics` endpoint or observe its current `/targets` via API
2. So that you can use [loki_push_api](https://grafana.com/docs/loki/latest/send-data/promtail/configuration/#loki_push_api) and push logs to Promtail (so that it can forward them onto its [clients](#configuring-clients)). This feature likely needs to be enabled explicitly.

To expose Promtail to the web, you need to assign a hostname in `promtail_hostname` and optionally a path-prefix.

You can then decide whether you'd like to expose Promtail's whole API via `promtail_container_labels_api_enabled` or just its metrics endpoint via `promtail_container_labels_metrics_enabled`.

Consult the `defaults/main.yml` file for variables related to these.

When exposing metrics, and especially the whole API, it's important to protected them. The Promtail Ansible role has variables that let you easily set up [HTTP Basic Authentication](https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication) via `promtail_container_labels_api_traefik_middleware_basic_auth_*` and `promtail_container_labels_metrics_traefik_middleware_basic_auth_*` variables.



## Recommended other services

- [Grafana Loki](grafana-loki.md) — a storage server for your logs compatible with Promtail
- [Grafana](grafana.md) — a web-based tool for visualizing your Promtail logs (stored in [Grafana Loki](grafana-loki.md) or elsewhere)
