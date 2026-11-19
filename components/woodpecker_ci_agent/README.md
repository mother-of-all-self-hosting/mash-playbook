<!--
SPDX-FileCopyrightText: 2020 Aaron Raimist
SPDX-FileCopyrightText: 2020 Chris van Dijk
SPDX-FileCopyrightText: 2020 Dominik Zajac
SPDX-FileCopyrightText: 2020 Mickaël Cornière
SPDX-FileCopyrightText: 2020-2024 MDAD project contributors
SPDX-FileCopyrightText: 2020-2025 Slavi Pantaleev
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

# Woodpecker CI agent

The playbook can install and configure an agent of [Woodpecker CI](https://woodpecker-ci.org/) for you.

The agent runs the CI jobs of a [Woodpecker CI server](../woodpecker_ci_server/README.md). See the server's page for an overview of a Woodpecker CI installation.

>[!WARNING]
> It's better to run the agent elsewhere (not on the source-control server or a server serving anything of value) — on a machine that doesn't contain sensitive data.

For details about configuring the [Ansible role for Woodpecker CI agent](https://github.com/mother-of-all-self-hosting/ansible-role-woodpecker-ci-agent), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-woodpecker-ci-agent/blob/main/docs/configuring-woodpecker-ci-agent.md) online
- 📁 `roles/galaxy/woodpecker_ci_agent/docs/configuring-woodpecker-ci-agent.md` locally, if you have [fetched the Ansible roles](../../docs/installing.md)

## Dependencies

This service requires the following other services:

- a [Woodpecker CI server](../woodpecker_ci_server/README.md)

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../../docs/installing.md) process:

```yaml
########################################################################
#                                                                      #
# woodpecker_ci_agent                                                  #
#                                                                      #
########################################################################

woodpecker_ci_agent_enabled: true

########################################################################
#                                                                      #
# /woodpecker_ci_agent                                                 #
#                                                                      #
########################################################################
```

## Usage

The agent should automatically register with the Woodpecker CI server and take jobs from it.

## Related services

- [Woodpecker CI server](../woodpecker_ci_server/README.md) — Extensible Continuous Integration (CI) engine
