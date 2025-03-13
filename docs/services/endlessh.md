# Endlessh

[Endlessh-go](https://github.com/shizunge/endlessh-go) is a Golang implementation of [endlessh](https://github.com/skeeto/endlessh), an [SSH tarpit](https://nullprogram.com/blog/2019/03/22). Installing it is powered by the [mother-of-all-self-hosting/ansible-role-endlessh](https://github.com/mother-of-all-self-hosting/ansible-role-endlessh) Ansible role.

## Dependencies

This service requires the following other services:

- (optionally) [Traefik](traefik.md) — a reverse-proxy server for exposing endlessh publicly
- (optionally) [Prometheus](./prometheus.md) — a database for storing metrics
- (optionally) [Grafana](./grafana.md) — a web UI that can query the prometheus datasource (connection) and display the logs

## Prerequisites

An SSH tarpit server needs a port to mimic the SSH server. Port 22 is therefore a good choice.
If you already have your SSH server on this port, you'll have to relocate it.
I recommend using a random port for the ssh server (eg: 14567) and port 22 for the tarpit.

## Installing

To configure and install endlessh on your own server(s), you should use a playbook like [Mother of all self-hosting](https://github.com/mother-of-all-self-hosting/mash-playbook) or write your own.

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

By default, endlessh will try to bind to port 22 on all network interfaces.
You could change this behavior by setting `endlessh_container_host_bind_port`:

```yaml
endlessh_container_host_bind_port: 22
```

See the full list of options in the [default/main.yml](default/main.yml) file

## Integrating with Prometheus

Endlessh can natively expose metrics to [Prometheus](./prometheus.md).

### Prerequesites

The bare minimium is to ensure Prometheus can reach endlessh.

- If Endlessh is on a different host than Prometheus, refer to section [Expose metrics publicly](endlessh.md#)
- If Endlessh is on the same host than prometheus, refer to section [Ensure Prometheus is on the same container network as endlessh.](endlessh.md#)

### Ensure Prometheus is on the same container network as endlessh.

If endlessh and prometheus do not share a network (like traefik), you will have to

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

Default endlessh port for metrics is `2112`. It can be changed via container extra flag `-prometheus_port=8085`.

Default endlessh listening for metrics adress is `0.0.0.0.` (so endlessh will listing on all adresses). This parrameter can be changed via container extra flag `-prometheus_host=10.10.10.10`.

Default endlessh entrypoint for metrics is `/metrics`. It can be changed via container extra flag `-prometheus_entry=/endlessh`.

For more container extra flag, refer to the documentation of [endlessh-go](https://github.com/shizunge/endlessh-go).

### Exposing metrics publicly

Unless you're scraping the endlessh metrics from a local [Prometheus](prometheus.md) instance, as described in [Integrating with Prometheus](endlessh.md#), you will probably wish to expose the metrics publicly so that a remote Prometheus instance can fetch them. When exposing publicly, it's natural to set up [HTTP Basic Authentication](https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication) **or anyone would be able to read your metrics**.

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

After [installing](../installing.md), refer to the documentation of [endlessh-go](https://github.com/shizunge/endlessh-go).
