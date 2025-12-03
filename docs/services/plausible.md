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

# Plausible Analytics

The playbook can install and configure [Plausible Analytics](https://plausible.io/) for you.

Plausible Analytics is intuitive, lightweight and open source web analytics. No cookies and fully compliant with GDPR, CCPA and PECR. With this playbook, you can install the [Community Edition](https://plausible.io/blog/community-edition) of Plausible Analytics.

See the project's [documentation](https://plausible.io/docs) to learn what Plausible Analytics does and why it might be useful to you.

## Dependencies

This service requires the following other services:

- a [ClickHouse](clickhouse.md) database
- a [Postgres](postgres.md) database
- a [Traefik](traefik.md) reverse-proxy server
- (optional) the [exim-relay](exim-relay.md) mailer

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# plausible                                                            #
#                                                                      #
########################################################################

plausible_enabled: true

plausible_hostname: plausible.example.com

# Generate this with: `openssl rand -base64 48`
plausible_environment_variable_secret_key_base: ''

# Generate this with: `openssl rand -base64 32`
plausible_environment_variable_totp_vault_key: ''

# Controls which user ids will be system admins
# By default, only the first user (`1`) to be registered will be made an admin.
# plausible_environment_variable_admin_user_ids: '1,2,3'

########################################################################
#                                                                      #
# /plausible                                                           #
#                                                                      #
########################################################################
```

**Note**: hosting Plausible Analytics under a subpath (by configuring the `plausible_path_prefix` variable) does not seem to be possible due to Plausible Analytics' technical limitations.

## Usage

After running the command for installation, the Plausible Analytics instance becomes available at the URL specified with `plausible_hostname`. With the configuration above, the service is hosted at `https://plausible.example.com`.

First, create your first user account, which will be created as an admin (see the details about `plausible_environment_variable_admin_user_ids` above).

After logging in with your user account you can create properties (websites) and invite other users by email. By default, the system is configured to allow registrations that are coming from an explicit invitation, while public registrations are disabled. This can be controlled via the `plausible_environment_variable_disable_registration` variable.

For additional configuration options, refer to [ansible-role-plausible](https://github.com/mother-of-all-self-hosting/ansible-role-plausible)'s `defaults/main.yml` file.

## Related services

- [Matomo](matomo.md) — Free and open source web analytics platform
- [OxiTraffic](oxitraffic.md) — Self-hosted, simple and privacy respecting website traffic tracker
