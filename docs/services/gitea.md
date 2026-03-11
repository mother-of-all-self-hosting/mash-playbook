<!--
SPDX-FileCopyrightText: 2020 - 2024 MDAD project contributors
SPDX-FileCopyrightText: 2020 - 2025 Slavi Pantaleev
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
SPDX-FileCopyrightText: 2023 MASH project contributors
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara
SPDX-FileCopyrightText: 2024 Sergio Durigan Junior

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Gitea

The playbook can install and configure [Gitea](https://gitea.io) for you.

Gitea is a self-hosted lightweight software forge (Git hosting service, etc).

See the project's [documentation](https://docs.gitea.com/) to learn what Gitea does and why it might be useful to you.

For details about configuring the [Ansible role for Gitea](https://github.com/mother-of-all-self-hosting/ansible-role-gitea), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-gitea/blob/main/docs/configuring-gitea.md) online
- 📁 `roles/galaxy/gitea/docs/configuring-gitea.md` locally, if you have [fetched the Ansible roles](../installing.md)

> [!WARNING]
> [Gitea is Open Core](https://codeberg.org/forgejo/discussions/issues/102) and your interests may be better served by using and supporting [Forgejo](forgejo.md) instead. See the [Comparison with Gitea](https://forgejo.org/compare-to-gitea/) page for more information. You may also wish to see our [Migrating from Gitea](forgejo.md#migrating-from-gitea) guide.

## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server
- (optional) [Postgres](postgres.md) / MySQL / [MariaDB](mariadb.md) database

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# gitea                                                                #
#                                                                      #
########################################################################

gitea_enabled: true

gitea_hostname: mash.example.com
gitea_path_prefix: /gitea

########################################################################
#                                                                      #
# /gitea                                                               #
#                                                                      #
########################################################################
```

### Select database to use

It is necessary to select a database used by Gitea from a MySQL compatible database, Postgres, and SQLite. See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-gitea/blob/main/docs/configuring-gitea.md#specify-database) on the role's documentation for details.

### Configure SSH port for Gitea (optional)

Gitea uses port 22 for its SSH feature by default. We recommend you to move your regular SSH server to another port and stick to this default for your Gitea instance, but you can have the instance listen to another port. See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-gitea/blob/main/docs/configuring-gitea.md#configure-ssh-port-for-gitea-optional) on the role's documentation for details.

### Configuring cache (optional)

Gitea uses caching to avoid repeating expensive operations. By default the internal memory (`memory`) is enabled for it, but you can use a specific cache adapter like [Redis](redis.md) and [Memcached](memcached.md). See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-gitea/blob/main/docs/configuring-gitea.md#configuring-cache-optional) on the role's documentation for details.

## Usage

After running the command for installation, the Gitea instance becomes available at the URL specified with `gitea_hostname` and `gitea_path_prefix`. With the configuration above, the service is hosted at `https://mash.example.com/gitea`.

To get started, open the URL with a web browser, and follow the set up wizard.

## Related services

- [Forgejo](forgejo.md) — Self-hosted lightweight software forge (Git hosting service, etc.)
- [Radicle node](radicle-node.md) — Network daemon for the [Radicle](https://radicle.xyz/) network, a peer-to-peer code collaboration stack built on Git
- [Woodpecker CI](woodpecker-ci.md) — Simple Continuous Integration (CI) engine with great extensibility
