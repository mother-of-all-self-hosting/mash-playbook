# Endlessh

[Endlessh-go](https://github.com/shizunge/endlessh-go) is a A golang implementation of endlessh, a ssh trapit. Installing it is powered by the [mother-of-all-self-hosting/ansible-role-endlessh](https://github.com/mother-of-all-self-hosting/ansible-role-endlessh) Ansible role.

## Dependencies

This service requires the following other services:

- (optionally) [Traefik](traefik.md) - a reverse-proxy server for exposing endlessh publicly
- (optionally) [Prometheus](./prometheus.md) - a database for storing metrics
- (optionally) [Grafana](./grafana.md) - a web UI that can query the prometheus datasource (connection) and display the logs

## Installing

To configure and install endlessh on your own server(s), you should use a playbook like [Mother of all self-hosting](https://github.com/mother-of-all-self-hosting/mash-playbook) or write your own.

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# endlessh                                                                 #
#                                                                      #
########################################################################

endlessh_enabled: true

########################################################################
#                                                                      #
# /endlessh                                                                #
#                                                                      #
########################################################################
```
See the full list of options in the [default/main.yml](default/main.yml) file

## Exporting Prometheus metrics

Default port is 2112

Default entrypoint is /metrics

use environment variable 
```yaml
endlessh_container_extra_arguments_custom:
  - "-enable_prometheus"
```

### Exposing the web interface

By setting a hostname and optionally a path prefix, you can expose endlessh publicly.

When exposing publicly, it's natural to set up [HTTP Basic Authentication](https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication) **or anyone would be able to read your logs or push new ones**.

```yaml
endlessh_hostname: mash.example.com
endlessh_path_prefix: /endlessh

# If you are sure you wish to run without Basic Auth enabled,
# explicitly set the variable below to false.
endlessh_container_labels_middleware_basic_auth_enabled: true
# Use `htpasswd -nb USERNAME PASSSWORD` to generate the users below.
endlessh_container_labels_middleware_basic_auth_users: ''
```


## Usage

After [installing](../installing.md), refer to the documentation of [endlessh-go](https://github.com/shizunge/endlessh-go).
