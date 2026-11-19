<!--
SPDX-FileCopyrightText: 2020 Aaron Raimist
SPDX-FileCopyrightText: 2020 Chris van Dijk
SPDX-FileCopyrightText: 2020 Dominik Zajac
SPDX-FileCopyrightText: 2020 Mickaël Cornière
SPDX-FileCopyrightText: 2020-2024 MDAD project contributors
SPDX-FileCopyrightText: 2020-2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2021 foxcris
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

# obfs4 bridge

The playbook can install and configure an [obfs4 bridge](https://community.torproject.org/relay/setup/bridge/) for you.

The obfs4 bridge helps users connect to the [Tor](https://torproject.org/) network in places where Tor is blocked.

For details about configuring the [Ansible role for the obfs4 bridge](https://radicle.network/nodes/progressiv.radicle.garden/rad%3Az2zadyxdG33vwpHEHDWFpRH6qtacQ), you can check them via:

- 🌐 [the role's documentation](https://radicle.network/nodes/progressiv.radicle.garden/rad%3Az2zadyxdG33vwpHEHDWFpRH6qtacQ/tree/docs/configuring-obfs4-bridge.md) online
- 📁 `roles/galaxy/obfs4_bridge/docs/configuring-obfs4-bridge.md` locally, if you have [fetched the Ansible roles](../../docs/installing.md)

## Related services

- [Standalone Snowflake proxy](../snowflake/README.md) — Help users connect to the Tor network in places where Tor is blocked
