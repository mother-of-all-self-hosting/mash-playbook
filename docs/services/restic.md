<!--
SPDX-FileCopyrightText: 2022 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2022 MDAD project contributors
SPDX-FileCopyrightText: 2022-2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2022-2025 Nikita Chernyi
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Restic

>[!WARNING]
> This service is a new addition to the playbook. It may not fully work or be configured in a suboptimal manner. It would be pretty appreciated if you could send a patch to the role to improve it!

The playbook can install and configure [restic](https://www.restic.org/) for you.

Restic is a fast and secure backup program.

The [Ansible role for restic](https://github.com/mother-of-all-self-hosting/ansible-role-restic) is developed and maintained by the MASH project. For details about configuring restic, you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-restic/blob/main/docs/configuring-restic.md) online
- 📁 `roles/galaxy/restic/docs/configuring-restic.md` locally, if you have [fetched the Ansible roles](../installing.md)

>[!NOTE]
>
> - Because the playbook is configured to create a backup of the whole MASH directory, you do not have to specify a directory to mount with `restic_container_additional_volumes_*`.
> - Backing up dumped database files requires additional settings.

## Related services

- [BorgBackup with borgmatic](backup-borg.md) — Deduplicating backup program with optional compression and encryption
- [Duplicati](duplicati.md) — Backup software that securely stores encrypted, incremental, compressed backups on local storage, cloud storage services and remote file servers
- [Rest Server](restserver.md) — HTTP server that implements restic's REST backend API to backup data remotely
