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

# CryptPad

The playbook can install and configure [CryptPad](https://cryptpad.org) for you.

CryptPad is a free and open-source collaboration suite that is end-to-end encrypted.

See the project's [documentation](https://docs.cryptpad.org) to learn what CryptPad does and why it might be useful to you.

For details about configuring the [Ansible role for CryptPad](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az38Yp2e9yFouswvrnX5MdgZYaViLb), you can check them via:
- 🌐 [the role's documentation](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az38Yp2e9yFouswvrnX5MdgZYaViLb/tree/docs/configuring-cryptpad.md) online
- 📁 `roles/galaxy/cryptpad/docs/configuring-cryptpad.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# cryptpad                                                             #
#                                                                      #
########################################################################

cryptpad_enabled: true

cryptpad_main_hostname: cryptpad.example.com

cryptpad_sandbox_hostname: sandbox.example.com

########################################################################
#                                                                      #
# /cryptpad                                                            #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the CryptPad instance becomes available at the URL specified with `cryptpad_main_hostname`. With the configuration above, the service is hosted at `https://cryptpad.example.com`.

To get started, run the command below to output the URL for creating a first administrator account:

```sh
ansible-playbook -i inventory/hosts setup.yml --tags=get-installation-url-cryptpad
```

After running the command, open the URL with a web browser, and follow the set up wizard.

## Troubleshooting

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az38Yp2e9yFouswvrnX5MdgZYaViLb/tree/docs/configuring-cryptpad.md#troubleshooting) on the role's documentation for details.
