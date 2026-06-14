<!--
SPDX-FileCopyrightText: 2020 - 2024 MDAD project contributors
SPDX-FileCopyrightText: 2020 - 2025 Slavi Pantaleev
SPDX-FileCopyrightText: 2020 Aaron Raimist
SPDX-FileCopyrightText: 2020 Chris van Dijk
SPDX-FileCopyrightText: 2020 Dominik Zajac
SPDX-FileCopyrightText: 2020 Mickaël Cornière
SPDX-FileCopyrightText: 2022 François Darveau
SPDX-FileCopyrightText: 2022 Julian Foad
SPDX-FileCopyrightText: 2022 Warren Bailey
SPDX-FileCopyrightText: 2023 - 2024 MASH project contributors
SPDX-FileCopyrightText: 2023 Antonis Christofides
SPDX-FileCopyrightText: 2023 Felix Stupp
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 Gergely Horváth
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara
SPDX-FileCopyrightText: 2024 Philipp Homann

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# FileGator

The playbook can install and configure [FileGator](https://filegator.io/) for you.

FileGator is a free self-hosted web-based file manager.

See the project's [documentation](https://docs.filegator.io/) to learn what FileGator does and why it might be useful to you.

For details about configuring the [Ansible role for FileGator](https://radicle.network/nodes/iris.radicle.network/rad%3AzBuFgpA5FBmUEcLEXHY9ZBVGpqDM), you can check them via:

- 🌐 [the role's documentation](https://radicle.network/nodes/iris.radicle.network/rad%3AzBuFgpA5FBmUEcLEXHY9ZBVGpqDM/tree/docs/configuring-filegator.md) online
- 📁 `roles/galaxy/filegator/docs/configuring-filegator.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# filegator                                                            #
#                                                                      #
########################################################################

filegator_enabled: true

filegator_hostname: filegator.example.com

########################################################################
#                                                                      #
# /filegator                                                           #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the FileGator instance becomes available at the URL specified with `filegator_hostname`. With the configuration above, the service is hosted at `https://filegator.example.com`.

To get started, open the URL with a web browser, and log in to the instance with the administrator account credentials. The default login credentials can be checked at <https://github.com/filegator/filegator/blob/master/README.md>. **After logging in, make sure to change the credentials.**

## Troubleshooting

See [this section](https://radicle.network/nodes/iris.radicle.network/rad%3AzBuFgpA5FBmUEcLEXHY9ZBVGpqDM/tree/docs/configuring-filegator.md#troubleshooting) on the role's documentation for details.

## Related services

- [File Browser](filebrowser.md) — Web-based file manager
- [FileBrowser Quantum](filebrowser-quantum.md) — Web-based file manager
