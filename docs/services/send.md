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

The playbook can install and configure [Send](https://joplinapp.org/help/dev/spec/architecture#send) for you.

Send is a self-hosted server component for [Send](https://joplinapp.org/) — a privacy-focused note taking and to-do application, which can handle a large number of notes organized into notebooks.

While Send is architectured to be "offline first", with a Send it is able to not only synchronize data among devices but also [share a notebook](https://joplinapp.org/help/apps/share_notebook/) with users and [publish a note](https://joplinapp.org/help/apps/publish_note/) on the internet to share it with anyone.

See the project's [documentation](https://joplinapp.org/help/) to learn what Send and Send do and why they might be useful to you.

For details about configuring the [Ansible role for Send](https://codeberg.org/acioustick/ansible-role-send), you can check them via:
- 🌐 [the role's documentation](https://codeberg.org/acioustick/ansible-role-send/src/branch/master/docs/configuring-send.md) online
- 📁 `roles/galaxy/send/docs/configuring-send.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Postgres](postgres.md) database
- [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# send                                                                 #
#                                                                      #
########################################################################

send_enabled: true

send_hostname: mash.example.com
send_path_prefix: /joplin

########################################################################
#                                                                      #
# send                                                                 #
#                                                                      #
########################################################################
```

As the most of the necessary settings for the role have been taken care of by the playbook, you can enable Send on your server with this minimum configuration.

## Usage

To configure and manage the Send, go to `mash.example.com/joplin/login` specified with `send_hostname` and `send_path_prefix`, enter the admin credentials (email address: `admin@localhost`, password: `admin`) to log in. **After logging in, make sure to change the credentials.**

For security reason, the developer recommends to create a non-admin user for synchronization. You can create one on the "Users" page. After creating, you can use the email and password you specified for the user to synchronize data with your Send clients.

See [this section](https://codeberg.org/acioustick/ansible-role-send/src/branch/master/docs/configuring-send.md#usage) on the role's documentation for details about configuring the Send and the client application.

## Troubleshooting

See [this section](https://codeberg.org/acioustick/ansible-role-send/src/branch/master/docs/configuring-send.md#troubleshooting) on the role's documentation for details.
