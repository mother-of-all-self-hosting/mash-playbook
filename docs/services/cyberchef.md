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

# CyberChef

The playbook can install and configure [CyberChef](https://github.com/gchq/CyberChef) for you.

CyberChef is an intuitive application for carrying out encryption, encoding, and data analysis operations inside a browser locally. These operations include simple encoding like XOR and Base64, more complex encryption like AES, DES and Blowfish, creating binary and hexdumps, and so on.

See the project's [documentation](https://github.com/gchq/CyberChef/blob/master/README.md) to learn what CyberChef does and why it might be useful to you.

For details about configuring the [Ansible role for CyberChef](https://codeberg.org/acioustick/ansible-role-cyberchef), you can check them via:
- 🌐 [the role's documentation](https://codeberg.org/acioustick/ansible-role-cyberchef/src/branch/master/docs/configuring-cyberchef.md) online
- 📁 `roles/galaxy/cyberchef/docs/configuring-cyberchef.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# cyberchef                                                            #
#                                                                      #
########################################################################

cyberchef_enabled: true

cyberchef_hostname: cyberchef.example.com

########################################################################
#                                                                      #
# /cyberchef                                                           #
#                                                                      #
########################################################################
```

**Note**: hosting CyberChef under a subpath (by configuring the `cyberchef_path_prefix` variable) does not seem to be possible due to CyberChef's technical limitations.

## Usage

After running the command for installation, the CyberChef instance becomes available at the URL specified with `cyberchef_hostname`. With the configuration above, the service is hosted at `https://cyberchef.example.com`.

## Troubleshooting

See [this section](https://codeberg.org/acioustick/ansible-role-cyberchef/src/branch/master/docs/configuring-cyberchef.md#troubleshooting) on the role's documentation for details.
