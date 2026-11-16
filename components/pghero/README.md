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

# PgHero

The playbook can install and configure [PgHero](https://github.com/ankane/pghero) for you.

PgHero is a performance dashboard for Postgres.

See the project's [documentation](https://github.com/ankane/pghero) to learn what PgHero does and why it might be useful to you.

For details about configuring the [Ansible role for PgHero](https://radicle.network/nodes/progressiv.radicle.garden/rad%3Az3hLeeK934cgjDRL6BmxPeKpNcVUb), you can check them via:

- 🌐 [the role's documentation](https://radicle.network/nodes/progressiv.radicle.garden/rad%3Az3hLeeK934cgjDRL6BmxPeKpNcVUb/tree/docs/configuring-pghero.md) online
- 📁 `roles/galaxy/pghero/docs/configuring-pghero.md` locally, if you have [fetched the Ansible roles](../../docs/installing.md)

## Dependencies

This service requires the following other services:

- [Postgres](../postgres/README.md) database
- [Traefik](../traefik/README.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../../docs/installing.md) process:

```yaml
########################################################################
#                                                                      #
# pghero                                                               #
#                                                                      #
########################################################################

pghero_enabled: true

pghero_hostname: mash.example.com
pghero_path_prefix: /pghero

########################################################################
#                                                                      #
# /pghero                                                              #
#                                                                      #
########################################################################
```

### Configuring HTTP Basic authentication

Since there does not exist an authentication system on the web interface, the HTTP Basic authentication on Traefik is enabled for the web interface by default, considering the nature of the service. Refer to [this section](https://radicle.network/nodes/progressiv.radicle.garden/rad%3Az3hLeeK934cgjDRL6BmxPeKpNcVUb/tree/docs/configuring-pghero.md#configuring-http-basic-authentication) on the role's documentation for details about how to set it up.

## Usage

After running the command for installation, the PgHero instance becomes available at the URL specified with `pghero_hostname` and `pghero_path_prefix`. With the configuration above, the service is hosted at `https://mash.example.com/pghero`.

## Troubleshooting

Refer to [this section](https://radicle.network/nodes/progressiv.radicle.garden/rad%3Az3hLeeK934cgjDRL6BmxPeKpNcVUb/tree/docs/configuring-pghero.md#troubleshooting) on the role's documentation for details.
