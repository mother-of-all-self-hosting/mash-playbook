<!--
SPDX-FileCopyrightText: 2023 Slavi Pantaleev
SPDX-FileCopyrightText: 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Keycloak

[Keycloak](https://www.keycloak.org/) is an open source identity and access management solution.

Follow the [Keycloak documentation](https://www.keycloak.org/documentation) or other guides for learning how to use Keycloak.

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

keycloak_environment_variable_kc_bootstrap_admin_username: your_username_here
# Generating a strong password (e.g. `pwgen -s 64 1`) is recommended
keycloak_environment_variable_kc_bootstrap_admin_password: ''

########################################################################
#                                                                      #
# /keycloak                                                            #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the Keycloak instance becomes available at the URL specified with `keycloak_hostname` and `keycloak_path_prefix`. With the configuration above, the service is hosted at `https://mash.example.com/keycloak`.

To get started, open the URL with a web browser, and log in with the admin user account. The account is created on the first start, as defined with the `keycloak_environment_variable_kc_bootstrap_admin_username` and `keycloak_environment_variable_kc_bootstrap_admin_password` variables.

On each start after that, Keycloak will attempt to create the user again and report a non-fatal error (Keycloak will continue running).

>[!NOTE]
> Subsequent changes to the password will not affect an existing user's password.

## Related services

- [authentik](authentik.md) — Open-source identity provider focused on flexibility and versatility
- [Authelia](authelia.md) — Open-source authentication and authorization server that can work as a companion to common reverse proxies like Traefik
- [OAuth2-Proxy](oauth2-proxy.md) — Reverse proxy and static file server that provides authentication using OpenID Connect providers (Google, GitHub, authentik, Keycloak, and others) to SSO-protect services which do not support SSO natively
