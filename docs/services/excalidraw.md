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

>[!NOTE]
> At the moment, self-hosting your own instance doesn't support sharing or collaboration features (see [here](https://docs.excalidraw.com/docs/introduction/development#self-hosting)).

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-excalidraw/blob/main/docs/configuring-excalidraw.md#troubleshooting) on the role's documentation for details.
