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
SPDX-FileCopyrightText: 2023 - 2025 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# listmonk

The playbook can install and configure [listmonk](https://listmonk.app/) for you.

listmonk is a self-hosted, high performance one-way mailing list and newsletter manager.

See the project's [documentation](https://listmonk.app/docs/) to learn what listmonk does and why it might be useful to you.

For details about configuring the [Ansible role for listmonk](https://github.com/mother-of-all-self-hosting/ansible-role-listmonk), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-listmonk/blob/main/docs/configuring-listmonk.md) online
- 📁 `roles/galaxy/listmonk/docs/configuring-listmonk.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Postgres](postgres.md) database
- [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# listmonk                                                             #
#                                                                      #
########################################################################

listmonk_enabled: true

listmonk_hostname: listmonk.example.com

########################################################################
#                                                                      #
# /listmonk                                                            #
#                                                                      #
########################################################################
```

**Note**: hosting listmonk under a subpath does not seem to be possible due to listmonk's technical limitations.

## Usage

After running the command for installation, listmonk becomes available at the specified hostname like `https://listmonk.example.com`.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-listmonk/blob/main/docs/configuring-listmonk.md#troubleshooting) on the role's documentation for details.
