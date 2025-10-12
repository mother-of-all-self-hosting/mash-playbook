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
SPDX-FileCopyrightText: 2024 Tiz
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Meilisearch

The playbook can install and configure [Meilisearch](https://www.meilisearch.com) for you.

Meilisearch is a typo-tolerant fulltext search engine like ElasticSearch with a RESTful search API.

See the project's [documentation](https://www.meilisearch.com/docs/learn/self_hosted/getting_started_with_self_hosted_meilisearch) to learn what Meilisearch does and why it might be useful to you.

For details about configuring the [Ansible role for Meilisearch](https://github.com/mother-of-all-self-hosting/ansible-role-meilisearch), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-meilisearch/blob/main/docs/configuring-meilisearch.md) online
- 📁 `roles/galaxy/meilisearch/docs/configuring-meilisearch.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- (optional) [Traefik](traefik.md) — a reverse-proxy server for exposing Meilisearch publicly

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# meilisearch                                                          #
#                                                                      #
########################################################################

meilisearch_enabled: true

########################################################################
#                                                                      #
# /meilisearch                                                         #
#                                                                      #
########################################################################
```

### Expose the instance publicly (optional)

By default, the Meilisearch instance is not exposed externally, as it is mainly intended to be used in the internal network.

To expose it publicly, add the following configuration to your `vars.yml` file (adapt to your needs):

```yaml
# The hostname at which Meilisearch is served.
meilisearch_hostname: "meilisearch.example.com"
```

**Note**: hosting Meilisearch under a subpath (by configuring the `meilisearch_path_prefix` variable) does not seem to be possible due to Meilisearch's technical limitations.

## Usage

After running the command for installation, Meilisearch becomes available internally to other services on the same network. If the service is exposed to the internet, it becomes available at the URL specified with `meilisearch_hostname`. With the configuration above, the service is hosted at `https://meilisearch.example.com`.

To get started, refer to [the documentation](https://www.meilisearch.com/docs/learn/getting_started/what_is_meilisearch) for guides about how to integrate Meilisearch.

### Obtaining API keys

**It is [not recommended](https://www.meilisearch.com/docs/learn/security/basic_security) to use the master key for operations anything but managing other API keys.** See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-meilisearch/blob/main/docs/configuring-meilisearch.md#obtaining-api-keys) about the instruction to obtain those API keys.

### Setting default API admin key

To let other services on the playbook use the Meilisearch instance, you can set the obtained default API admin key by adding the following configuration to your `vars.yml` file:

```yaml
meilisearch_default_admin_api_key: YOUR_DEFAULT_ADMIN_API_KEY_HERE
```

>[!NOTE]
> In most cases, the default Admin API Key is sufficient for services to use Meilisearch (reading and writing data). It is [not recommended](https://www.meilisearch.com/docs/learn/security/basic_security) to use the master key for operations anything but managing other API keys.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-meilisearch/blob/main/docs/configuring-meilisearch.md#troubleshooting) on the role's documentation for details.

## Related services

- [Typesense](typesense.md) — Fast and typo-tolerant fulltext search engine
