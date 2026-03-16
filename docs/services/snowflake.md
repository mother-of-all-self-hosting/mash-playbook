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
SPDX-FileCopyrightText: 2024-2025 Suguru Hirahara
SPDX-FileCopyrightText: 2024 Thomas Miceli

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Standalone Snowflake proxy

The playbook can install and configure a [standalone Snowflake proxy](https://community.torproject.org/relay/setup/snowflake/standalone/) for you.

The standalone [Snowflake](https://snowflake.torproject.org/) proxy helps users connect to the [Tor](https://torproject.org/) network in places where Tor is blocked.

The [Ansible role for the standalone Snowflake proxy](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Aznvd313jEb23f9AUNmtsweE7YHCK) is developed and maintained by the MASH project. For details about configuring the proxy, you can check them via:
- 🌐 [the role's documentation](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Aznvd313jEb23f9AUNmtsweE7YHCK/tree/docs/configuring-snowflake.md) online
- 📁 `roles/galaxy/snowflake/docs/configuring-snowflake.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Related services

- [Onion Service with C Tor](onion-service-tor.md) — Run Onion Service with [C Tor](https://gitlab.torproject.org/tpo/core/tor)
