# n.eko

[n.eko](https://neko.m1k1o.net/) is a self-hosted virtual browser, that this playbook can install, powered by the [mother-of-all-self-hosting/ansible-role-neko](https://github.com/mother-of-all-self-hosting/ansible-role-neko) Ansible role.

> [!WARNING]
> The neko service will run in a container with root privileges, no dropped capabilities and will be able to write inside the container. This seems to be a neccessary deviation from the usual security standards in this playbook.

## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# neko                                                                 #
#                                                                      #
########################################################################

neko_enabled: true
neko_hostname: 'neko.example.org'
neko_password: 'SECURE_PASSWORD'
neko_password_admin: 'SUPER_SECURE_PASSWORD'

########################################################################
#                                                                      #
# /neko                                                                #
#                                                                      #
########################################################################
```

## Advanced configuration

There are different flavours of neko and while `firefox` is the default, you can try others by setting

```yaml
neko_version: "kde"
```

All available tags can be found on [Dockerhub](https://hub.docker.com/r/m1k1o/neko/tags)

