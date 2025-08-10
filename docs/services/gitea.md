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

The playbook can install and configure [Gitea](https://gitea.org) for you.

Gitea is a self-hosted lightweight software forge (Git hosting service, etc.), an alternative to [Gitea](https://gitea.io/).

See the project's [documentation](https://gitea.org/docs/latest/) to learn what Gitea does and why it might be useful to you.

For details about configuring the [Ansible role for Gitea](https://github.com/mother-of-all-self-hosting/ansible-role-gitea), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-gitea/blob/main/docs/configuring-gitea.md) online
- 📁 `roles/galaxy/gitea/docs/configuring-gitea.md` locally, if you have [fetched the Ansible roles](../installing.md)

> [!WARNING]
> [Gitea is Open Core](https://codeberg.org/forgejo/discussions/issues/102) and your interests may be better served by using and supporting [Forgejo](forgejo.md) instead. See the [Comparison with Gitea](https://forgejo.org/compare-to-gitea/) page for more information. You may also wish to see our [Migrating from Gitea](forgejo.md#migrating-from-gitea) guide.

## Dependencies

This service requires the following other services:

- a [Postgres](postgres.md) database
- a [Traefik](traefik.md) reverse-proxy server

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

### Configure SSH port for Gitea (optional)

Gitea uses port 22 for its SSH feature by default. We recommend you to move your regular SSH server to another port and stick to this default for your Gitea instance, but you can have the instance listen to another port. See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-gitea/blob/main/docs/configuring-gitea.md#configure-ssh-port-for-gitea-optional) on the role's documentation for details.

## Usage

After running the command for installation, the Gitea instance becomes available at the URL specified with `gitea_hostname` and `gitea_path_prefix`. With the configuration above, the service is hosted at `https://mash.example.com/gitea`.

To get started, open the URL with a web browser, and follow the set up wizard.

## Migrating from Gitea

Gitea is a fork of [Gitea](gitea.md). Migrating Gitea (versions up to and including v1.22.0) to Gitea was relatively easy, but [Gitea versions after v1.22.0 do not allow such transparent upgrades anymore](https://gitea.org/2024-12-gitea-compatibility/).

Nevertheless, upgrades may be possible with some manual work. See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-gitea/blob/main/docs/configuring-gitea.md#migrating-from-gitea) on the role's documentation for details.

## Related services

- [Gitea Runner](gitea-runner.md) — Runner to use with Gitea Actions
- [Gitea](gitea.md) — Painless self-hosted [Git](https://git-scm.com/) service
- [Woodpecker CI](woodpecker-ci.md) — Simple Continuous Integration (CI) engine with great extensibility

### Integration with Woodpecker CI

If you want to integrate Gitea with Woodpecker CI, and if you plan to serve Woodpecker CI under a subpath on the same host as Gitea (e.g., Gitea lives at `https://mash.example.com` and Woodpecker CI lives at `https://mash.example.com/ci`), then you need to configure Gitea to use the host's external IP when invoking webhooks from Woodpecker CI. You can do it by setting the following variables:

```yaml
gitea_container_add_host_domain_name: "{{ woodpecker_ci_server_hostname }}"
gitea_container_add_host_domain_ip_address: "{{ ansible_host }}"

# If ansible_host points to an internal IP address, you may need to allow Gitea to make requests to it.
# By default, requests are only allowed to external IP addresses for security reasons.
# See: https://gitea.org/docs/latest/admin/config-cheat-sheet/#webhook-webhook
gitea_environment_variables_additional_variables: |
  FORGEJO__webhook__ALLOWED_HOST_LIST=external,{{ ansible_host }}
```
