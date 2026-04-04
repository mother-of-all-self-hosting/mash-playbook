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

# Memos

The playbook can install and configure [Memos](https://usememos.com/) for you.

Memos is a Markdown-native note-taking tool.

See the project's [documentation](https://usememos.com/docs) to learn what Memos does and why it might be useful to you.

For details about configuring the [Ansible role for Memos](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az2UFFCDXMH6Am1K99TaiYP8BJmqaj), you can check them via:
- 🌐 [the role's documentation](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az2UFFCDXMH6Am1K99TaiYP8BJmqaj/tree/docs/configuring-memos.md) online
- 📁 `roles/galaxy/memos/docs/configuring-memos.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Postgres](postgres.md) / MySQL / [MariaDB](mariadb.md) / [SQLite](https://www.sqlite.org/) database
- [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# memos                                                                #
#                                                                      #
########################################################################

memos_enabled: true

memos_hostname: memos.example.com

########################################################################
#                                                                      #
# /memos                                                               #
#                                                                      #
########################################################################
```

**Note**: hosting Memos under a subpath (by configuring the `memos_path_prefix` variable) does not seem to be possible due to Memos's technical limitations.

### Select database to use

It is necessary to select a database used by Memos from a MySQL compatible database, Postgres, and SQLite. See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az2UFFCDXMH6Am1K99TaiYP8BJmqaj/tree/docs/configuring-memos.md#specify-database) on the role's documentation for details.

## Usage

After running the command for installation, the Memos instance becomes available at the URL specified with `memos_hostname`. With the configuration above, the service is hosted at `https://memos.example.com`.

To get started, open the URL with a web browser, and register the account.

## Troubleshooting

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az2UFFCDXMH6Am1K99TaiYP8BJmqaj/tree/docs/configuring-memos.md#troubleshooting) on the role's documentation for details.

## Related services

- [flatnotes](flatnotes.md) — Database-less note taking web app that utilises a flat folder of markdown files for storage
