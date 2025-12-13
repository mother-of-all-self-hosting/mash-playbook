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

For details about configuring the [Ansible role for CyberChef](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az2zgHMDh4Pb8yr4DH8BVkMcdboBXd), you can check them via:
- 🌐 [the role's documentation](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az2zgHMDh4Pb8yr4DH8BVkMcdboBXd/tree/docs/configuring-cyberchef.md) online
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

### Using the default Docker image (optional)

To have the service run as the playbook's default user instead of root user, this service is by default configured to use the Docker image locally built on [this own Dockerfile](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az2zgHMDh4Pb8yr4DH8BVkMcdboBXd/tree/templates/Dockerfile.j2).

If you prefer simply using [the official Docker image](https://github.com/gchq/CyberChef/pkgs/container/cyberchef) instead, add the following configuration to your `vars.yml` file:

```yaml
cyberchef_container_image_self_build: false
```

>[!NOTE]
> Adding the variable configures the playbook to run the service as a root user.

## Usage

After running the command for installation, the CyberChef instance becomes available at the URL specified with `cyberchef_hostname`. With the configuration above, the service is hosted at `https://cyberchef.example.com`.

## Troubleshooting

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az2zgHMDh4Pb8yr4DH8BVkMcdboBXd/tree/docs/configuring-cyberchef.md#troubleshooting) on the role's documentation for details.
