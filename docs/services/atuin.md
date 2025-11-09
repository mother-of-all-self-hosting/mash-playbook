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

# Atuin server

The playbook can install and configure [Atuin](https://atuin.sh/) server for you.

Atuin server is an optional data synchronization server for Atuin, which replaces your existing shell history with a SQLite database to enable faster history search.

See the project's [documentation](https://docs.atuin.sh/self-hosting/server-setup/) to learn what Atuin server does and why it might be useful to you.

For details about configuring the [Ansible role for Atuin server](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az4ATDhf89CPqP7XCLNpNwobuJ9fBs), you can check them via:
- 🌐 [the role's documentation](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az4ATDhf89CPqP7XCLNpNwobuJ9fBs/tree/docs/configuring-atuin.md) online
- 📁 `roles/galaxy/atuin/docs/configuring-atuin.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Postgres](postgres.md) / [SQLite](https://www.sqlite.org/) database
- [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# atuin                                                                #
#                                                                      #
########################################################################

atuin_enabled: true

atuin_hostname: atuin.example.com

########################################################################
#                                                                      #
# /atuin                                                               #
#                                                                      #
########################################################################
```

**Note**: hosting Atuin server under a subpath (by configuring the `atuin_path_prefix` variable) does not seem to be possible due to Atuin server's technical limitations.

### Select database to use

It is necessary to select a database used by Atuin server from Postgres and SQLite. See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az4ATDhf89CPqP7XCLNpNwobuJ9fBs/tree/docs/configuring-atuin.md#specify-database) on the role's documentation for details.

### Enabling signing up

By default account registration for the service is disabled. To enable it, add the following configuration to your `vars.yml` file:

```yaml
atuin_environment_variables_open_registration: true
```

## Usage

After installation, the Atuin server instance becomes available at the URL specified with `atuin_hostname`. With the configuration above, the service is hosted at `https://atuin.example.com`.

To get started, [install Atuin](https://docs.atuin.sh/guide/installation/) on your local computer if it is not yet available there, and proceed to configure synchronization. See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az4ATDhf89CPqP7XCLNpNwobuJ9fBs/tree/docs/configuring-atuin.md#usage) on the role's documentation for details.

Since account registration is disabled by default, you need to enable it first by setting `atuin_environment_variables_open_registration` to `true` temporarily in order to create your own account.

## Troubleshooting

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az4ATDhf89CPqP7XCLNpNwobuJ9fBs/tree/docs/configuring-atuin.md#troubleshooting) on the role's documentation for details.
