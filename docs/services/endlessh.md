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

>[!NOTE]
> None of them are required unless you will expose metrics to a Prometheus server.

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

## Usage

After installation, the instance starts running on the server and listens to the specified port (port 22 by default).

You can customize how it works with the `endlessh_container_extra_arguments_custom` variable. See [this section](https://github.com/shizunge/endlessh-go/blob/main/README.md#usage) of the documentation for available arguments.

### Integrating with Prometheus (optional)

Endlessh can natively expose metrics to [Prometheus](prometheus.md).

As the metrics is off by default, you can turn it via the CLI argument `-enable_prometheus` as below:

```yaml
endlessh_container_extra_arguments_custom:
  - "-enable_prometheus"
```

You can set other arguments to customize how metrics are exposed, such as `-prometheus_port`, `-prometheus_host`, `-prometheus_entry`, etc. See [this section](https://github.com/shizunge/endlessh-go/blob/main/README.md#usage) of the documentation for details.

After settings arguments, you need to expose metrics internally or externally.

- If Endlessh is on the same host as Prometheus, refer to this section: [Expose metrics internally](#expose-metrics-internally)
- If Endlessh is on a different host than Prometheus, refer to this section: [Expose metrics publicly](#expose-metrics-publicly)

#### Expose metrics internally

If Endlessh and Prometheus do not share a network (like Traefik), you will have to either:

- Connect the Prometheus container network to Endlessh by adjusting `prometheus_container_additional_networks_auto`
- Connect the Endlessh container network to Prometheus by adjusting `endlessh_container_additional_networks_custom`

Here is an example configuration to be added to your `vars.yml` file:

```yaml
prometheus_container_additional_networks:
  - "{{ endlessh_container_network }}"
```

#### Expose metrics publicly

If Endlessh metrics are not scraped from a local Prometheus instance, you can expose the metrics publicly so that a remote instance can fetch them.

When exposing metrics publicly, you should consider to set up [HTTP Basic Authentication](https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication) **or anyone would be able to read your metrics**.

To expose the metrics publicly, add the following configuration to your `vars.yml` file (adapt to your needs):

```yaml
# The hostname at which Endlessh is served.
endlessh_hostname: ''

# The path at which Endlessh is exposed.
endlessh_path_prefix: /metrics/mash-endlessh
```

To enable HTTP Basic Auth, add the following configuration to your `vars.yml` file (adapt to your needs):

```yaml
endlessh_container_labels_metrics_middleware_basic_auth_enabled: true

# See https://doc.traefik.io/traefik/middlewares/http/basicauth/#users for details.
endlessh_container_labels_metrics_middleware_basic_auth_users: ""
```
