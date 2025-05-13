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
SPDX-FileCopyrightText: 2024 Tiz
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Endlessh

The playbook can install and configure [Endlessh-go](https://github.com/shizunge/endlessh-go) for you.

Endlessh-go is a Golang implementation of [Endlessh](https://github.com/skeeto/endlessh). Endlessh is an [SSH tarpit](https://nullprogram.com/blog/2019/03/22), one of the methods to guard an SSH server from attackers. The program opens a socket and pretends to be an SSH server, but it just ties up SSH clients with false promises indefinitely until the client eventually gives up. It not only blocks blute force attacks to the server but also aims to waste attacker's time and resources.

See the project's [documentation](https://github.com/shizunge/endlessh-go/blob/main/README.md) to learn what Endlessh-go does and why it might be useful to you.

For details about configuring the [Ansible role for Endlessh-go](https://github.com/mother-of-all-self-hosting/ansible-role-endlessh), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-endlessh/blob/main/docs/configuring-endlessh.md) online
- 📁 `roles/galaxy/endlessh/docs/configuring-endlessh.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- (optionally) [Traefik](traefik.md) — a reverse-proxy server for exposing Endlessh publicly
- (optionally) [Prometheus](./prometheus.md) — a database for storing metrics
- (optionally) [Grafana](./grafana.md) — a web UI that can query the Prometheus datasource (connection) and display the logs

## Prerequisites

The role is configured to set up the Endlessh-go instance to listen to the port 22, the standard SSH port, therefore you need to move the port for the real SSH server to another port, so that an Endlessh-go instance can listen to the port 22 and trap attackers' clients into it.

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# endlessh                                                             #
#                                                                      #
########################################################################

endlessh_enabled: true

########################################################################
#                                                                      #
# /endlessh                                                            #
#                                                                      #
########################################################################
```

### Change the port to listen (optional)

By default, the Endlessh-go instance binds to port 22 on all network interfaces. You can change the port by adding the following configuration to your `vars.yml` file:

```yaml
endlessh_container_host_bind_port: YOUR_PORT_NUMBER_HERE
```

## Integrating with Prometheus

Endlessh can natively expose metrics to [Prometheus](./prometheus.md).

### Prerequesites

The bare minimium is to ensure Prometheus can reach Endlessh.

- If Endlessh is on a different host than Prometheus, refer to section [Expose metrics publicly](endlessh.md#)
- If Endlessh is on the same host than Prometheus, refer to section [Ensure Prometheus is on the same container network as Endlessh.](endlessh.md#)

### Ensure Prometheus is on the same container network as Endlessh.

If Endlessh and Prometheus do not share a network (like traefik), you will have to

- Either connect Prometheus container network to Endlessh by editing `prometheus_container_additional_networks_auto`
- Either connect Endlessh container network to Prometheus by editing `endlessh_container_additional_networks_custom`

Exemple:

```yaml
prometheus_container_additional_networks:
  - "{{ endlessh_container_network }}"
```

### Set container extra flag:

The bare minimum is to set container extra flag `-enable_prometheus`

```yaml
endlessh_container_extra_arguments_custom:
  - "-enable_prometheus"
```

Default Endlessh port for metrics is `2112`. It can be changed via container extra flag `-prometheus_port=8085`.

Default Endlessh listening for metrics adress is `0.0.0.0.` (so Endlessh will listing on all adresses). This parrameter can be changed via container extra flag `-prometheus_host=10.10.10.10`.

Default Endlessh entrypoint for metrics is `/metrics`. It can be changed via container extra flag `-prometheus_entry=/endlessh`.

For more container extra flag, refer to the documentation of [Endlessh-go](https://github.com/shizunge/endlessh-go).

### Exposing metrics publicly

Unless you're scraping the Endlessh metrics from a local [Prometheus](prometheus.md) instance, as described in [Integrating with Prometheus](endlessh.md#), you will probably wish to expose the metrics publicly so that a remote Prometheus instance can fetch them. When exposing publicly, it's natural to set up [HTTP Basic Authentication](https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication) **or anyone would be able to read your metrics**.

```yaml
# To expose the metrics publicly, enable and configure the lines below:
endlessh_hostname: mash.example.com
endlessh_path_prefix: /metrics/mash-endlessh

# To protect the metrics with HTTP Basic Auth, enable and configure the lines below.
# See: https://doc.traefik.io/traefik/middlewares/http/basicauth/#users
endlessh_container_labels_metrics_middleware_basic_auth_enabled: true
endlessh_container_labels_metrics_middleware_basic_auth_users: ""
```

## Usage

After [installing](../installing.md), refer to the documentation of [Endlessh-go](https://github.com/shizunge/endlessh-go).
