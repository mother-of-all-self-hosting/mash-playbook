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

# Syncthing

The playbook can install and configure [Syncthing](https://syncthing.net/) for you.

Syncthing is a continuous file synchronization program which synchronizes files between two or more computers in real time, safely protected from prying eyes.

See the project's [documentation](https://docs.syncthing.net/) to learn what Syncthing does and why it might be useful to you.

For details about configuring the [Ansible role for Syncthing](https://github.com/mother-of-all-self-hosting/ansible-role-syncthing), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-syncthing/blob/main/docs/configuring-syncthing.md) online
- 📁 `roles/galaxy/syncthing/docs/configuring-syncthing.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# syncthing                                                            #
#                                                                      #
########################################################################

syncthing_enabled: true

syncthing_hostname: mash.example.com
syncthing_path_prefix: /syncthing

########################################################################
#                                                                      #
# /syncthing                                                           #
#                                                                      #
########################################################################
```

### Configuring HTTP Basic authentication

For Syncthing, it is configured to enable the HTTP Basic authentication on Traefik by default. Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-syncthing/blob/main/docs/configuring-syncthing.md#configuring-http-basic-authentication) on the role's documentation for details about how to set it up.

### Integrating with Prometheus (optional)

Syncthing can natively expose metrics to [Prometheus](prometheus.md).

#### Expose metrics internally

If Syncthing and Prometheus do not share a network (like Traefik), you can connect the Syncthing container network to Prometheus by adding the following configuration to your `vars.yml` file:

```yaml
prometheus_container_additional_networks_custom:
  - "{{ syncthing_container_network }}"
```

#### Expose metrics publicly

If Syncthing metrics are not scraped from a local Prometheus instance, you can expose the metrics publicly so that a remote instance can fetch them.

When exposing metrics publicly, you should consider to set up [HTTP Basic Authentication](https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication) **or anyone would be able to read your metrics**.

To expose the metrics publicly, add the following configuration to your `vars.yml` file (adapt to your needs):

```yaml
mash_playbook_metrics_exposure_enabled: true
mash_playbook_metrics_exposure_hostname: mash.example.com
```

It will expose the metrics at `https://mash.example.com/metrics/mash-syncthing`.

To enable the HTTP Basic authentication, add the following configuration to your `vars.yml` file (adapt to your needs):

```yaml
syncthing_container_labels_traefik_metrics_middleware_basic_auth_enabled: true

# See https://doc.traefik.io/traefik/middlewares/http/basicauth/#users for details.
syncthing_container_labels_traefik_metrics_middleware_basic_auth_users: ""
```

## Usage

After running the command for installation, the Syncthing instance becomes available at the URL specified with `syncthing_hostname` and `syncthing_path_prefix`. With the configuration above, the service is hosted at `https://mash.example.com/syncthing`.

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-syncthing/blob/main/docs/configuring-syncthing.md#usage) on the role's documentation for details about the usage, including recommended settings.
