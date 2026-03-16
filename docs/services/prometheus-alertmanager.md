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
SPDX-FileCopyrightText: 2024 Thomas Miceli
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Prometheus Alertmanager

The playbook can install and configure [Prometheus Alertmanager](https://github.com/prometheus/alertmanager) for you.

Prometheus Alertmanager is the application which handles alerts sent by client applications such as the Prometheus server.

See the project's [documentation](https://prometheus.io/docs/alerting/latest/alertmanager/) to learn what Prometheus Alertmanager does and why it might be useful to you.

## Dependencies

This service requires the following other services:

- [Prometheus](prometheus.md)
- (optional) [exim-relay](exim-relay.md) mailer
- (optional) [Traefik](traefik.md)

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# prometheus_alertmanager                                              #
#                                                                      #
########################################################################

prometheus_alertmanager_enabled: true

# To expose the metrics publicly, enable and configure the lines below:
# prometheus_alertmanager_hostname: mash.example.com
# prometheus_alertmanager_path_prefix: /metrics/mash-prometheus-alertmanager

# To protect the metrics with HTTP Basic Auth, enable and configure the lines below.
# See: https://doc.traefik.io/traefik/middlewares/http/basicauth/#users
# prometheus_alertmanager_container_labels_metrics_middleware_basic_auth_enabled: true
# prometheus_alertmanager_container_labels_metrics_middleware_basic_auth_users: ""

########################################################################
#                                                                      #
# /prometheus_alertmanager                                             #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the Prometheus Alertmanager instance becomes available.
