<!--
SPDX-FileCopyrightText: 2020 Aaron Raimist
SPDX-FileCopyrightText: 2020 Chris van Dijk
SPDX-FileCopyrightText: 2020 Dominik Zajac
SPDX-FileCopyrightText: 2020 Mickaël Cornière
SPDX-FileCopyrightText: 2020-2024 MDAD project contributors
SPDX-FileCopyrightText: 2020-2025 Slavi Pantaleev
SPDX-FileCopyrightText: 2022 François Darveau
SPDX-FileCopyrightText: 2022 Julian Foad
SPDX-FileCopyrightText: 2022 Warren Bailey
SPDX-FileCopyrightText: 2023 Antonis Christofides
SPDX-FileCopyrightText: 2023 Felix Stupp
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 MASH project contributors
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 Sergio Durigan Junior
SPDX-FileCopyrightText: 2024 Thomas Miceli
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

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

- [Traefik](traefik.md) reverse-proxy server
- (optional) [exim-relay](exim-relay.md) mailer — required on the default configuration
- (optional) [Meilisearch](meilisearch.md)
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

### Configuring issue indexer (optional)

By default Gitea is configured to use `bleve` as an issue indexer, but you can use another indexer like Meilisearch.

Meilisearch is available on the playbook. To have the Gitea instance connect to it, add the following configuration to your `vars.yml` file, after enabling it and setting the default admin API key (`meilisearch_default_admin_api_key`):

```yaml
gitea_environment_variables_indexer_issue_indexer_type: meilisearch
```

See [this page](meilisearch.md) for details about how to install it and setting the key for the Meilisearch instance.

### Configuring the mailer (optional)

On Gitea you can set up a mailer for functions such as password recovery. If you enable the [exim-relay](exim-relay.md) service in your inventory configuration, the playbook will automatically configure it as a mailer for the service.

To actually have the service use (and get messages sent through the exim-relay service), you will need to adjust settings on the service's UI after the service is installed.

>[!WARNING]
> Without setting an authentication method such as DKIM, SPF, and DMARC for your hostname, emails are most likely to be quarantined as spam at recipient's mail servers. The worst scenario is that your server's IP address or hostname will be included in the spam list such as the one managed by [Spamhaus](https://www.spamhaus.org/), depending on the reputation. As the exim-relay service supports DKIM signing, refer to [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay/blob/main/docs/configuring-exim-relay.md#enable-dkim-support-optional) for details about how to set it up.

### Integrating with Prometheus (optional)

Gitea can natively expose metrics to [Prometheus](prometheus.md).

#### Expose metrics internally

If Gitea and Prometheus do not share a network (like Traefik), you can connect the Gitea container network to Prometheus by adding the following configuration to your `vars.yml` file:

```yaml
prometheus_container_additional_networks_custom:
  - "{{ gitea_container_network }}"
```

#### Expose metrics publicly

If Gitea metrics are not scraped from a local Prometheus instance, you can expose the metrics publicly so that a remote instance can fetch them.

When exposing metrics publicly, you should consider to set up [HTTP Basic Authentication](https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication) **or anyone would be able to read your metrics**.

To expose the metrics publicly, add the following configuration to your `vars.yml` file (adapt to your needs):

```yaml
mash_playbook_metrics_exposure_enabled: true
mash_playbook_metrics_exposure_hostname: mash.example.com
```

It will expose the metrics at `https://mash.example.com/metrics/mash-gitea`.

To enable the HTTP Basic authentication, add the following configuration to your `vars.yml` file (adapt to your needs):

```yaml
gitea_container_labels_traefik_metrics_middleware_basic_auth_enabled: true

# See https://doc.traefik.io/traefik/middlewares/http/basicauth/#users for details.
gitea_container_labels_traefik_metrics_middleware_basic_auth_users: ""
```

## Usage

After running the command for installation, the Gitea instance becomes available at the URL specified with `gitea_hostname` and `gitea_path_prefix`. With the configuration above, the service is hosted at `https://mash.example.com/gitea`.

To get started, open the URL with a web browser, and follow the set up wizard.

## Related services

- [Forgejo](forgejo.md) — Self-hosted lightweight software forge (Git hosting service, etc.)
- [Radicle node](radicle-node.md) — Network daemon for the [Radicle](https://radicle.xyz/) network, a peer-to-peer code collaboration stack built on Git
- [Woodpecker CI](woodpecker-ci.md) — Simple Continuous Integration (CI) engine with great extensibility
