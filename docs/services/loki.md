# Loki

[Loki](https://grafana.com/docs/loki/latest/) Grafana Loki is a set of components that can be composed into a fully featured logging stack. Installing it is powered by the [mother-of-all-self-hosting/ansible-role-loki](https://github.com/mother-of-all-self-hosting/ansible-role-loki) Ansible role.

## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server

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

By setting a hostname you will expose loki on this domain.
Usually you should also set up basic_auth in this case, otherwise everyone will be able to access your metrics

```yaml
loki_hostname: loki.example.org

# Uncommenting the following lines allows you to configure basic auth
# loki_basic_auth_enabled: true
# loki_basic_auth_username: ''
# loki_basic_auth_password: ''
```

## Usage

After [installing](../installing.md), refer to the [official documentation](https://grafana.com/docs/loki/latest/reference/api/#post-lokiapiv1push) to send logs throught loki's API withtout agent.
Promtail agent is comming soon
