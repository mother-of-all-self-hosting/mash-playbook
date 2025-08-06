<!--
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2024 Slavi Pantaleev

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Plausible Analytics

[Plausible Analytics](https://plausible.io/) is intuitive, lightweight and open source web analytics. No cookies and fully compliant with GDPR, CCPA and PECR.

With this playbook, you can install the [Community Edition](https://plausible.io/blog/community-edition) of Plausible Analytics.


## Dependencies

This service requires the following other services:

- a [Postgres](postgres.md) database
- a [ClickHouse](clickhouse.md) database
- a [Traefik](traefik.md) reverse-proxy server
- (optional) the [exim-relay](exim-relay.md) mailer


## Configuration

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

In the example configuration above, we configure the service to be hosted at `https://plausible.example.com`.

The Ansible role for Plausible Analytics contains a `plausible_path_prefix` variable for hosting at a subdirectory, but this is not implemented yet. See the comments about `plausible_path_prefix` in [ansible-role-plausible](https://github.com/mother-of-all-self-hosting/ansible-role-plausible)'s `defaults/main.yml` file.


## Usage

After [installation](../installing.md), you should be able to access your new Plausible Analytics instance at the URL you've chosen.

You should then be able to create your first user account, which will be created as an admin (see the details about `plausible_environment_variable_admin_user_ids` above).

After logging in with your user account you can create properties (websites) and invite other users by email.
By default, the system is configured to allow registrations that are coming from an explicit invitation, while public registrations are disabled. This can be controlled via the `plausible_environment_variable_disable_registration` variable.

For additional configuration options, refer to [ansible-role-plausible](https://github.com/mother-of-all-self-hosting/ansible-role-plausible)'s `defaults/main.yml` file.

## Related services

- [OxiTraffic](oxitraffic.md) — Self-hosted, simple and privacy respecting website traffic tracker
