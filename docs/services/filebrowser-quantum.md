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

# FileBrowser Quantum

The playbook can install and configure [FileBrowser Quantum](https://filebrowser.org/) for you.

FileBrowser Quantum provides a file managing interface within a specified directory and it can be used to upload, delete, preview and edit your files.

See the project's [documentation](https://filebrowser.org/) to learn what FileBrowser Quantum does and why it might be useful to you.

For details about configuring the [Ansible role for FileBrowser Quantum](https://codeberg.org/acioustick/ansible-role-filebrowser), you can check them via:
- 🌐 [the role's documentation](https://codeberg.org/acioustick/ansible-role-filebrowser/src/branch/master/docs/configuring-filebrowser.md) online
- 📁 `roles/galaxy/filebrowser/docs/configuring-filebrowser.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# filebrowser_quantum                                                  #
#                                                                      #
########################################################################

filebrowser_quantum_enabled: true

filebrowser_quantum_hostname: filebrowser.example.com

########################################################################
#                                                                      #
# /filebrowser_quantum                                                 #
#                                                                      #
########################################################################
```

**Note**: hosting FileBrowser Quantum under a subpath (by configuring the `filebrowser_quantum_path_prefix` variable) does not seem to be possible due to FileBrowser Quantum's technical limitations.

## Usage

After running the command for installation, the FileBrowser Quantum instance becomes available at the URL specified with `filebrowser_quantum_hostname`. With the configuration above, the service is hosted at `https://filebrowser.example.com`.

To get started, open the URL with a web browser, and log in to the instance with the administrator account (`admin`).

The initial password of the administrator has been logged to the console logs during the first run.

You can check it directly by logging in to the server with SSH and running `journalctl -fu filebrowser` (or how you/your playbook named the service, e.g. `mash-filebrowser`). You also can use the command below to check the line on the log to find the initial password:

```sh
ansible-playbook -i inventory/hosts setup.yml --tags=check-initial-password-filebrowser
```

You can create additional users (admin-privileged or not) after logging in via the web frontend.

## Troubleshooting

See [this section](https://codeberg.org/acioustick/ansible-role-filebrowser/src/branch/master/docs/configuring-filebrowser.md#troubleshooting) on the role's documentation for details.
