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

# Actual

The playbook can install and configure [Actual](https://actualbudget.org) for you.

Actual is a local-first personal finance tool.

See the project's [documentation](https://actualbudget.org/docs/) to learn what Actual does and why it might be useful to you.

For details about configuring the [Ansible role for Actual](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az2chD7Kt74JwEMafxTooxN7MaeYtK), you can check them via:
- 🌐 [the role's documentation](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az2chD7Kt74JwEMafxTooxN7MaeYtK/tree/docs/configuring-actual.md) online
- 📁 `roles/galaxy/actual/docs/configuring-actual.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# actual                                                               #
#                                                                      #
########################################################################

actual_enabled: true

actual_hostname: actual.example.com

########################################################################
#                                                                      #
# /actual                                                              #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the Actual instance becomes available at the URL specified with `actual_hostname`. With the configuration above, the service is hosted at `https://actual.example.com`.

To get started, open the URL with a web browser to create an account.

## Troubleshooting

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az2chD7Kt74JwEMafxTooxN7MaeYtK/tree/docs/configuring-actual.md#troubleshooting) on the role's documentation for details.

## Related services

- [I hate money](ihatemoney.md) — Shared budget manager
