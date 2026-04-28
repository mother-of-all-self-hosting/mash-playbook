<!--
SPDX-FileCopyrightText: 2021 foxcris
SPDX-FileCopyrightText: 2021-2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Gotenberg

The playbook can install and configure [Gotenberg](https://gotenberg.dev/) for you.

Gotenberg is a Docker-based API for converting documents to PDF.

The [Ansible role for Gotenberg](https://github.com/mother-of-all-self-hosting/ansible-role-gotenberg) is developed and maintained by the MASH project. For details about configuring Gotenberg, you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-gotenberg/blob/main/docs/configuring-gotenberg.md) online
- 📁 `roles/galaxy/gotenberg/docs/configuring-gotenberg.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Related services

- [Apache Tika Server](tika.md) — Detect and extract metadata and text from different file types (such as PPT, XLS, and PDF)
- [Paperless-ngx](paperless-ngx.md) — Community-supported document management system that transforms your physical documents into a searchable online archive
