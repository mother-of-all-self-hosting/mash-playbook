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

# Excalidraw

The playbook can install and configure the [Excalidraw](https://excalidraw.com/) client for you.

Excalidraw is a free and open source virtual whiteboard for sketching hand-drawn like diagrams. It saves data locally on the browser, and the data is end-to-end encrypted.

See the project's [documentation](https://docs.excalidraw.com/) to learn what it does and why it might be useful to you.

For details about configuring the [Ansible role for the server](https://github.com/mother-of-all-self-hosting/ansible-role-excalidraw), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-excalidraw/blob/main/docs/configuring-excalidraw.md) online
- 📁 `roles/galaxy/excalidraw/docs/configuring-excalidraw.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# excalidraw                                                           #
#                                                                      #
########################################################################

excalidraw_enabled: true

excalidraw_hostname: excalidraw.example.com

########################################################################
#                                                                      #
# /excalidraw                                                          #
#                                                                      #
########################################################################
```

**Note**: hosting Excalidraw client under a subpath (by configuring the `excalidraw_path_prefix` variable) does not seem to be possible due to Excalidraw's technical limitations.

## Usage

After installation, the Excalidraw client becomes available at the URL specified with `excalidraw_hostname`.

### Enable a collaboration server (optional)

It is optionally possible to self-host an [example collaboration server](https://github.com/excalidraw/excalidraw-room) for your instance, which by default is configured to connect to the Excalidraw's server at `oss-collab.excalidraw.com`.

To set up the collaboration server with this playbook, see [this page](excalidraw-room.md) for the instruction.

>[!NOTE]
> By enabling the collaboration server along with the Excalidraw instance, the Docker image for the instance will be built instead of downloading it — This case there will be two images to be built; one for the Excalidraw instance and the other for the collaboration server itself.
>
> Before enabling it, make sure that the machine which you are going to run the Ansible commands against has sufficient computing power to build it.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-excalidraw/blob/main/docs/configuring-excalidraw.md#troubleshooting) on the role's documentation for details.

## Related services

- [Docmost](docmost.md) — Open-source collaborative wiki and documentation software
- [Excalidraw collaboration server](excalidraw-room.md) — Self-hosted collaboration server for Excalidraw instance
