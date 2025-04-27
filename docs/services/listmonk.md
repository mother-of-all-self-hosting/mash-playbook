# Listmonk

[Listmonk](https://listmonk.app/) is a self-hosted newsletter and mailing list manager, that this playbook can install, powered by the [mother-of-all-self-hosting/ansible-role-listmonk](https://github.com/mother-of-all-self-hosting/ansible-role-listmonk) Ansible role.

## Dependencies

This service requires the following other services:

- a [Postgres](postgres.md) database
- a [Traefik](traefik.md) reverse-proxy server


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# listmonk                                                             #
#                                                                      #
########################################################################

listmonk_enabled: true
listmonk_hostname: 'newsletter.example.org'

########################################################################
#                                                                      #
# /listmonk                                                            #
#                                                                      #
########################################################################
```

## Usage

After [installing](../installing.md), you can visit the domain you specified in `listmonk_hostname` to create an admin user and get started.
*
