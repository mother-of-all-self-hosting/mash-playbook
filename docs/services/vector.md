<!--
SPDX-FileCopyrightText: 2026 MASH project contributors

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Vector

The playbook can install and configure [Vector](https://vector.dev/) for you.

Vector is a high-performance observability data pipeline that lets you collect, transform, and route logs and metrics from many sources to many destinations (sinks).

See the project's [documentation](https://vector.dev/docs/) to learn what Vector does and why it might be useful to you.

For details about configuring the [Ansible role for Vector](https://github.com/spatterIight/ansible-role-vector), you can check them via:

- 🌐 [the role's `defaults/main.yml`](https://github.com/spatterIight/ansible-role-vector/blob/main/defaults/main.yml) online
- 📁 `roles/galaxy/vector/defaults/main.yml` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- (optional) [Traefik](traefik.md) — Reverse-proxy server for exposing Vector's API publicly
- (optional) [Grafana Loki](grafana-loki.md) — Log aggregation system that Vector can ship logs to (via a `loki` sink)
- (optional) [Prometheus](prometheus.md) — Metrics collection solution that can scrape Vector's `prometheus_exporter` sink
- (optional) [Grafana](grafana.md) — Web-based tool for visualizing the resulting logs and metrics

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# vector                                                               #
#                                                                      #
########################################################################

vector_enabled: true

########################################################################
#                                                                      #
# /vector                                                              #
#                                                                      #
########################################################################
```

## Usage

By default Vector is configured to output its own internal logs and write them as JSON to the console. After running the command for installation you can observe its output with:

```sh
journalctl -fu mash-vector
```

To extend the default configuration we show you a few built-in log sources you can easily enable below. To build your own extend the default sources, transforms, and sinks through the `vector_sources_custom`, `vector_transforms_custom`, and `vector_sinks_custom` variables.

### Collecting system logs (journald and `/var/log`)

To collect the host's systemd journal and/or textual log files under `/var/log`, enable the built-in log sources:

```yaml
# Collect the host's systemd journal
vector_journald_source_enabled: true

# Collect textual log files found under /var/log
vector_varlog_source_enabled: true
```

Each enabled source becomes a stream you reference in a sink's `inputs`:

- `journald` — carries a `service_name` field (derived from the systemd unit, falling back to the syslog identifier).
- `varlog` — carries a `file` field with the source file's path.

### Shipping logs to Grafana Loki

If [Grafana Loki](grafana-loki.md) runs on the same server, Vector automatically joins Loki's container network when `loki_enabled` is set, so you can ship logs to it directly over the container network.

Add `loki` sinks with the following additional configuration. Use a separate sink per stream, since a sink applies one `labels` block to all its inputs and `journald`/`varlog` carry different fields:

```yaml
vector_sinks_custom:
  loki_journald:
    type: loki
    inputs:
      - journald
    endpoint: "{{ loki_scheme }}://{{ loki_identifier }}:{{ loki_server_http_listen_port }}"
    tenant_id: mash
    encoding:
      codec: text
    labels:
      source: vector
      service_name: "{{ '{{ service_name }}' }}"
      host: "{{ '{{ host }}' }}"

  loki_varlog:
    type: loki
    inputs:
      - varlog
    endpoint: "{{ loki_scheme }}://{{ loki_identifier }}:{{ loki_server_http_listen_port }}"
    tenant_id: mash
    encoding:
      codec: text
    labels:
      source: vector
      filename: "{{ '{{ file }}' }}"
      host: "{{ ansible_hostname | default(inventory_hostname) }}"
```

> [!WARNING]
> A `{{ '{{ field }}' }}` label must reference a field present and non-empty on **every** event the sink receives, otherwise Vector drops the event and logs a warning. Never route `internal_logs` into such a sink: it carries those warnings, so a failed render feeds back into the sink and can pin the CPU. Only label on guaranteed fields (`service_name` on `journald`, `file` on `varlog`); `unit` and `syslog_identifier` are empty for unit-less entries like kernel messages, so they are not safe to label on.

For connecting to a remote Loki instance, set `endpoint` to the public hostname (e.g. `https://mash.example.com/loki`) and adjust authentication as needed.

You can then add Loki as a datasource in Grafana — see [Integrating with a local Loki instance](grafana.md#integrating-with-a-local-loki-instance) on the Grafana documentation page.

### Exposing metrics to Prometheus

To let [Prometheus](prometheus.md) collect Vector's metrics, add a `prometheus_exporter` sink that exposes them on a port:

```yaml
vector_sinks_custom:
  prometheus:
    type: prometheus_exporter
    inputs:
      - internal_metrics
    address: 0.0.0.0:9598
```

Then, on the Prometheus side, add a scrape job targeting Vector over the container network (Prometheus needs to share Vector's network, so this is configured on the Prometheus side):

```yaml
prometheus_config_scrape_configs_additional:
  - job_name: vector
    metrics_path: /metrics
    static_configs:
      - targets:
          - "{{ vector_identifier }}:9598"
```

See [Scraping other exporter services](prometheus.md#scraping-other-exporter-services) on the Prometheus documentation page for more details.

### Exposing the API (optional)

Vector ships a GraphQL API (with a `/health` endpoint and an interactive `/playground`) that powers `vector top` / `vector tap`. It is disabled by default. To enable it and expose it publicly through [Traefik](traefik.md), set a hostname:

```yaml
vector_api_enabled: true
vector_hostname: mash.example.com
vector_path_prefix: /vector
```

>[!WARNING]
> Vector's API has no authentication of its own. Whenever you expose it publicly, protect it with HTTP Basic Authentication:
>
> ```yaml
> vector_container_labels_api_middleware_basic_auth_enabled: true
> # See https://doc.traefik.io/traefik/middlewares/http/basicauth/#users for the format.
> vector_container_labels_api_middleware_basic_auth_users: ""
> ```

## Related services

- [Grafana](grafana.md) — Web-based tool for visualizing your Prometheus metrics (time-series)
- [Grafana Loki](grafana-loki.md) — Log aggregation system that helps collect, store, and analyze logs in a scalable and efficient manner
- [Prometheus](prometheus.md) — Metrics collection and alerting monitoring solution
- [Promtail](promtail.md) — Agent which ships the contents of local logs to a private Grafana Loki instance
- [Telegraf](telegraf.md) — A server agent to help you collect metrics from your stacks, sensors, and systems
