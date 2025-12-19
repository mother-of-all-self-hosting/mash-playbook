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

# keyoxide-web

The playbook can install and configure [keyoxide-web](https://codeberg.org/keyoxide/keyoxide-web) for you.

keyoxide-web is a web client for [Keyoxide](https://keyoxide.org/), a decentralized tool to create and verify decentralized online identities.

See the project's [documentation](https://docs.keyoxide.org/) to learn what keyoxide-web does and why it might be useful to you.

For details about configuring the [Ansible role for keyoxide-web](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az3m9zZgMmAQX5aVtj5Y9KYRnhjVrt), you can check them via:
- 🌐 [the role's documentation](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az3m9zZgMmAQX5aVtj5Y9KYRnhjVrt/tree/docs/configuring-keyoxide.md) online
- 📁 `roles/galaxy/keyoxide/docs/configuring-keyoxide.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Prerequisites

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# keyoxide                                                             #
#                                                                      #
########################################################################

keyoxide_enabled: true

keyoxide_hostname: keyoxide.example.com

########################################################################
#                                                                      #
# /keyoxide                                                            #
#                                                                      #
########################################################################
```

**Note**: hosting keyoxide-web under a subpath (by configuring the `keyoxide_path_prefix` variable) does not seem to be possible due to keyoxide-web's technical limitations.

## Usage

After running the command for installation, the keyoxide-web instance becomes available at the URL specified with `keyoxide_hostname`. With the configuration above, the service is hosted at `https://keyoxide.example.com`.

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az3m9zZgMmAQX5aVtj5Y9KYRnhjVrt/tree/docs/configuring-keyoxide.md#usage) on the role's documentation for details about the usage.

## Troubleshooting

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az3m9zZgMmAQX5aVtj5Y9KYRnhjVrt/tree/docs/configuring-keyoxide.md#troubleshooting) on the role's documentation for details.
