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

# authentik

The playbook can install and configure [authentik](https://goauthentik.io/) for you.

authentik is an open-source Identity Provider (IdP) focused on flexibility and versatility.

> [!WARNING]
> The SSO system of authentik is pretty complex, and we have only tested OIDC and OAuth integration. There is a high probability that using outposts/LDAP would need further configuration efforts. Make sure you test before using this in production, and feel free to provide feedback!

## Dependencies

This service requires the following other services:

- [Postgres](postgres.md) database
- [Traefik](traefik.md) reverse-proxy server
- (optional) [exim-relay](exim-relay.md) mailer

## Configuration

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

### Configuring the mailer (optional)

On authentik you can set up a mailer for functions such as password recovery. If you enable the [exim-relay](exim-relay.md) service in your inventory configuration, the playbook will automatically configure it as a mailer for the service.

To actually have the service use (and get messages sent through the exim-relay service), you will need to adjust settings on the service's UI after the service is installed.

>[!WARNING]
> Without setting an authentication method such as DKIM, SPF, and DMARC for your hostname, emails are most likely to be quarantined as spam at recipient's mail servers. The worst scenario is that your server's IP address or hostname will be included in the spam list such as the one managed by [Spamhaus](https://www.spamhaus.org/), depending on the reputation. As the exim-relay service supports DKIM signing, refer to [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay/blob/main/docs/configuring-exim-relay.md#enable-dkim-support-optional) for details about how to set it up.

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
