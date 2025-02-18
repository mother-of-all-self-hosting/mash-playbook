# ihatemoney

[ihatemoney](https://github.com/spiral-project/ihatemoney) is a self-hosted shared budget manager, that this playbook can install, powered by the [ansible-role-ihatemoney](https://github.com/IUCCA/ansible-role-ihatemoney) Ansible role.


## Dependencies

This service requires the following other services:
- a [Postgres](postgres.md) database
- a [Traefik](traefik.md) reverse-proxy server


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# ihatemoney                                                           #
#                                                                      #
########################################################################

ihatemoney_enabled: true

# To enable the Admin dashboard, first generate a hashed password with:
# docker run -it --rm --entrypoint ihatemoney ihatemoney/ihatemoney generate_password_hash
#ihatemoney_admin_password:
ihatemoney_environment_variable_public: false
ihatemoney_hostname: mash.example.com
ihatemoney_path_prefix: /ihatemoney

########################################################################
#                                                                      #
# /ihatemoney                                                          #
#                                                                      #
########################################################################
```

### URL

In the example configuration above, we configure the service to be hosted at `https://mash.example.com/ihatemoney`.

## Usage

After installation, you can go to the ihatemoney URL, as defined in `ihatemoney_hostname` and `ihatemoney_path_prefix`.
