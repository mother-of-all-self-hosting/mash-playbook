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

# etcd

The playbook can install and configure [etcd](https://etcd.io/) for you.

etcd is a strongly consistent, distributed key-value store that provides a reliable way to store data that needs to be accessed by a distributed system or cluster of machines. It gracefully handles leader elections during network partitions and can tolerate machine failure, even in the leader node.

See the project's [documentation](https://etcd.io/docs/latest/) to learn what etcd does and why it might be useful to you.

For details about configuring the [Ansible role for etcd](https://github.com/mother-of-all-self-hosting/ansible-role-etcd), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-etcd/blob/main/docs/configuring-etcd.md) online
- 📁 `roles/galaxy/etcd/docs/configuring-etcd.md` locally, if you have [fetched the Ansible roles](../installing.md)

>[!NOTE]
> Our current setup and documentation are **aiming at running etcd for internal purposes** (as a dependency for other [services](../supported-services.md) such as [APISIX Dashboard](apisix-dashboard.md) and [APISIX Gateway](apisix-gateway.md)). If you need a production deployment, you will need to install multiple etcd instances (on multiple machines) and connect them in a cluster. Please note that this is beyond the scope of our documentation here.

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# etcd                                                                 #
#                                                                      #
########################################################################

etcd_enabled: true

# By default, the playbook will set a root password by itself.
# If you'd like to set your own, uncomment and explicitly set this.
# etcd_environment_variable_etcd_root_password: ''

# Uncomment this if you'd like to run etcd without password-protection.
# etcd_environment_variable_allow_none_authentication: true

########################################################################
#                                                                      #
# /etcd                                                                #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the etcd instance becomes available.

As mentioned above, the purpose of the etcd component in this Ansible playbook is to serve as a dependency for other [services](../supported-services.md). For this use-case, you don't need to do anything special beyond enabling the component.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-etcd/blob/main/docs/configuring-etcd.md#troubleshooting) on the role's documentation for details.
