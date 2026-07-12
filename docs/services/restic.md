<!--
SPDX-FileCopyrightText: 2022 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2022 MDAD project contributors
SPDX-FileCopyrightText: 2022-2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2022-2025 Nikita Chernyi
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Restic

The playbook can install and configure [restic](https://www.restic.org/) (short: restic) with [borgmatic](https://torsion.org/borgmatic/) for you.

restic is a deduplicating backup program with optional compression and encryption. That means your daily incremental backups can be stored in a fraction of the space and is safe whether you store it at home or on a cloud service.

The [Ansible role for restic](https://github.com/mother-of-all-self-hosting/ansible-role-restic) is developed and maintained by the MASH project. For details about configuring restic, you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-restic/blob/main/docs/configuring-restic.md) online
- 📁 `roles/galaxy/restic/docs/configuring-restic.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Related services

- [restic Web UI](borg-ui.md) — Unofficial web interface for restic
- [Duplicati](duplicati.md) — Backup software that securely stores encrypted, incremental, compressed backups on local storage, cloud storage services and remote file servers
- [Rest Server](restserver.md) — HTTP server that implements restic's REST backend API to backup data remotely
