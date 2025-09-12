<!--
SPDX-FileCopyrightText: 2020 - 2024 MDAD project contributors
SPDX-FileCopyrightText: 2020 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2020 Aaron Raimist
SPDX-FileCopyrightText: 2020 Chris van Dijk
SPDX-FileCopyrightText: 2020 Dominik Zajac
SPDX-FileCopyrightText: 2020 Mickaël Cornière
SPDX-FileCopyrightText: 2022 François Darveau
SPDX-FileCopyrightText: 2022 Julian Foad
SPDX-FileCopyrightText: 2022 Warren Bailey
SPDX-FileCopyrightText: 2023 Antonis Christofides
SPDX-FileCopyrightText: 2023 Felix Stupp
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Tinyauth

The playbook can install and configure [Tinyauth](https://tinyauth.app) for you.

Tinyauth is a simple authentication middleware that adds a login screen or OAuth with Google, Github, and any provider to your Docker services. It also supports Lightweight Directory Access Protocol (LDAP).

See the project's [documentation](https://tinyauth.app/docs/about) to learn what Tinyauth does and why it might be useful to you.

For details about configuring the [Ansible role for Tinyauth](https://codeberg.org/acioustick/ansible-role-tinyauth), you can check them via:
- 🌐 [the role's documentation](https://codeberg.org/acioustick/ansible-role-tinyauth/src/branch/master/docs/configuring-tinyauth.md) online
- 📁 `roles/galaxy/tinyauth/docs/configuring-tinyauth.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Prerequisites

💡 *If you intend to enable logging in via OAuth only, you can skip this step.*

The Tinyauth service requires at least one user to have been created and specified for a successful launch, unless logging in with a user is disabled in favor of OAuth.

You can generate a first user with its TOTP secret by running the command below:

```sh
ansible-playbook -i inventory/hosts setup.yml --tags=create-user-tinyauth -e username=USERNAME_HERE -e password=RAW_PASSWORD_HERE
```

Then, specify the output to the `tinyauth_environment_variables_users` environment variable on your `vars.yml` file.

Refer to [this section](https://codeberg.org/acioustick/ansible-role-tinyauth/src/branch/master/docs/configuring-tinyauth.md#prerequisites) on the role's documentation for details.

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

>[!NOTE]
> Tinyauth is available for other proxies like nginx and Caddy. See the documentation for details: <https://tinyauth.app/docs/guides/nginx-proxy-manager> and <https://tinyauth.app/docs/community/caddy>

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# tinyauth                                                             #
#                                                                      #
########################################################################

tinyauth_enabled: true

tinyauth_hostname: tinyauth.example.com

########################################################################
#                                                                      #
# /tinyauth                                                            #
#                                                                      #
########################################################################
```

With this configuration, Tinyauth will set a cookie for `.example.com` for authentication. Note that all your services to be authenticated will need to be under this domain. See [this section](https://tinyauth.app/docs/getting-started/#set-up-the-domains) on the official documentation for details.

**Note**: hosting Tinyauth under a subpath (by configuring the `tinyauth_path_prefix` variable) does not seem to be possible due to Tinyauth's technical limitations.

### Configuring OAuth (optional)

If you skipped creating a user to use OAuth authentication only, you can configure authentication with your OAuth provider by following the instruction available on [this section](https://codeberg.org/acioustick/ansible-role-tinyauth/src/branch/master/docs/configuring-tinyauth.md#oauth) of the role's documentation.

>[!NOTE]
> When setting OAuth configuration, make sure to set the `OAUTH_WHITELIST` environment variable to limit who is allowed to log in with OAuth. Enabling OAuth solely will not activate authorization!

## Usage

After running the command for installation, the Tinyauth instance becomes available at the URL specified with `tinyauth_hostname`. With the configuration above, the service is hosted at `https://tinyauth.example.com`.

Open the URL `https://tinyauth.example.com` and confirm that you can log in to Tinyauth with the generated credentials or via your OAuth provider if it is enabled.

### Add Traefik's labels

You can enable Tinyauth for a service by simply adding a Traefik label as below:

```txt
traefik.http.routers.YOUR_ROUTER_HERE.middlewares={{ tinyauth_identifier }}
```

Replace `YOUR_ROUTER_HERE` with a proper value. On this playbook, the value has the common format: `{{ *_identifier }}`.

For example, you can enable Tinyauth for [echoip](echoip.md) by adding the following configuration to your `vars.yml` file:

```yaml
########################################################################
#                                                                      #
# echoip                                                               #
#                                                                      #
########################################################################

echoip_enabled: true

echoip_hostname: echoip.example.com

echoip_container_labels_additional_labels: |
  traefik.http.routers.{{ echoip_identifier }}.middlewares={{ tinyauth_identifier }}

########################################################################
#                                                                      #
# /echoip                                                              #
#                                                                      #
########################################################################
```

After re-running the playbook, accessing to `https://echoip.example.com` redirects to the Tinyauth log in page at `https://tinyauth.example.com`.

### Integrating with Pocket ID

Pocket ID is a simple OpenID Connect (OIDC) provider (Identity Provider, IdP) that accepts exclusively passkeys for authentication. This playbook supports it, and it is possible to set up the Tinyauth instance as a proxy service for it.

See [this page](pocket-id.md) for the instruction to install Pocket ID with this playbook.

After installing it and adding Tinyauth as an OIDC client on the Pocket ID's UI (see [this section](https://tinyauth.app/docs/guides/pocket-id/#configuring-pocket-id) for details), add Pocket ID as a generic OAuth provider by adding the configuration as below:

```yaml
tinyauth_environment_variables_additional_variables: |
  GENERIC_CLIENT_ID=YOUR_POCKET_ID_CLIENT_ID_HERE
  GENERIC_CLIENT_SECRET=YOUR_POCKET_ID_CLIENT_SECRET_HERE
  GENERIC_AUTH_URL=https://{{ pocket_id_hostname }}/authorize
  GENERIC_TOKEN_URL=https://{{ pocket_id_hostname }}/api/oidc/token
  GENERIC_USER_URL=https://{{ pocket_id_hostname }}/api/oidc/userinfo
  GENERIC_SCOPES=openid email profile groups
  GENERIC_NAME=Pocket ID
  OAUTH_WHITELIST=YOUR_POCKET_ID_EMAIL_ADDRESS_HERE
```

Replace `YOUR_POCKET_ID_CLIENT_ID_HERE`, `YOUR_POCKET_ID_CLIENT_SECRET_HERE`, and `YOUR_POCKET_ID_EMAIL_ADDRESS_HERE` with your own values.

Instead of using `OAUTH_WHITELIST`, it is able to manage access control by using Pocket ID's user group function. See [this section](https://tinyauth.app/docs/guides/pocket-id/#access-controls-with-pocket-id-groups) on the Tinyauth's documentation for details.

#### Example: passkey-only authentication with access control for echoip

Here is an example of the whole stack of the configuration for:

- Enabling passkey-only authentication for echoip (`echoip.example.com`)
- Setting up access control by Pocket ID (`pocketid.example.com`) to limit accessing the echoip instance to users who belong to the `admins` group managed on the Pocket ID instance

```yaml
########################################################################
#                                                                      #
# echoip                                                               #
#                                                                      #
########################################################################

echoip_enabled: true

echoip_hostname: echoip.example.com

# Access control by Pocket ID with the `tinyauth.oauth.groups` label
echoip_container_labels_additional_labels: |
  traefik.http.routers.{{ echoip_identifier }}.middlewares={{ tinyauth_identifier }}
  tinyauth.oauth.groups=admins

########################################################################
#                                                                      #
# /echoip                                                              #
#                                                                      #
########################################################################

########################################################################
#                                                                      #
# pocket_id                                                            #
#                                                                      #
########################################################################

pocket_id_enabled: true

pocket_id_hostname: pocketid.example.com

########################################################################
#                                                                      #
# /pocket_id                                                           #
#                                                                      #
########################################################################

########################################################################
#                                                                      #
# tinyauth                                                             #
#                                                                      #
########################################################################

tinyauth_enabled: true

tinyauth_hostname: tinyauth.example.com

# Obtain the ODIC client ID and secret for Tinyauth at pocketid.example.com first
tinyauth_environment_variables_additional_variables: |
  GENERIC_CLIENT_ID=YOUR_POCKET_ID_CLIENT_ID_HERE
  GENERIC_CLIENT_SECRET=YOUR_POCKET_ID_CLIENT_SECRET_HERE
  GENERIC_AUTH_URL=https://{{ pocket_id_hostname }}/authorize
  GENERIC_TOKEN_URL=https://{{ pocket_id_hostname }}/api/oidc/token
  GENERIC_USER_URL=https://{{ pocket_id_hostname }}/api/oidc/userinfo
  GENERIC_SCOPES=openid email profile groups
  GENERIC_NAME=Pocket ID

# Disable logging in with a password
tinyauth_environment_variables_users_enabled: false

########################################################################
#                                                                      #
# /tinyauth                                                            #
#                                                                      #
########################################################################
```

After configuring the Pocket ID instance and restarting the services, accessing `echoip.example.com` automatically redirects you to `tinyauth.example.com`, where you can then proceed to log in only via `pocketid.example.com` with your registered passkey.

## Troubleshooting

See [this section](https://codeberg.org/acioustick/ansible-role-tinyauth/src/branch/master/docs/configuring-tinyauth.md#troubleshooting) on the role's documentation for details.

## Related services

- [Authelia](authelia.md) — Open-source authentication and authorization server that can work as a companion to common reverse proxies like Traefik
- [authentik](authentik.md) — Open-source identity provider focused on flexibility and versatility
- [Keycloak](keycloak.md) — Open source identity and access management solution
