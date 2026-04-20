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
SPDX-FileCopyrightText: 2024 Tiz
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Reitti

The playbook can install and configure [Reitti](https://www.dedicatedcode.com/projects/reitti/) for you.

Reitti is a personal location tracking and analysis application.

See the project's [documentation](https://www.dedicatedcode.com/projects/reitti/) to learn what Reitti does and why it might be useful to you.

For details about configuring the [Ansible role for Reitti](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az3rhdtDR5EHHGk1SNBHwYtofxNyAf), you can check them via:

- 🌐 [the role's documentation](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az3rhdtDR5EHHGk1SNBHwYtofxNyAf/tree/docs/configuring-reitti.md) online
- 📁 `roles/galaxy/reitti/docs/configuring-reitti.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Postgres database with PostGIS extensions installed](postgis.md)
- [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# reitti                                                               #
#                                                                      #
########################################################################

reitti_enabled: true

reitti_hostname: reitti.example.com

########################################################################
#                                                                      #
# /reitti                                                              #
#                                                                      #
########################################################################
```

### Usage

After running the command for installation, the Reitti instance becomes available at the URL specified with `reitti_hostname`. With the configuration above, the service is hosted at `https://reitti.example.com`.

To get started, open the URL with a web browser to create an account. **Note that the first registered user becomes an administrator automatically.**

## Troubleshooting

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az3rhdtDR5EHHGk1SNBHwYtofxNyAf/tree/docs/configuring-reitti.md#troubleshooting) on the role's documentation for details.
