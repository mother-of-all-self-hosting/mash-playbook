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
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Mermaid Live Editor

The playbook can install and configure [Mermaid Live Editor](https://github.com/mermaid-js/mermaid-live-editor) for you.

Mermaid Live Editor is an online flow chart and diagrams editor.

See the project's [documentation](https://github.com/mermaid-js/mermaid-live-editor/blob/develop/README.md) to learn what Mermaid Live Editor does and why it might be useful to you.

For details about configuring the [Ansible role for Mermaid Live Editor](https://radicle.network/nodes/iris.radicle.network/rad%3Az2RAnfyxCYZSoUiDufyzTM7P3RvEd), you can check them via:

- 🌐 [the role's documentation](https://radicle.network/nodes/iris.radicle.network/rad%3Az2RAnfyxCYZSoUiDufyzTM7P3RvEd/tree/docs/configuring-mermaid.md) online
- 📁 `roles/galaxy/mermaid/docs/configuring-mermaid.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# mermaid                                                              #
#                                                                      #
########################################################################

mermaid_enabled: true

mermaid_hostname: mermaid.example.com

########################################################################
#                                                                      #
# /mermaid                                                             #
#                                                                      #
########################################################################
```

### Using the default Docker image (optional)

To have the service run as the playbook's default user instead of root user, this service is by default configured to use the Docker image locally built on [this own Dockerfile](https://radicle.network/nodes/iris.radicle.network/rad%3Az2RAnfyxCYZSoUiDufyzTM7P3RvEd/tree/templates/Dockerfile.j2).

If you prefer simply pulling and using [the official Docker image](https://github.com/-/mermaid-js/packages/container/package/mermaid-live-editor) instead, add the following configuration to your `vars.yml` file:

```yaml
mermaid_container_image_self_build: false
```

>[!NOTE]
> Adding the variable configures the playbook to run the service as a root user.

## Usage

After running the command for installation, the Mermaid Live Editor instance becomes available at the URL specified with `mermaid_hostname`. With the configuration above, the service is hosted at `https://mermaid.example.com`.

## Troubleshooting

See [this section](https://radicle.network/nodes/iris.radicle.network/rad%3Az2RAnfyxCYZSoUiDufyzTM7P3RvEd/tree/docs/configuring-mermaid.md#troubleshooting) on the role's documentation for details.

## Related services

- [Excalidraw](excalidraw.md) — Virtual whiteboard for sketching hand-drawn like diagrams
