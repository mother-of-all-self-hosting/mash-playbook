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
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Static Web Server

The playbook can install and configure [Static Web Server](https://static-web-server.net/) for you.

Static Web Server is a web server for static file-serving.

See the project's [documentation](https://static-web-server.net/v3/) to learn what Static Web Server does and why it might be useful to you.

For details about configuring the [Ansible role for Static Web Server](https://github.com/mother-of-all-self-hosting/ansible-role-static-web-server), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-static-web-server/blob/main/docs/configuring-static-web-server.md) online
- 📁 `roles/galaxy/static_web_server/docs/configuring-static-web-server.md` locally, if you have [fetched the Ansible roles](../../docs/installing.md)

>[!NOTE]
> This role is configured to install [v3](https://static-web-server.net/v3/) by default.

## Dependencies

This service requires the following other services:

- [Traefik](../traefik/README.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../../docs/installing.md) process:

```yaml
########################################################################
#                                                                      #
# static_web_server                                                    #
#                                                                      #
########################################################################

static_web_server_enabled: true

static_web_server_hostname: static-web-server.example.com

########################################################################
#                                                                      #
# /static_web_server                                                   #
#                                                                      #
########################################################################
```

### Mounting the root directory

By default, Static Web Server serves the example page bundled with its container image. To serve your own files, mount a directory from the host as the root directory by adding the following configuration to your `vars.yml` file (adapt to your needs):

```yaml
static_web_server_container_additional_volumes_custom:
  - type: bind
    src: /path/on/the/host
    dst: "{{ static_web_server_environment_variables_server_root }}"
    options: readonly
```

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-static-web-server/blob/main/docs/configuring-static-web-server.md#mounting-the-root-directory) on the role's documentation for details.

### Integrating with Prometheus (optional)

Static Web Server can natively expose metrics to [Prometheus](../prometheus/README.md).

#### Expose metrics internally

If Static Web Server and Prometheus do not share a network (like Traefik), you can connect the Static Web Server container network to Prometheus by adding the following configuration to your `vars.yml` file:

```yaml
prometheus_container_additional_networks_custom:
  - "{{ static_web_server_container_network }}"
```

#### Expose metrics publicly

If Static Web Server metrics are not scraped from a local Prometheus instance, you can expose the metrics publicly so that a remote instance can fetch them.

When exposing metrics publicly, you should consider to set up [HTTP Basic Authentication](https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication) **or anyone would be able to read your metrics**.

To expose the metrics publicly, add the following configuration to your `vars.yml` file (adapt to your needs):

```yaml
mash_playbook_metrics_exposure_enabled: true
mash_playbook_metrics_exposure_hostname: mash.example.com
```

It will expose the metrics at `https://mash.example.com/metrics/mash-static-web-server`.

To enable the HTTP Basic authentication, add the following configuration to your `vars.yml` file (adapt to your needs):

```yaml
static_web_server_container_labels_traefik_metrics_middleware_basic_auth_enabled: true

# See https://doc.traefik.io/traefik/middlewares/http/basicauth/#users for details.
static_web_server_container_labels_traefik_metrics_middleware_basic_auth_users: ""
```

## Usage

After running the command for installation, the Static Web Server instance becomes available at the URL specified with `static_web_server_hostname`. With the configuration above, the service is hosted at `https://static-web-server.example.com`.

## Troubleshooting

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-static-web-server/blob/main/docs/configuring-static-web-server.md#troubleshooting) on the role's documentation for details.

## Related services

- [Nginx](../nginx/README.md) — Web server, reverse proxy, load balancer and HTTP cache
