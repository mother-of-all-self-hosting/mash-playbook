# Keycloak

[Keycloak](https://www.keycloak.org/) is an open source identity and access management solution.

> [!WARNING]
> This service is a new addition to the playbook. It may not fully work or be configured in a suboptimal manner.


## Dependencies

This service requires the following other services:

- a [Postgres](postgres.md) database
- a [Traefik](traefik.md) reverse-proxy server


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# keycloak                                                             #
#                                                                      #
########################################################################

keycloak_enabled: true

keycloak_hostname: mash.example.com
keycloak_path_prefix: /keycloak

keycloak_environment_variable_keycloak_admin: your_username_here
# Generating a strong password (e.g. `pwgen -s 64 1`) is recommended
keycloak_environment_variable_keycloak_admin_password: ''

########################################################################
#                                                                      #
# /keycloak                                                            #
#                                                                      #
########################################################################
```

### URL

In the example configuration above, we configure the service to be hosted at `https://mash.example.com/keycloak`.

You can remove the `keycloak_path_prefix` variable definition, to make it default to `/`, so that the service is served at `https://mash.example.com/`.

### Authentication

On first start, the admin user account will be created as defined with the `keycloak_environment_variable_keycloak_admin` and `keycloak_environment_variable_keycloak_admin_password` variables.

On each start after that, Keycloak will attempt to create the user again and report a non-fatal error (Keycloak will continue running).

Subsequent changes to the password will not affect an existing user's password.


## Usage

After installation, you can go to the Keycloak URL, as defined in `keycloak_hostname` and `keycloak_path_prefix` and log in as described in [Authentication](#authentication).

Follow the [Keycloak documentation](https://www.keycloak.org/documentation) or other guides for learning how to use Keycloak.


## Related services

- [OAuth2-Proxy](oauth2-proxy.md) — A reverse proxy and static file server that provides authentication using OpenID Connect Providers (Google, GitHub, [Authentik](authentik.md), [Keycloak](keycloak.md), and others) to SSO-protect services which do not support SSO natively
