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

# Focalboard

The playbook can install and configure [Focalboard](https://www.focalboard.com/) for you.

Focalboard is an open source, self-hosted alternative to [Trello](https://trello.com/), [Notion](https://www.notion.so/), and [Asana](https://asana.com/).

See the project's [documentation](https://github.com/mattermost-community/focalboard/blob/main/README.md) to learn what Focalboard does and why it might be useful to you.

For details about configuring the [Ansible role for Focalboard](https://github.com/mother-of-all-self-hosting/ansible-role-focalboard), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-focalboard/blob/main/docs/configuring-focalboard.md) online
- 📁 `roles/galaxy/focalboard/docs/configuring-focalboard.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server
- (optional) a [Postgres](postgres.md) database — Focalboard will default to [SQLite](https://www.sqlite.org/) if Postgres is not enabled

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# focalboard                                                           #
#                                                                      #
########################################################################

focalboard_enabled: true

focalboard_hostname: mash.example.com
focalboard_path_prefix: /focalboard

########################################################################
#                                                                      #
# /focalboard                                                          #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the Focalboard instance becomes available at the URL specified with `focalboard_hostname` and `focalboard_path_prefix`. With the configuration above, the service is hosted at `https://mash.example.com/focalboard`.

You can open the page with a web browser to register the first (administrator) user. After the first user is created, an invitation link is required to sign up.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-focalboard/blob/main/docs/configuring-focalboard.md#troubleshooting) on the role's documentation for details.
