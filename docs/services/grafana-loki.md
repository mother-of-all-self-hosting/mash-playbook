# Grafana Loki

[Grafana Loki](https://grafana.com/docs/loki/latest/) is a set of components that can be composed into a fully featured logging stack. Installing it is powered by the [mother-of-all-self-hosting/ansible-role-loki](https://github.com/mother-of-all-self-hosting/ansible-role-loki) Ansible role.

Loki is just a log storage system. In order to make use of it, you'd need at least 2 other components

- some agent (like [Promtail](./promtail.md)) to send logs to Loki
- some system (like [Grafana](./grafana.md)) to read the logs out of Loki and display them nicely


## Dependencies

This service requires the following other services:

- (optionally) [Traefik](traefik.md) — a reverse-proxy server for exposing Loki publicly
- (optionally) [Promtail](./promtail.md) — an agent that can send logs to Loki
- (optionally) [Grafana](./grafana.md) — a web UI that can query the Loki datasource (connection) and display the logs


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

By setting a hostname and optionally a path prefix, you can expose Loki publicly. You may wish to do this, if you'd like to be able to:

- push logs from remote agents (e.g. Promtail installed on remote machines, etc.)
- query logs from remote systems (e.g. Grafana installed elsewhere)

When exposing publicly, it's natural to set up [HTTP Basic Authentication](https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication) **or anyone would be able to read your logs or push new ones**.

```yaml
loki_hostname: mash.example.com
loki_path_prefix: /loki

# If you are sure you wish to run without Basic Auth enabled,
# explicitly set the variable below to false.
loki_container_labels_middleware_basic_auth_enabled: true
# Use `htpasswd -nb USERNAME PASSSWORD` to generate the users below.
loki_container_labels_middleware_basic_auth_users: ''
```


## Usage

After [installing](../installing.md), refer to the [official documentation](https://grafana.com/docs/loki/latest/reference/api/#post-lokiapiv1push) to send logs to loki's API without an agent or set up one or more instances of the [Promtail](./promtail.md) agent.


## Recommended other services

- [Grafana](grafana.md) — a web-based tool for visualizing your Promtail logs (stored in [Grafana Loki](grafana-loki.md) or elsewhere)
- [Promtail](promtail.md) — an agent which ships the contents of local logs to a private [Grafana Loki](grafana-loki.md) instance
