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

The playbook can install and configure [Bar Assistant](https://github.com/karlomikus/bar-assistant/) for you.

Bar Assistant is a service for managing cocktail recipes at your home bar with a lot of cocktail-oriented features like ingredient substitutes. The playbook is configured to set up the Bar Assistant's API server and its web client software [Salt Rim](https://github.com/karlomikus/vue-salt-rim).

See the project's [documentation](https://docs.barassistant.app/) to learn what Bar Assistant does and why it might be useful to you.

For details about configuring the [Ansible role for Bar Assistant](https://codeberg.org/acioustick/ansible-role-barassistant), you can check them via:
- 🌐 [the role's documentation](https://codeberg.org/acioustick/ansible-role-barassistant/src/branch/master/docs/configuring-barassistant.md) online
- 📁 `roles/galaxy/barassistant/docs/configuring-barassistant.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

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
barassistant_server_environment_variables_allow_registration: false
```

### Connecting to a Meilisearch instance (optional)

To enable the search and filtering functions, you can optionally have the Bar Assistant instance connect to a Meilisearch instance.

Meilisearch is available on the playbook. Enabling it and setting the default admin API key automatically configures the Bar Assistant instance to connect to it.

See [this page](meilisearch.md) for details about how to install it and setting the key for the Meilisearch instance.

## Usage

After installation, the Bar Assistant's API server becomes available at the URL specified with `barassistant_hostname` and `barassistant_server_path_prefix`, and the Salt Rim instance becomes available at the URL specified with `barassistant_hostname`, respectively. With the configuration above, the Salt Rim instance is hosted at `https://barassistant.example.com`.

To get started, open the URL with a web browser, and register the account to use the web UI. **Note that the first registered user becomes an administrator automatically.**

Since account registration is disabled by default, you need to enable it first by setting `barassistant_server_environment_variables_allow_registration` to `false` temporarily in order to create your own account.

## Troubleshooting

See [this section](https://codeberg.org/acioustick/ansible-role-barassistant/src/branch/master/docs/configuring-barassistant.md#troubleshooting) on the role's documentation for details.
