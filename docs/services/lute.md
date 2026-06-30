<!--
SPDX-FileCopyrightText: 2020 Aaron Raimist
SPDX-FileCopyrightText: 2020 Chris van Dijk
SPDX-FileCopyrightText: 2020 Dominik Zajac
SPDX-FileCopyrightText: 2020 Mickaël Cornière
SPDX-FileCopyrightText: 2020-2024 MDAD project contributors
SPDX-FileCopyrightText: 2020-2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2022 François Darveau
SPDX-FileCopyrightText: 2022 Julian Foad
SPDX-FileCopyrightText: 2022 Warren Bailey
SPDX-FileCopyrightText: 2023 Antonis Christofides
SPDX-FileCopyrightText: 2023 Felix Stupp
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 Thomas Miceli
SPDX-FileCopyrightText: 2024 Tiz
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Tasks.md

The playbook can install and configure [Tasks.md](https://hub.docker.com/r/baldissaramatheus/tasks.md) for you.

Tasks.md is a Markdown file-based task management board.

See the project's [documentation](https://hub.docker.com/r/baldissaramatheus/tasks.md) to learn what Tasks.md does and why it might be useful to you.

For details about configuring the [Ansible role for Tasks.md](https://radicle.network/nodes/iris.radicle.network/rad%3AzfFbFSPaygGqPEkWCTUGnzNwWNoT), you can check them via:

- 🌐 [the role's documentation](https://radicle.network/nodes/iris.radicle.network/rad%3AzfFbFSPaygGqPEkWCTUGnzNwWNoT/tree/docs/configuring-tasksmd.md) online
- 📁 `roles/galaxy/tasksmd/docs/configuring-tasksmd.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# tasks.md                                                             #
#                                                                      #
########################################################################

tasksmd_enabled: true

tasksmd_hostname: tasksmd.example.com

########################################################################
#                                                                      #
# /tasks.md                                                            #
#                                                                      #
########################################################################
```

### Configuring HTTP Basic authentication

The HTTP Basic authentication on Traefik is enabled for the web interface by default, considering the nature of the service. See [this section](https://radicle.network/nodes/iris.radicle.network/rad%3AzfFbFSPaygGqPEkWCTUGnzNwWNoT/tree/docs/configuring-tasksmd.md#configuring-http-basic-authentication) on the role's documentation for details about how to set it up or disable it.

## Usage

After running the command for installation, the Tasks.md instance becomes available at the hostname `mash-tasksmd`. Its web interface is hosted at `https://tasksmd.example.com`, with the configuration above.

## Troubleshooting

See [this section](https://radicle.network/nodes/iris.radicle.network/rad%3AzfFbFSPaygGqPEkWCTUGnzNwWNoT/tree/docs/configuring-tasksmd.md#troubleshooting) on the role's documentation for details.
