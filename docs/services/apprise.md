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

# Apprise API

The playbook can install and configure [Apprise API](https://apprise.org) for you.

Apprise API is a fast and typo-tolerant fulltext search engine like ElasticSearch.

See the project's [documentation](https://apprise.org/docs/) to learn what Apprise API does and why it might be useful to you.

For details about configuring the [Ansible role for Apprise API](https://github.com/mother-of-all-self-hosting/ansible-role-apprise), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-apprise/blob/main/docs/configuring-apprise.md) online
- 📁 `roles/galaxy/apprise/docs/configuring-apprise.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- (optional) [Traefik](traefik.md) — a reverse-proxy server for exposing Apprise API publicly

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# apprise                                                              #
#                                                                      #
########################################################################

apprise_enabled: true

########################################################################
#                                                                      #
# /apprise                                                             #
#                                                                      #
########################################################################
```

### Expose the instance publicly (optional)

By default, the Apprise API instance is not exposed externally, as it is mainly intended to be used in the internal network.

To expose it publicly, add the following configuration to your `vars.yml` file (adapt to your needs):

```yaml
# The hostname at which Apprise API is served.
apprise_hostname: "apprise.example.com"
```

**Note**: hosting Apprise API under a subpath (by configuring the `apprise_path_prefix` variable) does not seem to be possible due to Apprise API's technical limitations.

## Usage

After running the command for installation, Apprise API becomes available internally to other services on the same network. If the service is exposed to the internet, it becomes available at the URL specified with `apprise_hostname`. With the configuration above, the service is hosted at `https://apprise.example.com`.

To get started, refer to [the documentation](https://apprise.org/docs/guide/) for guides about how to integrate Apprise API.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-apprise/blob/main/docs/configuring-apprise.md#troubleshooting) on the role's documentation for details.

## Related services

- [Meilisearch](meilisearch.md) — Typo-tolerant fulltext search engine with a RESTful search API
