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
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# radicle-search

The playbook can install and configure [radicle-search](https://radicle.network/nodes/seed.radicle.dev/rad%3Az4V1sjrXqjvFdnCUbxPFqd5p4DtH5/tree/explorer/crates/radicle-search/README.md) for you.

radicle-search is an optional indexing daemon for [Radicle](https://radicle.dev/), a peer-to-peer code collaboration stack built on Git. Along with the Radicle node, this service maintains a Meilisearch index of repository metadata, which Radicle HTTP Daemon can use to provide fast, typo-tolerant repo listings and full-text search.

See the project's [documentation](https://radicle.network/nodes/seed.radicle.dev/rad%3Az4V1sjrXqjvFdnCUbxPFqd5p4DtH5/tree/explorer/crates/radicle-search/README.md) to learn what radicle-search does and why it might be useful to you.

For details about configuring the [Ansible role for radicle-search](https://radicle.network/nodes/progressiv.radicle.garden/rad%253AzcZtvqNbQKGT9h17g5Mzbx9LjjVp), you can check them via:

- 🌐 [the role's documentation](https://radicle.network/nodes/progressiv.radicle.garden/rad%253AzcZtvqNbQKGT9h17g5Mzbx9LjjVp/tree/docs/configuring-radicle-search.md) online
- 📁 `roles/galaxy/radicle_search/docs/configuring-radicle-search.md` locally, if you have [fetched the Ansible roles](../../docs/installing.md)

## Prerequisites

This service requires the following other services:

- [Meilisearch](../meilisearch/README.md) — Make sure to [obtain and set the default API admin key](../meilisearch/README.md#obtaining-api-keys)
- [Radicle HTTP Daemon](../radicle_httpd/README.md)
- [Radicle node](../radicle_node/README.md)

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../../docs/installing.md) process:

```yaml
########################################################################
#                                                                      #
# radicle_search                                                       #
#                                                                      #
########################################################################

radicle_search_enabled: true

########################################################################
#                                                                      #
# /radicle_search                                                      #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the radicle-search instance becomes available.

## Troubleshooting

Refer to [this section](https://radicle.network/nodes/progressiv.radicle.garden/rad%253AzcZtvqNbQKGT9h17g5Mzbx9LjjVp/tree/docs/configuring-radicle-search.md#troubleshooting) on the role's documentation for details.

## Related services

- [Radicle HTTP Daemon](../radicle_httpd/README.md) — Gateway between the Radicle protocol and the HTTP protocol
- [Radicle node](../radicle_node/README.md) — Network daemon for the Radicle network
