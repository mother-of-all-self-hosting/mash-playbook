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
SPDX-FileCopyrightText: 2026 spatterlight

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# strongSwan

The playbook can install and configure [strongSwan](https://www.strongswan.org/) for you.

strongSwan is an IPsec-based VPN solution.

See the project's [documentation](https://docs.strongswan.org/) to learn what strongSwan does and why it might be useful to you.

For details about configuring the [Ansible role for strongSwan](https://github.com/mother-of-all-self-hosting/ansible-role-strongswan), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-strongswan/blob/main/docs/configuring-strongswan.md) online
- 📁 `roles/galaxy/strongswan/docs/configuring-strongswan.md` locally, if you have [fetched the Ansible roles](../../docs/installing.md)

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../../docs/installing.md) process:

```yaml
########################################################################
#                                                                      #
# strongswan                                                           #
#                                                                      #
########################################################################

strongswan_enabled: true

########################################################################
#                                                                      #
# /strongswan                                                          #
#                                                                      #
########################################################################
```

strongSwan does nothing until it is given connections to set up. Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-strongswan/blob/main/docs/configuring-strongswan.md#configure-connections) on the role's documentation for how to configure them, and to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-strongswan/blob/main/docs/configuring-strongswan.md#select-the-network-mode) for running the container with host networking, which site-to-site and road warrior setups need.

## Usage

After running the command for installation, strongSwan loads the configured connections and initiates those with `start_action = start`.

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-strongswan/blob/main/docs/configuring-strongswan.md#usage) on the role's documentation for details about the usage.

## Troubleshooting

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-strongswan/blob/main/docs/configuring-strongswan.md#troubleshooting) on the role's documentation for details.
