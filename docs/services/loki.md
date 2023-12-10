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

loki_hostname: loki.example.com



########################################################################
#                                                                      #
# /loki                                                                #
#                                                                      #
########################################################################
```


## Usage

After [installing](../installing.md), ....
