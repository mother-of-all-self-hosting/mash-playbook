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

The playbook can install and configure [FileBrowser Quantum](https://filebrowserquantum.com/) for you.

FileBrowser Quantum is a free self-hosted web-based file manager.

See the project's [documentation](https://filebrowserquantum.com/en/docs/) to learn what FileBrowser Quantum does and why it might be useful to you.

For details about configuring the [Ansible role for FileBrowser Quantum](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az3ALGSKDhVLeMnR49YPXk5yv2yTge), you can check them via:
- 🌐 [the role's documentation](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az3ALGSKDhVLeMnR49YPXk5yv2yTge/tree/docs/configuring-filebrowser-quantum.md) online
- 📁 `roles/galaxy/filebrowser_quantum/docs/configuring-filebrowser-quantum.md` locally, if you have [fetched the Ansible roles](../installing.md)

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

### Set an administrator's password

By default the password authentication is enabled, and you need to set a log in password for the administrator by adding the following configuration to your `vars.yml` file:

```yaml
filebrowser_quantum_environment_variables_filebrowser_admin_password: YOUR_ADMIN_PASSWORD_HERE
```

Replace `YOUR_ADMIN_PASSWORD_HERE` with your own value.

### Configuring OIDC authentication (optional)

Alternatively, you can enable OIDC authentication for FileBrowser Quantum. See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az3ALGSKDhVLeMnR49YPXk5yv2yTge/tree/docs/configuring-filebrowser-quantum.md#configuring-oidc-authentication-optional) on the role's documentation for necessary settings.

## Usage

After running the command for installation, the FileBrowser Quantum instance becomes available at the URL specified with `filebrowser_quantum_hostname`. With the configuration above, the service is hosted at `https://filebrowser.example.com`.

To get started, open the URL with a web browser, and log in to the instance with the administrator account. The default username of the administrator account is `admin`.

## Troubleshooting

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az3ALGSKDhVLeMnR49YPXk5yv2yTge/tree/docs/configuring-filebrowser-quantum.md#troubleshooting) on the role's documentation for details.

## Related services

- [File Browser](filebrowser.md) — File managing interface within a specified directory, which can be used to upload, delete, preview and edit your files
