<!--
SPDX-FileCopyrightText: 2020 - 2024 MDAD project contributors
SPDX-FileCopyrightText: 2020 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2020 Aaron Raimist
SPDX-FileCopyrightText: 2020 Chris van Dijk
SPDX-FileCopyrightText: 2020 Dominik Zajac
SPDX-FileCopyrightText: 2020 Mickaël Cornière
SPDX-FileCopyrightText: 2022 François Darveau
SPDX-FileCopyrightText: 2022 Julian Foad
SPDX-FileCopyrightText: 2022 Warren Bailey
SPDX-FileCopyrightText: 2023 Antonis Christofides
SPDX-FileCopyrightText: 2023 Felix Stupp
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# ReactFlux

The playbook can install and configure [ReactFlux](https://github.com/electh/ReactFlux) for you.

ReactFlux is a third-party web frontend for Miniflux, aimed at providing a more user-friendly reading experience.

See the project's [documentation](https://github.com/electh/ReactFlux/blob/main/README.md) to learn what ReactFlux does and why it might be useful to you.

For details about configuring the [Ansible role for ReactFlux](https://github.com/mother-of-all-self-hosting/ansible-role-reactflux), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-reactflux/blob/main/docs/configuring-reactflux.md) online
- 📁 `roles/galaxy/reactflux/docs/configuring-reactflux.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Miniflux](miniflux.md)
- [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# reactflux                                                            #
#                                                                      #
########################################################################

reactflux_enabled: true

reactflux_hostname: reactflux.example.com

########################################################################
#                                                                      #
# /reactflux                                                           #
#                                                                      #
########################################################################
```

**Note**: hosting ReactFlux under a subpath (by configuring the `reactflux_path_prefix` variable) does not seem to be possible due to ReactFlux's technical limitations.

## Usage

After running the command for installation, ReactFlux becomes available at the specified hostname like `https://reactflux.example.com`.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-reactflux/blob/main/docs/configuring-reactflux.md#troubleshooting) on the role's documentation for details.
