<!--
SPDX-FileCopyrightText: 2020 - 2024 MDAD project contributors
SPDX-FileCopyrightText: 2020 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2020 Aaron Raimist
SPDX-FileCopyrightText: 2020 Chris van Dijk
SPDX-FileCopyrightText: 2020 Dominik Zajac
SPDX-FileCopyrightText: 2020 Mickaël Cornière
SPDX-FileCopyrightText: 2022 François Darveau
SPDX-FileCopyrightText: 2022 Julian Foad
SPDX-FileCopyrightText: 2022 Warren Bailey
SPDX-FileCopyrightText: 2023 Antonis Christofides
SPDX-FileCopyrightText: 2023 Felix Stupp
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Grafana Loki

The playbook can install and configure [Grafana Loki](https://grafana.com/docs/loki/latest/) for you.

Loki is a log aggregation system designed to store and query logs from all your applications and infrastructure.

See the project's [documentation](https://grafana.com/docs/loki/latest/) to learn what Loki does and why it might be useful to you.

For details about configuring the [Ansible role for Loki](https://github.com/mother-of-all-self-hosting/ansible-role-loki), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-loki/blob/main/docs/configuring-loki.md) online
- 📁 `roles/galaxy/loki/docs/configuring-loki.md` locally, if you have [fetched the Ansible roles](../installing.md)

>[!NOTE]
> As Loki is just a log storage system, you would need at least two other components in order to make use of it:
> - an agent such as Promtail to send logs to Loki
> - a system such as Grafana to read the logs out of Loki and display them nicely

## Dependencies

This service requires the following other services:

- (optional) [Traefik](traefik.md) — a reverse-proxy server for exposing Loki publicly
- (optional; recommended) [Promtail](./promtail.md) — an agent which ships the contents of local logs to a private Grafana Loki instance
- (optional; recommended) [Grafana](./grafana.md) — a web-based tool for visualizing your Promtail logs (stored in Grafana Loki or elsewhere)

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# loki                                                                 #
#                                                                      #
########################################################################

loki_enabled: true

########################################################################
#                                                                      #
# /loki                                                                #
#                                                                      #
########################################################################
```

### Exposing the web interface

By setting a hostname with `loki_hostname` and optionally a path prefix with `loki_path_prefix`, you can expose Loki publicly. You may wish to do this, if you'd like to be able to push logs from remote agents (e.g. Promtail installed on remote machines, etc.) and query logs from remote systems (e.g. Grafana installed elsewhere).

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-loki/blob/main/docs/configuring-loki.md#set-the-hostname-to-expose-the-web-interface-optional) on the role's documentation for details about configuring it.

## Usage

Refer to the [official documentation](https://grafana.com/docs/loki/latest/reference/api/#post-lokiapiv1push) for details about how to send logs throught Loki's API without an agent.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-loki/blob/main/docs/configuring-loki.md#troubleshooting) on the role's documentation for details.
