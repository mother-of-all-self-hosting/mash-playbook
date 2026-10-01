<!--
SPDX-FileCopyrightText: 2020 Aaron Raimist
SPDX-FileCopyrightText: 2020 Chris van Dijk
SPDX-FileCopyrightText: 2020 Dominik Zajac
SPDX-FileCopyrightText: 2020 Mickaël Cornière
SPDX-FileCopyrightText: 2020-2024 MDAD project contributors
SPDX-FileCopyrightText: 2020-2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2022 François Darveau
SPDX-FileCopyrightText: 2022 Julian Foad
SPDX-FileCopyrightText: 2022 Warren Bailey
SPDX-FileCopyrightText: 2023 Antonis Christofides
SPDX-FileCopyrightText: 2023 Felix Stupp
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 Thomas Miceli
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Keycloak

The playbook can install and configure [Keycloak](https://www.keycloak.org/) for you.

Keycloak is an open-source identity and access management solution.

See the project's [documentation](https://www.keycloak.org/documentation) to learn what Keycloak does and why it might be useful to you.

For details about configuring the [Ansible role for Keycloak](https://github.com/mother-of-all-self-hosting/ansible-role-keycloak), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-keycloak/blob/main/docs/configuring-keycloak.md) online
- 📁 `roles/galaxy/keycloak/docs/configuring-keycloak.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Postgres](postgres.md) database
- [Traefik](traefik.md) reverse-proxy server

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

########################################################################
#                                                                      #
# /keycloak                                                            #
#                                                                      #
########################################################################
```

### Set details for the admin user

You need to create an instance's admin user by setting values to the `keycloak_environment_variable_kc_bootstrap_admin_*` variables. Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-keycloak/blob/main/docs/configuring-keycloak.md#set-details-for-the-admin-user) on the role's documentation for details.

## Usage

After running the command for installation, the Keycloak instance becomes available at the URL specified with `keycloak_hostname` and `keycloak_path_prefix`. With the configuration above, the service is hosted at `https://mash.example.com/keycloak`.

To get started, open the URL with a web browser to log in to the instance with the administrator account.

## Related services

- [authentik](authentik.md) — Identity Provider focused on flexibility and versatility
- [Authelia](authelia.md) — Authentication and authorization server that can work as a companion to common reverse proxies
- [OAuth2-Proxy](oauth2-proxy.md) — Reverse proxy and static file server that provides authentication using OpenID Connect providers
- [Pocket ID](pocket-id.md) — OIDC provider for passkey-only authentication
- [Tinyauth](tinyauth.md) — Authentication middleware that adds a login screen or OAuth with providers to Docker services
