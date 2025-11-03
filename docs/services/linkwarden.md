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

# Linkwarden

The playbook can install and configure [Linkwarden](https://github.com/linkwarden/linkwarden/) for you.

Linkwarden is a self-hosted, open-source collaborative bookmark manager to collect, organize and archive webpages.

See the project's [documentation](https://docs.linkwarden.app) to learn what Linkwarden does and why it might be useful to you.

For details about configuring the [Ansible role for Linkwarden](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3AzCF75tYyujYQ3T4L3BkBDrPzXree), you can check them via:
- 🌐 [the role's documentation](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3AzCF75tYyujYQ3T4L3BkBDrPzXree/tree/docs/configuring-linkwarden.md) online
- 📁 `roles/galaxy/linkwarden/docs/configuring-linkwarden.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Postgres](postgres.md) database
- [Traefik](traefik.md) reverse-proxy server
- (optional) [Meilisearch](meilisearch.md)

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# linkwarden                                                           #
#                                                                      #
########################################################################

linkwarden_enabled: true

linkwarden_hostname: linkwarden.example.com

########################################################################
#                                                                      #
# /linkwarden                                                          #
#                                                                      #
########################################################################
```

**Note**: hosting Linkwarden under a subpath (by configuring the `linkwarden_path_prefix` variable) does not seem to be possible due to Linkwarden's technical limitations.

### Enabling signing up

By default account registration for the service is disabled. To enable it, add the following configuration to your `vars.yml` file:

```yaml
linkwarden_environment_variables_next_public_disable_registration: false
```

### Connecting to a Meilisearch instance (optional)

To enable the [advanced search options](https://docs.linkwarden.app/Usage/advanced-search), you can optionally have the Linkwarden instance connect to a Meilisearch instance.

Meilisearch is available on the playbook. Enabling it and setting its default admin API key automatically configures the Linkwarden instance to connect to it.

See [this page](meilisearch.md) for details about how to install it and setting the key for the Meilisearch instance.

## Usage

After installation, the Linkwarden instance becomes available at the URL specified with `linkwarden_hostname`. With the configuration above, the service is hosted at `https://linkwarden.example.com`.

To get started, open the URL with a web browser, and register the account. **Note that the first registered user becomes an administrator automatically.**

Since account registration is disabled by default, you need to enable it first by setting `linkwarden_environment_variables_next_public_disable_registration` to `false` temporarily in order to create your own account.

## Troubleshooting

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3AzCF75tYyujYQ3T4L3BkBDrPzXree/tree/docs/configuring-linkwarden.md#troubleshooting) on the role's documentation for details.

## Related services

- [Karakeep](karakeep.md) — Self-hosted, open-source bookmark manager to collect, organize and archive webpages
- [linkding](linkding.md) — Bookmark manager designed to be minimal and fast
- [Readeck](readeck.md) — Bookmark manager and a read-later tool combined in one
