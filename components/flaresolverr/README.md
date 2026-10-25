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
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 Thomas Miceli
SPDX-FileCopyrightText: 2024 Tiz
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara
SPDX-FileCopyrightText: 2025 MASH project contributors
SPDX-FileCopyrightText: 2025 sudo-Tiz

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# FlareSolverr

The playbook can install and configure [FlareSolverr](https://github.com/FlareSolverr/FlareSolverr) for you.

FlareSolverr is an open-source proxy server to bypass Cloudflare protection.

See the project's [documentation](https://github.com/FlareSolverr/FlareSolverr/blob/master/README.md) to learn what FlareSolverr does and why it might be useful to you.

For details about configuring the [Ansible role for FlareSolverr](https://github.com/mother-of-all-self-hosting/ansible-role-flaresolverr), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-flaresolverr/blob/main/docs/configuring-flaresolverr.md) online
- 📁 `roles/galaxy/flaresolverr/docs/configuring-flaresolverr.md` locally, if you have [fetched the Ansible roles](../../docs/installing.md)

## Dependencies

This service requires the following other services:

- (optional) [Traefik](../traefik/README.md) — Reverse-proxy server for exposing FlareSolverr publicly

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../../docs/installing.md) process:

```yaml
########################################################################
#                                                                      #
# flaresolverr                                                         #
#                                                                      #
########################################################################

flaresolverr_enabled: true

########################################################################
#                                                                      #
# /flaresolverr                                                        #
#                                                                      #
########################################################################
```

### Expose the instance publicly (optional)

By default, the FlareSolverr instance is not exposed externally, as it is mainly intended to be used in the internal network.

To expose it publicly, add the following configuration to your `vars.yml` file (adapt to your needs):

```yaml
# The hostname at which FlareSolverr is served.
flaresolverr_hostname: "flaresolverr.example.com"
```

### Integrating with Prometheus (optional)

FlareSolverr can natively expose metrics to [Prometheus](../prometheus/README.md).

#### Expose metrics internally

If FlareSolverr and Prometheus do not share a network (like Traefik), you can connect the FlareSolverr container network to Prometheus by adding the following configuration to your `vars.yml` file:

```yaml
prometheus_container_additional_networks_custom:
  - "{{ flaresolverr_container_network }}"
```

#### Expose metrics publicly

If FlareSolverr metrics are not scraped from a local Prometheus instance, you can expose the metrics publicly so that a remote instance can fetch them.

When exposing metrics publicly, you should consider to set up [HTTP Basic Authentication](https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication) **or anyone would be able to read your metrics**.

To expose the metrics publicly, add the following configuration to your `vars.yml` file (adapt to your needs):

```yaml
mash_playbook_metrics_exposure_enabled: true
mash_playbook_metrics_exposure_hostname: mash.example.com
```

It will expose the metrics at `https://mash.example.com/metrics/mash-flaresolverr`.

To enable the HTTP Basic authentication, add the following configuration to your `vars.yml` file (adapt to your needs):

```yaml
flaresolverr_container_labels_traefik_metrics_middleware_basic_auth_enabled: true

# See https://doc.traefik.io/traefik/middlewares/http/basicauth/#users for details.
flaresolverr_container_labels_traefik_metrics_middleware_basic_auth_users: ""
```

## Usage

After running the command for installation, the FlareSolverr instance becomes available internally to other services on the same network. If the service is exposed to the internet, it becomes available at the URL specified with `flaresolverr_hostname`. With the configuration above, the service is hosted at `https://flaresolverr.example.com`.

## Troubleshooting

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-flaresolverr/blob/main/docs/configuring-flaresolverr.md#troubleshooting) on the role's documentation for details.
