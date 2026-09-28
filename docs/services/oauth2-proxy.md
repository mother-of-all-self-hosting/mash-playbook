<!--
SPDX-FileCopyrightText: 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# OAuth2-Proxy

The playbook can install and configure [OAuth2-Proxy](https://github.com/oauth2-proxy/oauth2-proxy) for you.

OAuth2-Proxy is a reverse proxy and static file server that provides authentication using OpenID Connect Providers (Google, GitHub, [authentik](authentik.md), [Keycloak](keycloak.md), and others) to SSO-protect services which do not support SSO natively.

See the project's [documentation](https://oauth2-proxy.github.io/oauth2-proxy/) to learn what OAuth2-Proxy does and why it might be useful to you.

The [Ansible role for OAuth2-Proxy](https://github.com/mother-of-all-self-hosting/ansible-role-oauth2-proxy) is developed and maintained by the MASH project. For details about configuring OAuth2-Proxy, you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-oauth2-proxy/blob/main/docs/configuring-oauth2-proxy.md) online
- 📁 `roles/galaxy/oauth2_proxy/docs/configuring-oauth2-proxy.md` locally, if you have [fetched the Ansible roles](../installing.md)
