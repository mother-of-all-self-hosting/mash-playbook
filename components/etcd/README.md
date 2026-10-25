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
- 📁 `roles/galaxy/etcd/docs/configuring-etcd.md` locally, if you have [fetched the Ansible roles](../../docs/installing.md)

>[!NOTE]
> The current implementation on this playbook is **optimized for running etcd for internal purposes** (as a dependency for other [services](../../docs/supported-services.md) such as [APISIX](../apisix/README.md)).
