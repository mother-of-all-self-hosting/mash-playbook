<!--
SPDX-FileCopyrightText: 2023 Slavi Pantaleev
SPDX-FileCopyrightText: 2025, 2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Docker Registry Purger

The playbook can install and configure [Docker Registry Purger](https://github.com/devture/docker-registry-purger) for you.

Docker Registry Purger is a small tool used for purging a private Docker registry's old tags.

See the project's [documentation](https://github.com/devture/docker-registry-purger/blob/main/README.md) to learn what Docker Registry Purger does and why it might be useful to you.

For details about configuring the [Ansible role for Docker Registry Purger](https://github.com/mother-of-all-self-hosting/ansible-role-docker-registry-purger), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-docker-registry-purger/blob/main/docs/configuring-docker-registry-purger.md) online
- 📁 `roles/galaxy/docker_registry_purger/docs/configuring-docker-registry-purger.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Related services

- [Distribution Registry](docker-registry.md) — Container image distribution registry
