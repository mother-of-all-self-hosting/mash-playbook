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

# Karakeep

The playbook can install and configure [Karakeep](https://karakeep.app/) for you.

Karakeep is a self-hosted, open-source bookmark manager to collect, organize and archive webpages, enabling LLM providers to add tags to them automatically.

See the project's [documentation](https://docs.karakeep.app) to learn what Karakeep does and why it might be useful to you.

For details about configuring the [Ansible role for Karakeep](https://codeberg.org/acioustick/ansible-role-karakeep), you can check them via:
- 🌐 [the role's documentation](https://codeberg.org/acioustick/ansible-role-karakeep/src/branch/master/docs/configuring-karakeep.md) online
- 📁 `roles/galaxy/karakeep/docs/configuring-karakeep.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server
- (optional) [Browserless](browserless.md) — required for the screenshot function
- (optional) [Meilisearch](meilisearch.md) — required for the search function

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# karakeep                                                             #
#                                                                      #
########################################################################

karakeep_enabled: true

karakeep_hostname: karakeep.example.com

########################################################################
#                                                                      #
# /karakeep                                                            #
#                                                                      #
########################################################################
```

**Note**: hosting Karakeep under a subpath (by configuring the `karakeep_path_prefix` variable) does not seem to be possible due to Karakeep's technical limitations.

### Enabling signing up

By default account registration for the service is disabled. To enable it, add the following configuration to your `vars.yml` file:

```yaml
karakeep_environment_variables_disable_signups: false
```

### Connecting to a Browserless instance (optional)

To enable the screenshot function with JavaScript execution allowed, you can optionally have the Karakeep instance connect to a Browserless instance.

Browserless is available on the playbook. Enabling it automatically configures the Karakeep instance to connect to it.

See [this page](browserless.md) for details about how to install it.

### Connecting to a Meilisearch instance (optional)

To enable the search function, you can optionally have the Karakeep instance connect to a Meilisearch instance.

Meilisearch is available on the playbook. Enabling it and setting its default admin API key automatically configures the Karakeep instance to connect to it.

See [this page](meilisearch.md) for details about how to install it and setting the key for the Meilisearch instance.

### Extending the configuration

See [this page](https://docs.karakeep.app/configuration/) for a complete list of Karakeep's config options that you could put in `karakeep_environment_variables_additional_variables`.

>[!NOTE]
> Enabling automatic tagging with LLM providers requires environment variables to be specified manually. See [this section](https://docs.karakeep.app/configuration/#inference-configs-for-automatic-tagging) on the documentation for details.

## Usage

After installation, the Karakeep instance becomes available at the URL specified with `karakeep_hostname`. With the configuration above, the service is hosted at `https://karakeep.example.com`.

To get started, open the URL with a web browser, and register the account. **Note that the first registered user becomes an administrator automatically.**

Since account registration is disabled by default, you need to enable it first by setting `karakeep_environment_variables_disable_signups` to `false` temporarily in order to create your own account.

## Troubleshooting

See [this section](https://codeberg.org/acioustick/ansible-role-karakeep/src/branch/master/docs/configuring-karakeep.md#troubleshooting) on the role's documentation for details.

## Related services

- [linkding](linkding.md) — Bookmark manager designed to be minimal and fast
- [Linkwarden](linkwarden.md) — Self-hosted, open-source collaborative bookmark manager to collect, organize and archive webpages
- [Readeck](readeck.md) — Bookmark manager and a read-later tool combined in one
