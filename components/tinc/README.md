<!--
SPDX-FileCopyrightText: 2020 Aaron Raimist
SPDX-FileCopyrightText: 2020 Chris van Dijk
SPDX-FileCopyrightText: 2020 Dominik Zajac
SPDX-FileCopyrightText: 2020 Mickaël Cornière
SPDX-FileCopyrightText: 2020 Scott Crossen
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
SPDX-FileCopyrightText: 2024-2026 spatterlight

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# tinc

The playbook can install and configure [tinc](https://www.tinc-vpn.org/) for you.

tinc is a VPN daemon which joins nodes into one network. Nodes relay traffic for each other, and exchange it directly wherever they can reach each other.

See the project's [documentation](https://www.tinc-vpn.org/documentation/) to learn what tinc does and why it might be useful to you.

For details about configuring the [Ansible role for tinc](https://github.com/mother-of-all-self-hosting/ansible-role-tinc), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-tinc/blob/main/docs/configuring-tinc.md) online
- 📁 `roles/galaxy/tinc/docs/configuring-tinc.md` locally, if you have [fetched the Ansible roles](../../docs/installing.md)

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../../docs/installing.md) process:

```yaml
########################################################################
#                                                                      #
# tinc                                                                 #
#                                                                      #
########################################################################

tinc_enabled: true

# The name of this node, as in `tinc_hosts`
tinc_name: alpha

# The whole contents of this node's private key file
tinc_private_key: |
  PRIVATE_KEY_HERE

# The address of this node in the VPN, and the VPN's range
tinc_interface_addresses:
  - 10.10.0.1/24

########################################################################
#                                                                      #
# /tinc                                                                #
#                                                                      #
########################################################################
```

Every node also needs `tinc_hosts`, which lists all the nodes of the network with their public keys. Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-tinc/blob/main/docs/configuring-tinc.md#generate-the-keys) on the role's documentation for how to generate the keys, and to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-tinc/blob/main/docs/configuring-tinc.md#describe-the-network) for how to describe the network.

By default, the VPN interface only exists inside the container. Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-tinc/blob/main/docs/configuring-tinc.md#select-the-network-mode) for running the container with host networking, which the host needs to use the VPN.

## Usage

After running the command for installation, tinc connects to the nodes in `tinc_connect_to` and accepts connections from the other nodes in `tinc_hosts`.

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-tinc/blob/main/docs/configuring-tinc.md#usage) on the role's documentation for details about the usage.

## Troubleshooting

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-tinc/blob/main/docs/configuring-tinc.md#troubleshooting) on the role's documentation for details.
