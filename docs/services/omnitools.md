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

# OmniTools

The playbook can install and configure [OmniTools](https://github.com/iib0011/omni-tools) for you.

OmniTools is a self-hosted web app offering a variety of online tools to simplify everyday tasks. Whether you are coding, manipulating images/videos, PDFs or crunching numbers, OmniTools has you covered.

See the project's [documentation](https://github.com/iib0011/omni-tools/blob/main/README.md) to learn what OmniTools does and why it might be useful to you.

For details about configuring the [Ansible role for OmniTools](https://codeberg.org/daguwar/ansible-role-omnitools), you can check them via:
- 🌐 [the role's documentation](https://codeberg.org/daguwar/ansible-role-omnitools/src/branch/main/docs/configuring-omnitools.md) online
- 📁 `roles/galaxy/cyberchef/docs/configuring-omnitools.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# omnitools                                                            #
#                                                                      #
########################################################################

omnitools_enabled: true

omnitools_hostname: omnitools.example.com

########################################################################
#                                                                      #
# /omnitools                                                           #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the OmniTools instance becomes available at the URL specified with `omnitools_hostname`. With the configuration above, the service is hosted at `https://omnitools.example.com`.

## Troubleshooting

See [this section](https://codeberg.org/daguwar/ansible-role-omnitools/src/branch/main/docs/configuring-omnitools.md#troubleshooting) on the role's documentation for details.
