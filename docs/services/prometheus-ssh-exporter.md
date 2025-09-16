<!--
SPDX-FileCopyrightText: 2023 Nikita Chernyi
SPDX-FileCopyrightText: 2024 Slavi Pantaleev

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Prometheus SSH Exporter

This playbook can configure [Prometheus SSH Exporter](https://github.com/treydock/ssh_exporter).

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# prometheus_ssh_exporter                                              #
#                                                                      #
########################################################################

prometheus_ssh_exporter_enabled: true

# To expose the metrics publicly, enable and configure the lines below:
# prometheus_ssh_exporter_hostname: mash.example.com
# prometheus_ssh_exporter_path_prefix: /metrics/mash-prometheus-ssh-exporter

# To protect the metrics with HTTP Basic Auth, enable and configure the lines below.
# See: https://doc.traefik.io/traefik/middlewares/http/basicauth/#users
# prometheus_ssh_exporter_container_labels_metrics_middleware_basic_auth_enabled: true
# prometheus_ssh_exporter_container_labels_metrics_middleware_basic_auth_users: ''

########################################################################
#                                                                      #
# /prometheus_ssh_exporter                                             #
#                                                                      #
########################################################################
```

## Usage

After you've installed the ssh exporter, your ssh prober will be available on `mash.example.com/metrics/mash-prometheus-ssh-exporter` with the basic auth credentials you've configured if hostname and path prefix were provided.
