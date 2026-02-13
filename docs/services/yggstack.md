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

# Yggstack

The playbook can install and configure [Yggstack](https://github.com/yggdrasil-network/yggstack) for you.

Yggstack is a SOCKS5 proxy server and TCP port forwarder for [Yggdrasil](https://yggdrasil-network.github.io), an early-stage implementation of a fully end-to-end encrypted IPv6 network.

See the project's [documentation](https://github.com/yggdrasil-network/yggstack/blob/develop/README.md) to learn what Yggstack does and why it might be useful to you.

For details about configuring the [Ansible role for Yggstack](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az2BzsfYJzpSCK4tC8kCR1uCooZYX5), you can check them via:
- 🌐 [the role's documentation](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az2BzsfYJzpSCK4tC8kCR1uCooZYX5/tree/docs/configuring-yggstack.md) online
- 📁 `roles/galaxy/yggstack/docs/configuring-yggstack.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# yggstack                                                             #
#                                                                      #
########################################################################

yggstack_enabled: true

########################################################################
#                                                                      #
# /yggstack                                                            #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, Yggstack becomes available at the IPv6 address which the service generates for you. The IPv6 address, its subnet, and your public key have been been logged to the console logs on the startup. The configuration file (`yggdrasil.conf`) can be found in `yggstack_data_path`.

Refer to [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az2BzsfYJzpSCK4tC8kCR1uCooZYX5/tree/docs/configuring-yggstack.md#usage) for details about how to set up Yggstack.

## Troubleshooting

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az2BzsfYJzpSCK4tC8kCR1uCooZYX5/tree/docs/configuring-yggstack.md#troubleshooting) on the role's documentation for details.

## References

- <https://yggdrasil-network.github.io/about.html> — Basic concepts about Yggdrasil Network
- <https://yggdrasil-network.github.io/services.html>
