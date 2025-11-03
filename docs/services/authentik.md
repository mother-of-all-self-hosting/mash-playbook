<!--
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# authentik

The playbook can install and configure [authentik](https://goauthentik.io/) for you.

authentik is an open-source Identity Provider (IdP) focused on flexibility and versatility.

> [!WARNING]
> The SSO system of authentik is pretty complex, and we have only tested OIDC and OAuth integration. There is a high probability that using outposts/LDAP would need further configuration efforts. Make sure you test before using this in production, and feel free to provide feedback!

## Dependencies

This service requires the following other services:

- a [Postgres](postgres.md) database
- a [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file:

```yaml
########################################################################
#                                                                      #
# authentik                                                            #
#                                                                      #
########################################################################

authentik_enabled: true

authentik_hostname: authentik.example.com

# Put a strong secret below, generated with `pwgen -s 64 1` or in another way
authentik_secret_key: ''

########################################################################
#                                                                      #
# /authentik                                                           #
#                                                                      #
########################################################################
```

### Extending the configuration

There are some additional things you may wish to configure about the service.

Take a look at:

- [authentik](https://github.com/mother-of-all-self-hosting/ansible-role-authentik)'s [`defaults/main.yml`](https://github.com/mother-of-all-self-hosting/ansible-role-authentik/blob/main/defaults/main.yml) for some variables that you can customize via your `vars.yml` file.

## Installation

Once you're done configuring authentik, proceed to run the [installing](../installing.md) command.

## Usage

After running the command for installation, the authentik instance becomes available at the URL specified with `authentik_hostname`. With the configuration above, the service is hosted at `https://authentik.example.com`.

You can set the admin password at `https://authentik.example.com/if/flow/initial-setup/`, and start adding applications and users. Refer to the [official documentation](https://goauthentik.io/docs/) to learn how to integrate services.

When it comes to this playbook, tested configuration examples are described on the respective service documentation. See below for details:

- [Grafana](grafana.md#single-sign-on-authentik)
- [Nextcloud](nextcloud.md#single-sign-on-authentik)

## Related services

- [Authelia](authelia.md) — Open-source authentication and authorization server that can work as a companion to common reverse proxies like Traefik
- [Keycloak](keycloak.md) — Open source identity and access management solution
- [OAuth2-Proxy](oauth2-proxy.md) — Reverse proxy and static file server that provides authentication using OpenID Connect providers (Google, GitHub, authentik, Keycloak, and others) to SSO-protect services which do not support SSO natively
- [Pocket ID](pocket-id.md) — Simple OIDC provider for passkey-only authentication
- [Tinyauth](tinyauth.md) — Simple authentication middleware that adds a login screen or OAuth with Google, Github, and any provider to your Docker services
