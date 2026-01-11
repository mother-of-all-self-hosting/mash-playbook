# Cryptpad

**Warning: Still in development, not usable right now**

The playbook can install and configure [Cryptpad](https://cryptpad.fr), an end-to-end encrypted and open-source collaboration suite, for you.

The [Ansible role for Cryptpad](https://github.com/mother-of-all-self-hosting/ansible-role-cryptpad) is developed and maintained by the MASH project. For details about configuring Cryptpad, you can check them via:

- 🌐 [the role's documentation at the MASH project](https://github.com/mother-of-all-self-hosting/ansible-role-cryptpad/blob/main/defaults/main.yml) online
- 📁 `roles/galaxy/cryptpad/docs/configuring-cryptpad.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# cryptpad                                                             #
#                                                                      #
########################################################################

cryptpad_enabled: true

cryptpad_main_hostname: cryptpad.example.com
cryptpad_sandbox_hostname: sandbox.example.org
cryptpad_admin_email: admin@example.org

########################################################################
#                                                                      #
# /cryptpad                                                            #
#                                                                      #
########################################################################
```

As the most of the necessary settings for the role have been taken care of by the playbook, you can enable Cryptpad on your server with this minimum configuration.


## Usage

By default, the Cryptpad UI should be available at `cryptpad_main_hostname`.

