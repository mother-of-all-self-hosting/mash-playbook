# GoToSocial

[GoToSocial](https://gotosocial.org/) is a self-hosted [ActivityPub](https://activitypub.rocks/) social network server, that this playbook can install, powered by the [moan0s/role-gotosocial](https://github.com/moan0s/role-gotosocial) Ansible role.

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# gotosocial                                                           #
#                                                                      #
########################################################################

gotosocial_enabled: true
gotosocial_hostname: 'social.example.org'

########################################################################
#                                                                      #
# /gotosocial                                                          #
#                                                                      #
########################################################################
```

After installation, you can use `just run-tags firezone-create-or-reset-admin` any time to:
- create the configured admin account
- or, reset the password to the current password configured in `vars.yml`

### Networking

By default, the following ports will be exposed by the container on **all network interfaces**:

- `51820` over **UDP**, controlled by `firezone_wireguard_bind_port` - used for [Wireguard](https://en.wikipedia.org/wiki/WireGuard) connections

Docker automatically opens these ports in the server's firewall, so you **likely don't need to do anything**. If you use another firewall in front of the server, you may need to adjust it.

### Usage

After [installing](../installing.md), you can login at the URL specified in `firezone_hostname`, with the credentials set in `firezone_default_admin_email` and `firezone_default_admin_password`.

Refer to the [official documentation](https://www.firezone.dev/docs/user-guides/add-devices/) to figure out how to add devices, etc.
