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
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Send

The playbook can install and configure [Send](https://github.com/timvisee/send) for you.

Send is a fork of Mozilla's discontinued [Firefox Send](https://github.com/mozilla/send) which allows you to send files to others with a link. Files are end-to-end encrypted so they cannot be read by the server, and also can be protected with a password.

See the project's [documentation](https://github.com/timvisee/send/blob/master/README.md) to learn what Send does and why it might be useful to you.

For details about configuring the [Ansible role for Send](https://codeberg.org/acioustick/ansible-role-send), you can check them via:
- 🌐 [the role's documentation](https://codeberg.org/acioustick/ansible-role-send/src/branch/master/docs/configuring-send.md) online
- 📁 `roles/galaxy/send/docs/configuring-send.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server
- [Valkey](valkey.md) data-store

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# send                                                                 #
#                                                                      #
########################################################################

send_enabled: true

send_hostname: send.example.com

########################################################################
#                                                                      #
# send                                                                 #
#                                                                      #
########################################################################
```

**Note**: hosting Send under a subpath (by configuring the `send_path_prefix` variable) does not seem to be possible due to Send's technical limitations.

## Usage

To configure and manage the Send, go to `mash.example.com/joplin/login` specified with `send_hostname` and `send_path_prefix`, enter the admin credentials (email address: `admin@localhost`, password: `admin`) to log in. **After logging in, make sure to change the credentials.**

For security reason, the developer recommends to create a non-admin user for synchronization. You can create one on the "Users" page. After creating, you can use the email and password you specified for the user to synchronize data with your Send clients.

See [this section](https://codeberg.org/acioustick/ansible-role-send/src/branch/master/docs/configuring-send.md#usage) on the role's documentation for details about configuring the Send and the client application.

## Troubleshooting

See [this section](https://codeberg.org/acioustick/ansible-role-send/src/branch/master/docs/configuring-send.md#troubleshooting) on the role's documentation for details.
