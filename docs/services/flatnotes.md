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

# flatnotes

The playbook can install and configure [flatnotes](https://flatnotes.io/) for you.

flatnotes is a database-less note taking web app that utilises a flat folder of markdown files for storage.

See the project's [documentation](https://github.com/dullage/flatnotes/wiki) to learn what flatnotes does and why it might be useful to you.

For details about configuring the [Ansible role for flatnotes](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az49LkutSMcaLA2DBazn1h4V6Pn6GK), you can check them via:
- 🌐 [the role's documentation](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az49LkutSMcaLA2DBazn1h4V6Pn6GK/tree/docs/configuring-flatnotes.md) online
- 📁 `roles/galaxy/flatnotes/docs/configuring-flatnotes.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# flatnotes                                                            #
#                                                                      #
########################################################################

flatnotes_enabled: true

flatnotes_hostname: flatnotes.example.com

########################################################################
#                                                                      #
# /flatnotes                                                           #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the flatnotes instance becomes available at the URL specified with `flatnotes_hostname`. With the configuration above, the service is hosted at `https://flatnotes.example.com`.

To get started, open the URL with a web browser to create an account.

## Troubleshooting

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az49LkutSMcaLA2DBazn1h4V6Pn6GK/tree/docs/configuring-flatnotes.md#troubleshooting) on the role's documentation for details.

## Related services

- [Memos](memos.md) — Markdown-native note-taking tool
- [SilverBullet](silverbullet.md) — Programmable, private, personal knowledge management platform
