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

# Bar Assistant

The playbook can install and configure [Bar Assistant](https://github.com/barassistant/barassistant/) for you.

Bar Assistant is a self-hosted, open-source collaborative bookmark manager to collect, organize and archive webpages.

See the project's [documentation](https://docs.barassistant.app) to learn what Bar Assistant does and why it might be useful to you.

For details about configuring the [Ansible role for Bar Assistant](https://codeberg.org/acioustick/ansible-role-barassistant), you can check them via:
- 🌐 [the role's documentation](https://codeberg.org/acioustick/ansible-role-barassistant/src/branch/master/docs/configuring-barassistant.md) online
- 📁 `roles/galaxy/barassistant/docs/configuring-barassistant.md` locally, if you have [fetched the Ansible roles](../installing.md)

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
# barassistant                                                         #
#                                                                      #
########################################################################

barassistant_enabled: true

barassistant_hostname: barassistant.example.com

########################################################################
#                                                                      #
# /barassistant                                                        #
#                                                                      #
########################################################################
```

**Note**: hosting Bar Assistant under a subpath (by configuring the `barassistant_path_prefix` variable) does not seem to be possible due to Bar Assistant's technical limitations.

### Enabling signing up

By default account registration for the service is disabled. To enable it, add the following configuration to your `vars.yml` file:

```yaml
barassistant_environment_variables_next_public_disable_registration: false
```

### Connecting to a Meilisearch instance (optional)

To enable the [advanced search options](https://docs.barassistant.app/Usage/advanced-search), you can optionally have the Bar Assistant instance connect to a Meilisearch instance by adding the following configuration to your `vars.yml` file:

```yaml
barassistant_environment_variables_meili_key: YOUR_MEILISEARCH_KEY_HERE
```

Meilisearch is available on the playbook. See [this page](meilisearch.md) for details about how to install it.

>[!NOTE]
> The default Admin API Key is sufficient for using Meilisearch on a Bar Assistant instance. It is [not recommended](https://www.meilisearch.com/docs/learn/security/basic_security) to use the master key for operations anything but managing other API keys.

## Usage

After installation, the Bar Assistant instance becomes available at the URL specified with `barassistant_hostname`. With the configuration above, the service is hosted at `https://barassistant.example.com`.

To get started, open the URL with a web browser, and register the account. **Note that the first registered user becomes an administrator automatically.**

Since account registration is disabled by default, you need to enable it first by setting `barassistant_environment_variables_next_public_disable_registration` to `false` temporarily in order to create your own account.

## Troubleshooting

See [this section](https://codeberg.org/acioustick/ansible-role-barassistant/src/branch/master/docs/configuring-barassistant.md#troubleshooting) on the role's documentation for details.

## Related services

- [linkding](linkding.md) — Bookmark manager designed to be minimal and fast
- [Readeck](readeck.md) — Bookmark manager and a read-later tool combined in one
