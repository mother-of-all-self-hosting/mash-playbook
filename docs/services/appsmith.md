# Appsmith

[Appsmith](https://www.appsmith.com/) is an open-source platform that enables developers to build and deploy custom internal tools and applications without writing code.


## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# appsmith                                                             #
#                                                                      #
########################################################################

appsmith_enabled: true

appsmith_hostname: appsmith.example.com

# WARNING: remove this after you create your user account,
# unless you'd like to run a server with public registration enabled.
appsmith_environment_variable_appsmith_signup_disabled: false

########################################################################
#                                                                      #
# /appsmith                                                            #
#                                                                      #
########################################################################
```


### URL

In the example configuration above, we configure the service to be hosted at `https://appsmith.example.com`.

Hosting Appsmith under a subpath (by configuring the `appsmith_path_prefix` variable) does not seem to be possible right now, due to Appsmith limitations..


### Authentication

Public registration can be enabled/disabled using the `appsmith_environment_variable_appsmith_signup_disabled` variable.

We recommend installing with public registration enabled at first, creating your first user account, and then disabling public registration (unless you need it).


## Usage

After installation, you can go to the Appsmith URL, as defined in `appsmith_hostname`.

As mentioned in [Authentication](#authentication) above, you can create the first user from the web interface.

If you'd like to prevent other users from registering, consider disabling public registration by removing the `appsmith_environment_variable_appsmith_signup_disabled` references from your configuration and re-running the playbook (`just install-service appsmith`).
