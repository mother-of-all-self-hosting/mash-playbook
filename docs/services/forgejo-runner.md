<!--
SPDX-FileCopyrightText: 2020 Aaron Raimist
SPDX-FileCopyrightText: 2020 Chris van Dijk
SPDX-FileCopyrightText: 2020 Dominik Zajac
SPDX-FileCopyrightText: 2020 Mickaël Cornière
SPDX-FileCopyrightText: 2020-2024 MDAD project contributors
SPDX-FileCopyrightText: 2020-2025 Slavi Pantaleev
SPDX-FileCopyrightText: 2021 foxcris
SPDX-FileCopyrightText: 2022 François Darveau
SPDX-FileCopyrightText: 2022 Julian Foad
SPDX-FileCopyrightText: 2022 Warren Bailey
SPDX-FileCopyrightText: 2023 Antonis Christofides
SPDX-FileCopyrightText: 2023 Felix Stupp
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 MASH project contributors
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 Sergio Durigan Junior
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Forgejo Runner

The playbook can install and configure [Forgejo Runner](https://code.forgejo.org/forgejo/runner) for you.

Forgejo Runner is a runner to use with [Forgejo Actions](https://forgejo.org/docs/latest/admin/actions/). It provides a way to perform CI using Forgejo.

See the project's [documentation](https://forgejo.org/docs/latest/admin/actions/runner-installation/) to learn what Forgejo Runner does and why it might be useful to you.

> [!WARNING]
> The projects' documentation does **not recommend** running Forgejo Runner on the same machine as the Forgejo instance for security reasons.

The [Ansible role for Forgejo Runner](https://github.com/mother-of-all-self-hosting/ansible-role-forgejo-runner) is developed and maintained by the MASH project. For details about configuring Forgejo Runner, you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-forgejo-runner/blob/main/docs/configuring-forgejo-runner.md) online
- 📁 `roles/galaxy/forgejo_runner/docs/configuring-forgejo-runner.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Related services

- [Forgejo](forgejo.md) — Software forge (Git hosting service, etc.)
- [GitLab Runner](gitlab-runner.md) — Runner to use with GitLab CI/CD
- [Woodpecker CI](woodpecker-ci.md) — Extensible Continuous Integration (CI) engine
