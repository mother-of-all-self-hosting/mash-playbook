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

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# APISIX

The playbook can install and configure [APISIX](https://apisix.apache.org/docs/apisix/getting-started/README/) for you.

APISIX is an [API Gateway](https://apisix.apache.org/docs/apisix/terminology/api-gateway/) and Ingress Controller.

For details about configuring the [Ansible role for APISIX](https://github.com/mother-of-all-self-hosting/ansible-role-apisix), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-apisix/blob/main/docs/configuring-apisix.md) online
- 📁 `roles/galaxy/apisix/docs/configuring-apisix.md` locally, if you have [fetched the Ansible roles](../../docs/installing.md)

## Dependencies

This service requires the following other services:

- [etcd](../etcd/README.md) key-value store
- [Traefik](../traefik/README.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../../docs/installing.md) process:

```yaml
########################################################################
#                                                                      #
# apisix                                                               #
#                                                                      #
########################################################################

apisix_enabled: true

# Configure the hostname and path at which the API would be exposed
apisix_hostname: api.example.com
apisix_path_prefix: /api

########################################################################
#                                                                      #
# /apisix                                                              #
#                                                                      #
########################################################################
```

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-apisix/blob/main/docs/configuring-apisix.md#adjusting-the-playbook-configuration) on the role's documentation for other settings such as the one for exposing Admin API (with recommended configurations to reduce attack surfaces).

### Integrating with Prometheus (optional)

APISIX can natively expose metrics to [Prometheus](../prometheus/README.md).

#### Expose metrics internally

If APISIX and Prometheus do not share a network (like Traefik), you can connect the APISIX container network to Prometheus by adding the following configuration to your `vars.yml` file:

```yaml
prometheus_container_additional_networks_custom:
  - "{{ apisix_container_network }}"
```

#### Expose metrics publicly

If APISIX metrics are not scraped from a local Prometheus instance, you can expose the metrics publicly so that a remote instance can fetch them.

When exposing metrics publicly, you should consider to set up [HTTP Basic Authentication](https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication) **or anyone would be able to read your metrics**.

To expose the metrics publicly, add the following configuration to your `vars.yml` file (adapt to your needs):

```yaml
mash_playbook_metrics_exposure_enabled: true
mash_playbook_metrics_exposure_hostname: mash.example.com
```

It will expose the metrics at `https://mash.example.com/metrics/mash-apisix`.

To enable the HTTP Basic authentication, add the following configuration to your `vars.yml` file (adapt to your needs):

```yaml
apisix_container_labels_traefik_metrics_middleware_basic_auth_enabled: true

# See https://doc.traefik.io/traefik/middlewares/http/basicauth/#users for details.
apisix_container_labels_traefik_metrics_middleware_basic_auth_users: ""
```

## Usage

After running the command for installation, the APISIX instance becomes available. Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-apisix/blob/main/docs/configuring-apisix.md#usage) on the role's documentation for details about the usage.

## Related services

- [etcd](../etcd/README.md) — Distributed key-value store, where APISIX keeps its configuration
- [Traefik](../traefik/README.md) — Reverse-proxy server which fronts APISIX's listeners
