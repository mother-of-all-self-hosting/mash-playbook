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
SPDX-FileCopyrightText: 2024 Tiz
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

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

- [Traefik](traefik.md) reverse-proxy server
- (optional) [exim-relay](exim-relay.md) mailer — required on the default configuration
- (optional) [Meilisearch](meilisearch.md)
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

### Configuring cache (optional)

Forgejo uses caching to avoid repeating expensive operations. By default the internal memory (`memory`) is enabled for it, but you can use a specific cache adapter like [Redis](redis.md) and [Memcached](memcached.md). See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-forgejo/blob/main/docs/configuring-forgejo.md#configuring-cache-optional) on the role's documentation for details.

### Configuring issue indexer (optional)

By default Forgejo is configured to use `bleve` as an issue indexer, but you can use another indexer like Meilisearch.

Meilisearch is available on the playbook. To have the Forgejo instance connect to it, add the following configuration to your `vars.yml` file, after enabling it and setting the default admin API key (`meilisearch_default_admin_api_key`):

```yaml
forgejo_environment_variables_indexer_issue_indexer_type: meilisearch
```

See [this page](meilisearch.md) for details about how to install it and setting the key for the Meilisearch instance.

### Configuring the mailer (optional)

On Forgejo you can set up a mailer for functions such as password recovery. If you enable the [exim-relay](exim-relay.md) service in your inventory configuration, the playbook will automatically configure it as a mailer for the service.

To actually have the service use (and get messages sent through the exim-relay service), you will need to adjust settings on the service's UI after the service is installed.

>[!WARNING]
> Without setting an authentication method such as DKIM, SPF, and DMARC for your hostname, emails are most likely to be quarantined as spam at recipient's mail servers. The worst scenario is that your server's IP address or hostname will be included in the spam list such as the one managed by [Spamhaus](https://www.spamhaus.org/), depending on the reputation. As the exim-relay service supports DKIM signing, refer to [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay/blob/main/docs/configuring-exim-relay.md#enable-dkim-support-optional) for details about how to set it up.

### Configuring OAuth2/OpenID Connect login (optional)

You can configure Forgejo to authenticate users through an OpenID Connect provider.

Add variables like these to your `vars.yml` file:

```yaml
forgejo_oidc_client_enabled: true

forgejo_oidc_provider_name: "authentik"
forgejo_oidc_client_id: "FORGEJO_OIDC_CLIENT_ID_HERE"
forgejo_oidc_client_secret: "FORGEJO_OIDC_CLIENT_SECRET_HERE"
forgejo_oidc_auto_discover_url: "https://sso.example.com/application/o/forgejo/.well-known/openid-configuration"
```

To apply only OAuth configuration tasks, run:

```sh
just run-tags configure-oauth-forgejo
```

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-forgejo/blob/main/docs/configuring-forgejo.md#configure-oauth2openid-connect-login-optional) on the role's documentation for additional options.

### Integrating with Prometheus (optional)

Forgejo can natively expose metrics to [Prometheus](prometheus.md).

#### Expose metrics internally

If Forgejo and Prometheus do not share a network (like Traefik), you can connect the Forgejo container network to Prometheus by adding the following configuration to your `vars.yml` file:

```yaml
prometheus_container_additional_networks_custom:
  - "{{ forgejo_container_network }}"
```

#### Expose metrics publicly

If Forgejo metrics are not scraped from a local Prometheus instance, you can expose the metrics publicly so that a remote instance can fetch them.

When exposing metrics publicly, you should consider to set up [HTTP Basic Authentication](https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication) **or anyone would be able to read your metrics**.

To expose the metrics publicly, add the following configuration to your `vars.yml` file (adapt to your needs):

```yaml
mash_playbook_metrics_exposure_enabled: true
mash_playbook_metrics_exposure_hostname: mash.example.com
```

It will expose the metrics at `https://mash.example.com/metrics/mash-forgejo`.

To enable the HTTP Basic authentication, add the following configuration to your `vars.yml` file (adapt to your needs):

```yaml
forgejo_container_labels_traefik_metrics_middleware_basic_auth_enabled: true

# See https://doc.traefik.io/traefik/middlewares/http/basicauth/#users for details.
forgejo_container_labels_traefik_metrics_middleware_basic_auth_users: ""
```

## Usage

After running the command for installation, the Forgejo instance becomes available at the URL specified with `forgejo_hostname` and `forgejo_path_prefix`. With the configuration above, the service is hosted at `https://mash.example.com/forgejo`.

To get started, open the URL with a web browser, and follow the set up wizard.

## Migrating from Gitea

Forgejo is a fork of [Gitea](gitea.md). Migrating Gitea (versions up to and including v1.22.0) to Forgejo was relatively easy, but [Gitea versions after v1.22.0 do not allow such transparent upgrades anymore](https://forgejo.org/2024-12-gitea-compatibility/).

Nevertheless, upgrades may be possible with some manual work. See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-forgejo/blob/main/docs/configuring-forgejo.md#migrating-from-gitea) on the role's documentation for details.

## Related services

- [Forgejo Runner](forgejo-runner.md) — Runner to use with Forgejo Actions
- [Gitea](gitea.md) — Painless self-hosted [Git](https://git-scm.com/) service
- [Radicle node](radicle-node.md) — Network daemon for the [Radicle](https://radicle.xyz/) network, a peer-to-peer code collaboration stack built on Git
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
