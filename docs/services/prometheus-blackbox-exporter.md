<!--
SPDX-FileCopyrightText: 2023 Nikita Chernyi
SPDX-FileCopyrightText: 2023 - 2024 Slavi Pantaleev

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Prometheus Blackbox Exporter

This playbook can configure [Prometheus Blackbox Exporter](https://github.com/prometheus/blackbox_exporter).

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# prometheus_blackbox_exporter                                         #
#                                                                      #
########################################################################

prometheus_blackbox_exporter_enabled: true

# To expose the metrics publicly, enable and configure the lines below:
# prometheus_blackbox_exporter_hostname: mash.example.com
# prometheus_blackbox_exporter_path_prefix: /metrics/mash-prometheus-blackbox-exporter

# To protect the metrics with HTTP Basic Auth, enable and configure the lines below.
# See: https://doc.traefik.io/traefik/middlewares/http/basicauth/#users
# prometheus_blackbox_exporter_container_labels_metrics_middleware_basic_auth_enabled: true
# prometheus_blackbox_exporter_container_labels_metrics_middleware_basic_auth_users: ''

########################################################################
#                                                                      #
# /prometheus_blackbox_exporter                                        #
#                                                                      #
########################################################################
```

## Usage

After you've installed the blackbox exporter, your blackbox prober will be available on `mash.example.com/metrics/mash-prometheus-blackbox-exporter` with the basic auth credentials you've configured if hostname and path prefix where provided
