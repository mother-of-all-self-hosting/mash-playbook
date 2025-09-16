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

# Forgejo

The playbook can install and configure [Forgejo](https://forgejo.org) for you.

Forgejo is a self-hosted lightweight software forge (Git hosting service, etc.), an alternative to [Gitea](https://gitea.io/).

See the project's [documentation](https://forgejo.org/docs/latest/) to learn what Forgejo does and why it might be useful to you.

For details about configuring the [Ansible role for Forgejo](https://github.com/mother-of-all-self-hosting/ansible-role-forgejo), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-forgejo/blob/main/docs/configuring-forgejo.md) online
- 📁 `roles/galaxy/forgejo/docs/configuring-forgejo.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server
- (optional) [Postgres](postgres.md) / MySQL / [MariaDB](mariadb.md) database — Forgejo will default to [SQLite](https://www.sqlite.org/) if Postgres is not enabled

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# forgejo                                                              #
#                                                                      #
########################################################################

forgejo_enabled: true

forgejo_hostname: mash.example.com
forgejo_path_prefix: /forgejo

########################################################################
#                                                                      #
# /forgejo                                                             #
#                                                                      #
########################################################################
```

### Select database to use (optional)

By default Forgejo is configured to use Postgres, but you can choose other database such as SQLite and MySQL (MariaDB).

To use MariaDB, add the following configuration to your `vars.yml` file:

```yaml
forgejo_database_type: mysql
```

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-forgejo/blob/main/docs/configuring-forgejo.md#specify-database-optional) on the role's documentation for details.

### Configure SSH port for Forgejo (optional)

Forgejo uses port 22 for its SSH feature by default. We recommend you to move your regular SSH server to another port and stick to this default for your Forgejo instance, but you can have the instance listen to another port. See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-forgejo/blob/main/docs/configuring-forgejo.md#configure-ssh-port-for-forgejo-optional) on the role's documentation for details.

## Usage

After running the command for installation, the Forgejo instance becomes available at the URL specified with `forgejo_hostname` and `forgejo_path_prefix`. With the configuration above, the service is hosted at `https://mash.example.com/forgejo`.

To get started, open the URL with a web browser, and follow the set up wizard.

## Migrating from Gitea

Forgejo is a fork of [Gitea](gitea.md). Migrating Gitea (versions up to and including v1.22.0) to Forgejo was relatively easy, but [Gitea versions after v1.22.0 do not allow such transparent upgrades anymore](https://forgejo.org/2024-12-gitea-compatibility/).

Nevertheless, upgrades may be possible with some manual work. See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-forgejo/blob/main/docs/configuring-forgejo.md#migrating-from-gitea) on the role's documentation for details.

## Related services

- [Forgejo Runner](forgejo-runner.md) — Runner to use with Forgejo Actions
- [Gitea](gitea.md) — Painless self-hosted [Git](https://git-scm.com/) service
- [Woodpecker CI](woodpecker-ci.md) — Simple Continuous Integration (CI) engine with great extensibility

### Integration with Woodpecker CI

If you want to integrate Forgejo with Woodpecker CI, and if you plan to serve Woodpecker CI under a subpath on the same host as Forgejo (e.g., Forgejo lives at `https://mash.example.com` and Woodpecker CI lives at `https://mash.example.com/ci`), then you need to configure Forgejo to use the host's external IP when invoking webhooks from Woodpecker CI. You can do it by setting the following variables:

```yaml
forgejo_container_add_host_domain_name: "{{ woodpecker_ci_server_hostname }}"
forgejo_container_add_host_domain_ip_address: "{{ ansible_host }}"

# If ansible_host points to an internal IP address, you may need to allow Forgejo to make requests to it.
# By default, requests are only allowed to external IP addresses for security reasons.
# See: https://forgejo.org/docs/latest/admin/config-cheat-sheet/#webhook-webhook
forgejo_environment_variables_additional_variables: |
  FORGEJO__webhook__ALLOWED_HOST_LIST=external,{{ ansible_host }}
```
