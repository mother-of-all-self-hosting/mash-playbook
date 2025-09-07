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

# Pocket ID

The playbook can install and configure [Pocket ID](https://pocket-id.org) for you.

Pocket ID is a simple OpenID Connect (OIDC) provider (Identity Provider, IdP) that allows users to authenticate with their passkeys to your services.

See the project's [documentation](https://pocket-id.org/docs/) to learn what Pocket ID does and why it might be useful to you.

For details about configuring the [Ansible role for Pocket ID](https://codeberg.org/acioustick/ansible-role-pocket-id), you can check them via:
- 🌐 [the role's documentation](https://codeberg.org/acioustick/ansible-role-pocket-id/src/branch/master/docs/configuring-pocket-id.md) online
- 📁 `roles/galaxy/pocket_id/docs/configuring-pocket-id.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server
- (optional) [Postgres](postgres.md) — Pocket ID will default to [SQLite](https://www.sqlite.org/) if Postgres is not enabled

>[!NOTE]
> It is not recommended to store a SQLite database inside a networked filesystem, such as a NFS or SMB share. See [this section](https://pocket-id.org/docs/configuration/environment-variables#database-connection-string) on the official documentation for details.

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
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
```

**Note**: hosting Pocket ID under a subpath (by configuring the `pocket_id_path_prefix` variable) does not seem to be possible due to Pocket ID's technical limitations.

### Select database to use (optional)

By default Pocket ID is configured to use Postgres, but you can choose SQLite. See [this section](https://codeberg.org/acioustick/ansible-role-pocket-id/src/branch/master/docs/configuring-pocket-id.md#specify-database-optional) on the role's documentation for details.

### Configuring additional settings with environment variables (optional)

The Pocket ID instance's additional settings can be specified with *either its UI or environment variables*.

By default, this playbook enables configuring them on the UI, which therefore disables doing so with environment variables.

>[!NOTE]
> Basic settings can still be configured with environment variables.

See [this section](https://codeberg.org/acioustick/ansible-role-pocket-id/src/branch/master/docs/configuring-pocket-id.md#enable-or-disable-overriding-ui-configuration-with-environment-variables) on the role's documentation for details about what needs specifying.

## Usage

After running the command for installation, the Pocket ID instance becomes available at the URL specified with `pocket_id_hostname`. With the configuration above, the service is hosted at `https://pocketid.example.com`.

To get started, open the URL `https://example.com/setup` on a web browser to create and sign in with an admin account.

See [this section](https://codeberg.org/acioustick/ansible-role-pocket-id/src/branch/master/docs/configuring-pocket-id.md#usage) on the role's documentation for details about how to use Pocket ID.

## Troubleshooting

See [this section](https://codeberg.org/acioustick/ansible-role-pocket-id/src/branch/master/docs/configuring-pocket-id.md#troubleshooting) on the role's documentation for details.

## Related services

- [authentik](authentik.md) — Open-source Identity Provider (IdP) focused on flexibility and versatility
- [Authelia](authelia.md) — Open-source authentication and authorization server that can work as a companion to common reverse proxies like Traefik
- [Keycloak](keycloak.md) — Open source identity and access management solution
- [Tinyauth](tinyauth.md) — Simple authentication middleware that adds a login screen or OAuth with Google, Github, and any provider to your Docker services
