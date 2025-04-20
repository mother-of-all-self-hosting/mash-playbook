<!--
SPDX-FileCopyrightText: 2021 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2021 Béla Becker
SPDX-FileCopyrightText: 2021 pushytoxin
SPDX-FileCopyrightText: 2022 Jim Myhrberg
SPDX-FileCopyrightText: 2022 Nikita Chernyi
SPDX-FileCopyrightText: 2022 felixx9
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Etherpad

The playbook can install and configure [Etherpad](https://etherpad.org), an open source collaborative text editor, for you.

The [Ansible role for Etherpad](https://github.com/mother-of-all-self-hosting/ansible-role-etherpad) is developed and maintained by the MASH project. For details about configuring Etherpad, you can check them via:

- 🌐 [the role's documentation at the MASH project](https://github.com/mother-of-all-self-hosting/ansible-role-etherpad/blob/main/docs/configuring-etherpad.md) online
- 📁 `roles/galaxy/etherpad/docs/configuring-etherpad.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- a [Postgres](postgres.md) database
- a [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# etherpad                                                             #
#                                                                      #
########################################################################

etherpad_enabled: true

etherpad_hostname: etherpad.example.com

########################################################################
#                                                                      #
# /etherpad                                                            #
#                                                                      #
########################################################################
```

As the most of the necessary settings for the role have been taken care of by the playbook, you can enable Etherpad on your server with this minimum configuration.

See the role's documentation for details about configuring Etherpad per your preference (such as [the name of the instance](https://github.com/mother-of-all-self-hosting/ansible-role-etherpad/blob/main/docs/configuring-etherpad.md#set-the-name-of-the-instance-optional) and [the default pad text](https://github.com/mother-of-all-self-hosting/ansible-role-etherpad/blob/main/docs/configuring-etherpad.md#set-the-default-text-optional)).

### Create admin user (optional)

You probably might want to enable authentication to disallow anonymous access to your Etherpad.

It is possible to enable HTTP basic authentication by **creating an admin user** with `etherpad_admin_username` and `etherpad_admin_password` variables. The admin user account is also used by plugins for authentication and authorization.

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-etherpad/blob/main/docs/configuring-etherpad.md#create-admin-user-optional) on the role's documentation for details about how to create the admin user.

### Control Etherpad's availability on Jitsi conferences (optional)

If a Jitsi video-conferencing platform (see [our docs on Jitsi](jitsi.md)) is enabled on your server, you can configure it so to make Etherpad available on conferences.

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-jitsi/blob/main/docs/configuring-jitsi.md#control-etherpads-availability-on-jitsi-conferences) on the Jitsi role's documentation for details about how to set it up.

## Usage

By default, the Etherpad UI should be available at `https://etherpad.example.com`, while the admin UI (if enabled) should then be available at `https://etherpad.example.com/admin`.

💡 For more information about usage, take a look at [this section](https://github.com/mother-of-all-self-hosting/ansible-role-etherpad/blob/main/docs/configuring-etherpad.md#usage) on the role's documentation.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-etherpad/blob/main/docs/configuring-etherpad.md#troubleshooting) on the role's documentation for details.
