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

# Excalidraw collaboration server

The playbook can install and configure an [example collaboration server](https://github.com/excalidraw/excalidraw-room) for [Excalidraw](https://excalidraw.com/) for you.

It enables to self-host the collaboration server for your Excalidraw's instance, which by default is configured to connect to the Excalidraw's server at `oss-collab.excalidraw.com`.

See the project's [documentation](https://github.com/excalidraw/excalidraw-room/blob/master/README.md) to learn what it does and why it might be useful to you.

For details about configuring the [Ansible role for the server](https://github.com/mother-of-all-self-hosting/ansible-role-excalidraw-room), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-excalidraw-room/blob/main/docs/configuring-excalidraw-room.md) online
- 📁 `roles/galaxy/excalidraw_room/docs/configuring-excalidraw-room.md` locally, if you have [fetched the Ansible roles](../installing.md)

>[!NOTE]
> The role is configured to build the Docker image by default, as it is not provided by the upstream project. Before proceeding, make sure that the machine which you are going to run the Ansible commands against has sufficient computing power to build it.

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# excalidraw_room                                                      #
#                                                                      #
########################################################################

excalidraw_room_enabled: true

excalidraw_room_hostname: "excalidraw-room.example.com"

########################################################################
#                                                                      #
# /excalidraw_room                                                     #
#                                                                      #
########################################################################
```

**Note**: hosting Excalidraw collaboration server client under a subpath (by configuring the `excalidraw_room_path_prefix` variable) does not seem to be possible due to Excalidraw collaboration server's technical limitations.

## Usage

After installation, the Excalidraw collaboration server becomes available at the URL specified with `excalidraw_room_hostname`.

To use the collaboration server, you need to set up an Excalidraw instance built for the collaboration server. See [this page](excalidraw.md) for the instruction to set up the instance with this playbook.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-excalidraw-room/blob/main/docs/configuring-excalidraw-room.md#troubleshooting) on the role's documentation for details.

## Related services

- [Excalidraw](excalidraw.md) — Free and open source virtual whiteboard for sketching hand-drawn like diagrams
