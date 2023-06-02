# Infisical

[Infisical](https://infisical.com/) is an open-source end-to-end encrypted platform for securely managing secrets and configs across your team, devices, and infrastructure.


## Dependencies

This service requires the following other services:

- a [MongoDB](mongodb.md) document-oriented database server
- a [Traefik](traefik.md) reverse-proxy server


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# infisical                                                            #
#                                                                      #
########################################################################

infisical_enabled: true

infisical_hostname: infisical.example.com

# Generate this with: `openssl rand -hex 16`
infisical_backend_environment_variable_encryption_key: ''

# WARNING: uncomment this after creating your first user account,
# unless you'd like to run a server with public registration enabled.
# infisical_backend_environment_variable_invite_only_signup: true

########################################################################
#                                                                      #
# /infisical                                                           #
#                                                                      #
########################################################################
```


### URL

In the example configuration above, we configure the service to be hosted at `https://infisical.example.com`.

Hosting Infisical under a subpath (by configuring the `infisical_path_prefix` variable) does not seem to be possible right now, due to Infisical limitations.


### Authentication

Public registration can be enabled/disabled using the `infisical_backend_environment_variable_invite_only_signup` variable.

We recommend installing with public registration enabled at first (which is the default value for this variable), creating your first user account, and then disabling public registration by explicitly setting `infisical_backend_environment_variable_invite_only_signup` to `true`.


## Usage

After installation, you can go to the Infisical URL, as defined in `infisical_hostname`.

As mentioned in [Authentication](#authentication) above, you can create the first user from the web interface.

If you'd like to prevent other users from registering, consider disabling public registration by explicitly setting `infisical_backend_environment_variable_invite_only_signup` variable to `true` in your configuration and re-running the playbook (`just install-service infisical`).
