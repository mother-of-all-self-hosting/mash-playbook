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
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Authelia

The playbook can install and configure [Authelia](https://www.authelia.com/) for you.

Authelia is an open-source [authentication](https://www.authelia.com/overview/authentication/introduction/) and [authorization](https://www.authelia.com/overview/authorization/access-control/) server and portal fulfilling the identity and access management (IAM) role of information security in providing [multi-factor authentication](https://www.authelia.com/overview/authentication/introduction/) and single sign-on (SSO) for your applications via a web portal.

See the project's [documentation](https://www.authelia.com/integration/prologue/get-started/) to learn what Authelia does and why it might be useful to you.

For details about configuring the [Ansible role for Authelia](https://github.com/mother-of-all-self-hosting/ansible-role-authelia), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-authelia/blob/main/docs/configuring-authelia.md) online
- 📁 `roles/galaxy/authelia/docs/configuring-authelia.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Postgres](postgres.md) / MySQL / [MariaDB](mariadb.md) / [SQLite](https://www.sqlite.org/) database
- [Traefik](traefik.md) reverse-proxy server
- (optional; recommended) [Valkey](valkey.md) — if not enabled, restarting Authelia destroys user sessions

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# authelia                                                             #
#                                                                      #
########################################################################

authelia_enabled: true

authelia_hostname: authelia.example.com

# The configuration below connects Authelia to the Valkey instance, for session storage purposes.
# You may wish to run a separate Valkey instance for Authelia, because Valkey is not multi-tenant.
# Read more in docs/services/valkey.md.
# If Valkey is not available, session data will be stored in memory and will be lost on container restart.
authelia_redis_socket_enabled: false
authelia_redis_hostname: "{{ valkey_identifier if valkey_enabled else '' }}"

########################################################################
#                                                                      #
# /authelia                                                            #
#                                                                      #
########################################################################
```

**Note**: hosting Authelia under a subpath (by configuring the `authelia_path_prefix` variable) does not seem to be possible due to Authelia's technical limitations.

### Set a random string

You also need to set a random string to the variable as below by adding the following configuration to your `vars.yml` file. The value can be generated with `pwgen -s 64 1` or in another way.

```yaml
authelia_config_storage_encryption_key: YOUR_SECRET_KEY_HERE
```

>[!WARNING]
> Changing `authelia_config_storage_encryption_key` subsequently will cause trouble unless you use the CLI to migrate.

### Set the base domain for session cookies

You also need to specify the base domain that session cookies related to authentication will be set on. Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-authelia/blob/main/docs/configuring-authelia.md#set-the-base-domain-for-session-cookies) on the role's documentation for details.

### Select database to use

It is necessary to select a database used by Authelia from a MySQL compatible database, Postgres, and SQLite. Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-authelia/blob/main/docs/configuring-authelia.md#configuring-database) on the role's documentation for details.

>[!NOTE]
> If you have neither enabled MariaDB or disabled Postgres explicitly with this playbook, the database for your existing installation is most likely to be `postgres`.

### Configuring operation modes

Authelia can be used in two different modes, which can be enabled simultaneously. Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-authelia/blob/main/docs/configuring-authelia.md#configuring-operation-modes) on the role's documentation for details.

### Configuring authentication storage providers

Authelia supports [file-based](https://www.authelia.com/configuration/first-factor/file/) and [LDAP](https://www.authelia.com/configuration/first-factor/ldap/) storage providers for the user database. Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-authelia/blob/main/docs/configuring-authelia.md#configuring-authentication-storage-providers) on the role's documentation for details.

## Usage

After running the command for installation, the Authelia instance becomes available at the URL specified with `authelia_hostname`. With the configuration above, the service is hosted at `https://authelia.example.com`.

To get started, open the URL with a web browser to log in to the portal website where you can and manage your user account.

## Related services

- [authentik](authentik.md) — Identity Provider focused on flexibility and versatility
- [Keycloak](keycloak.md) — Identity and access management solution
- [OAuth2-Proxy](oauth2-proxy.md) — Reverse proxy and static file server that provides authentication using OpenID Connect providers
- [Pocket ID](pocket-id.md) — OIDC provider for passkey-only authentication
- [Tinyauth](tinyauth.md) — Authentication middleware that adds a login screen or OAuth with providers to Docker services
