<!--
SPDX-FileCopyrightText: 2020 Aaron Raimist
SPDX-FileCopyrightText: 2020 Chris van Dijk
SPDX-FileCopyrightText: 2020 Dominik Zajac
SPDX-FileCopyrightText: 2020 Mickaël Cornière
SPDX-FileCopyrightText: 2020-2024 MDAD project contributors
SPDX-FileCopyrightText: 2020-2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2022 François Darveau
SPDX-FileCopyrightText: 2022 Julian Foad
SPDX-FileCopyrightText: 2022 Warren Bailey
SPDX-FileCopyrightText: 2023 Antonis Christofides
SPDX-FileCopyrightText: 2023 Felix Stupp
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 Nikita Chernyi
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 Tiz
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Prometheus SSH Exporter

The playbook can install and configure [Prometheus SSH Exporter](https://github.com/treydock/ssh_exporter) for you.

Prometheus SSH Exporter is a Prometheus exporter which attempts to make an SSH connection to a remote system and optionally run a command and test output.

See the project's [documentation](https://github.com/treydock/ssh_exporter/blob/master/README.md) to learn what Prometheus SSH Exporter does and why it might be useful to you.

## Dependencies

This service requires the following other services:

- [Prometheus](prometheus.md) — database for storing metrics
- (optional) [Grafana](grafana.md) — web UI that can query the Prometheus datasource (connection) and display the logs
- (optional) [Traefik](traefik.md) — reverse-proxy server for exposing Prometheus SSH Exporter

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
