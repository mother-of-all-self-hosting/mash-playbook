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

The playbook can install and configure [Apprise API](https://github.com/caronc/apprise-api) for you.

[Apprise](https://github.com/caronc/apprise/) allows you to send a notification to almost all of the most popular notification services available to us today such as Matrix, Telegram, Discord, Slack, Amazon SNS, ntfy, Gotify, etc.

See the project's [documentation](https://github.com/caronc/apprise-api/blob/master/README.md) to learn what Apprise API does and why it might be useful to you.

For details about configuring the [Ansible role for Apprise API](https://codeberg.org/acioustick/ansible-role-apprise), you can check them via:
- 🌐 [the role's documentation](https://codeberg.org/acioustick/ansible-role-apprise/src/branch/master/docs/configuring-apprise.md) online
- 📁 `roles/galaxy/apprise/docs/configuring-apprise.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- (optional) [Traefik](traefik.md) — a reverse-proxy server for exposing Configuration Manager publicly

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

### Expose the Configuration Manager publicly (optional)

By default, the Apprise's built-in Configuration Manager where one can access and create configurations on the web browser is not exposed to the internet.

To expose it publicly, add the following configuration to your `vars.yml` file (adapt to your needs):

```yaml
# The hostname at which the Configuration Manager is served.
apprise_hostname: "apprise.example.com"
```

**Note**: hosting the Configuration Manager under a subpath (by configuring the `apprise_path_prefix` variable) does not seem to be possible due to Apprise's technical limitations.

## Usage

After running the command for installation, Apprise API becomes available. If the Configuration Manager is configured to be exposed to the internet, it becomes available at the URL specified with `apprise_hostname`. With the configuration above, it is hosted at `https://apprise.example.com`.

You can check the list of notification services supported by Apprise at <https://github.com/caronc/apprise/wiki#notification-services>. The instruction to use the Apprise CLI is available at <https://github.com/caronc/apprise/wiki/CLI_Usage>.

## Troubleshooting

See [this section](https://codeberg.org/acioustick/ansible-role-apprise/src/branch/master/docs/configuring-apprise.md#troubleshooting) on the role's documentation for details.

## Related services

- [Meilisearch](meilisearch.md) — Typo-tolerant fulltext search engine with a RESTful search API
