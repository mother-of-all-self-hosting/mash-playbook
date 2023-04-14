# Lago

[Lago](https://www.getlago.com/) is an open-source metering and usage-based billing solution.


## Dependencies

This service requires the following other services:

- a [Postgres](postgres.md) database
- a [Redis](redis.md) data-store, installation details [below](#redis)
- a [Traefik](traefik.md) reverse-proxy server


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# lago                                                                 #
#                                                                      #
########################################################################

lago_enabled: true

lago_hostname: lago.example.com

# Generate this using `openssl genrsa 2048 | base64 --wrap=0`
lago_api_environment_variable_lago_rsa_private_key: ''

# WARNING: remove this after you create your user account,
# unless you'd like to run a server with public registration enabled.
lago_front_environment_variable_lago_disable_signup: false

# Redis configuration, as described below

########################################################################
#                                                                      #
# /lago                                                                #
#                                                                      #
########################################################################
```

### URL

In the example configuration above, we configure the service to be hosted at `https://lago.example.com`.

Hosting Lago under a subpath (by configuring the `lago_path_prefix` variable) does not seem to be possible right now, due to Lago limitations.

Our setup hosts the Lago frontend at the root path (`/`) and the Lago API at the `/api` prefix.
This seems to work well, except for [PDF invoices failing due to a Lago bug](https://github.com/getlago/lago/issues/221).

### Authentication

Public registration can be enabled/disabled using the `lago_front_environment_variable_lago_disable_signup` variable.

We recommend installing with public registration enabled at first, creating your first user account, and then disabling public registration (unless you need it).

It should be noted that disabling public signup with this variable merely disables the Sign-Up page in the web interface, but [does not actually disable signups due to a Lago bug](https://github.com/getlago/lago/issues/220).

## Usage

After installation, you can go to the Lago URL, as defined in `lago_hostname`.

As mentioned in [Authentication](#authentication) above, you can create the first user from the web interface.

If you'd like to prevent other users from registering, consider disabling public registration by removing the `lago_front_environment_variable_lago_disable_signup` references from your configuration and re-running the playbook (`just install-service lago`).
