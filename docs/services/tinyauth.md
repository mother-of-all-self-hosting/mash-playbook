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

With this configuration, Tinyauth will set a cookie for `.example.com` for authentication. This means that all your services to be authenticated will need to be under this domain. See [this section](https://tinyauth.app/docs/getting-started/#set-up-the-domains) on the official documentation for details.

**Note**: hosting Tinyauth under a subpath (by configuring the `tinyauth_path_prefix` variable) does not seem to be possible due to Tinyauth's technical limitations.

## Usage

After running the command for installation, the Tinyauth instance becomes available at the URL specified with `tinyauth_hostname`. With the configuration above, the service is hosted at `https://tinyauth.example.com`.

Both default username and password are set to `mash`. Note that you will get a warning after finishing the installation command about the credential specified by default until setting yours, unless logging in via OAuth only is enabled.

See [this section](https://codeberg.org/acioustick/ansible-role-tinyauth/src/branch/master/docs/configuring-tinyauth.md#creating-a-user) on the role's documentation for details about how to create a user. Note that by default generating a time-based one-time password (TOTP) is enabled.

### OAuth

Tinyauth supports OAuth with Google, GitHub, and other generic OAuth providers. See [this section](https://codeberg.org/acioustick/ansible-role-tinyauth/src/branch/master/docs/configuring-tinyauth.md#oauth) on the role's documentation for details.

>[!NOTE]
> When setting OAuth configuration, make sure to set the `OAUTH_WHITELIST` environment variable to limit who is allowed to log in with OAuth.

### Configuring Traefik

After creating the user, you can enable Tinyauth for a service by simply adding a Traefik label as below:

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

## Troubleshooting

See [this section](https://codeberg.org/acioustick/ansible-role-tinyauth/src/branch/master/docs/configuring-tinyauth.md#troubleshooting) on the role's documentation for details.

## Related services

- [Authelia](authelia.md) — Open-source authentication and authorization server that can work as a companion to common reverse proxies like Traefik
- [authentik](authentik.md) — Open-source identity provider focused on flexibility and versatility
- [Keycloak](keycloak.md) — Open source identity and access management solution
