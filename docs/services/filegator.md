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

The playbook can install and configure [FileGator](https://filegator.org/) for you.

FileGator is a free self-hosted web-based file manager.

See the project's [documentation](https://filegator.org/) to learn what FileGator does and why it might be useful to you.

For details about configuring the [Ansible role for FileGator](https://radicle.network/nodes/iris.radicle.network/rad%3Az318zbpe2RNjFqVzXqPoDDJvvohbw), you can check them via:

- 🌐 [the role's documentation](https://radicle.network/nodes/iris.radicle.network/rad%3Az318zbpe2RNjFqVzXqPoDDJvvohbw/tree/docs/configuring-filegator.md) online
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

**Note**: hosting FileGator under a subpath (by configuring the `filegator_path_prefix` variable) does not seem to be possible due to FileGator's technical limitations.

## Usage

After running the command for installation, the FileGator instance becomes available at the URL specified with `filegator_hostname`. With the configuration above, the service is hosted at `https://filegator.example.com`.

To get started, open the URL with a web browser to log in to the instance with the administrator account (`admin`).

The initial password of the administrator has been logged to the console logs during the first run.

You can check it directly by logging in to the server with SSH and running `journalctl -fu filegator` (or how you/your playbook named the service, e.g. `mash-filegator`). You also can use the command below to check the line on the log to find the initial password:

```sh
ansible-playbook -i inventory/hosts setup.yml --tags=check-initial-password-filegator
```

You can create additional users (admin-privileged or not) after logging in via the web frontend.

## Troubleshooting

See [this section](https://radicle.network/nodes/iris.radicle.network/rad%3Az318zbpe2RNjFqVzXqPoDDJvvohbw/tree/docs/configuring-filegator.md#troubleshooting) on the role's documentation for details.

## Related services

- [FileBrowser Quantum](filegator-quantum.md) — Web-based file manager
