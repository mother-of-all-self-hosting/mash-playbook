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
SPDX-FileCopyrightText: 2024 Tiz
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Opengist

The playbook can install and configure [Opengist](https://opengist.io) for you.

Opengist is a self-hosted pastebin powered by Git. All snippets are stored in a Git repository and can be read and/or modified using standard Git commands, or with the web interface.

See the project's [documentation](https://opengist.io/docs/) to learn what Opengist does and why it might be useful to you.

For details about configuring the [Ansible role for Opengist](https://radicle.network/nodes/seed.radicle.garden/rad%3Az48WEbcYK3E6uDmfP1Qbb9AGdz1L3), you can check them via:

- 🌐 [the role's documentation](https://radicle.network/nodes/seed.radicle.garden/rad%3Az48WEbcYK3E6uDmfP1Qbb9AGdz1L3/tree/docs/configuring-opengist.md) online
- 📁 `roles/galaxy/opengist/docs/configuring-opengist.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server
- (optional) [Meilisearch](meilisearch.md)
- (optional) [Postgres](postgres.md) / MySQL / [MariaDB](mariadb.md) database — Opengist will default to [SQLite](https://www.sqlite.org/) if Postgres is not enabled

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# opengist                                                             #
#                                                                      #
########################################################################

opengist_enabled: true

opengist_hostname: opengist.example.com

########################################################################
#                                                                      #
# /opengist                                                            #
#                                                                      #
########################################################################
```

**Note**: hosting Opengist under a subpath (by configuring the `opengist_path_prefix` variable) does not seem to be possible due to Opengist's technical limitations.

### Set random 32-byte hex digits for secret key

You also need to set random **32-byte hex digits** for session store and encrypting MFA data on the database. To do so, add the following configuration to your `vars.yml` file. The value can be generated with `openssl rand -hex 32` or in another way.

```yaml
opengist_environment_variables_secret_key: YOUR_SECRET_KEY_HERE
```

>[!NOTE]
> Other type of values such as one generated with `pwgen -s 64 1` does not work.

### Select database to use (optional)

By default Opengist is configured to use Postgres, but you can choose other database such as SQLite and MySQL. See [this section](https://radicle.network/nodes/seed.radicle.garden/rad%3Az48WEbcYK3E6uDmfP1Qbb9AGdz1L3/tree/docs/configuring-opengist.md#specify-database-optional) on the role's documentation for details.

### Connecting to a Meilisearch instance (optional)

You can optionally have the Opengist instance connect to a Meilisearch instance as a code indexer.

Meilisearch is available on the playbook. Enabling it and setting its default admin API key (`meilisearch_default_admin_api_key`) automatically configures the Opengist instance to connect to it.

See [this page](meilisearch.md) for details about how to install it and setting the key for the Meilisearch instance.

### Integrating with Prometheus (optional)

Opengist can natively expose metrics to [Prometheus](prometheus.md).

#### Expose metrics internally

If Opengist and Prometheus do not share a network (like Traefik), you can connect the Opengist container network to Prometheus by adding the following configuration to your `vars.yml` file:

```yaml
prometheus_container_additional_networks_custom:
  - "{{ opengist_container_network }}"
```

#### Expose metrics publicly

If Opengist metrics are not scraped from a local Prometheus instance, you can expose the metrics publicly so that a remote instance can fetch them.

When exposing metrics publicly, you should consider to set up [HTTP Basic Authentication](https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication) **or anyone would be able to read your metrics**.

To expose the metrics publicly, add the following configuration to your `vars.yml` file (adapt to your needs):

```yaml
mash_playbook_metrics_exposure_enabled: true
mash_playbook_metrics_exposure_hostname: mash.example.com
```

It will expose the metrics at `https://mash.example.com/metrics/mash-opengist`.

To enable the HTTP Basic authentication, add the following configuration to your `vars.yml` file (adapt to your needs):

```yaml
opengist_container_labels_traefik_metrics_middleware_basic_auth_enabled: true

# See https://doc.traefik.io/traefik/middlewares/http/basicauth/#users for details.
opengist_container_labels_traefik_metrics_middleware_basic_auth_users: ""
```

## Usage

After running the command for installation, the Opengist instance becomes available at the URL specified with `opengist_hostname`. With the configuration above, the service is hosted at `https://opengist.example.com`.

To get started, open the URL with a web browser to create an account. **Note that the first registered user becomes an administrator automatically.**

See [this section](https://radicle.network/nodes/seed.radicle.garden/rad%3Az48WEbcYK3E6uDmfP1Qbb9AGdz1L3/tree/docs/configuring-opengist.md#configuring-ssh-feature-for-opengist-optional) on the role's documentation for details about how to set up the SSH feature.

## Troubleshooting

See [this section](https://radicle.network/nodes/seed.radicle.garden/rad%3Az48WEbcYK3E6uDmfP1Qbb9AGdz1L3/tree/docs/configuring-opengist.md#troubleshooting) on the role's documentation for details.

## Related services

- [PrivateBin](privatebin.md) — Minimalist, open source online pastebin where the server has zero knowledge of pasted data
