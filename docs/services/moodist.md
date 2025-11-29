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

# Moodist

The playbook can install and configure [Moodist](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az3HEG7KePQVAbZXSdn7tGNb7FVDqL) (a fork of the [original project](https://git.private.coffee/PrivateCoffee/nocdnbs)) for you.

Moodist allows you to use cdnjs without exposing your IP address, browsing habits, and other browser fingerprinting data to Cloudflare.

See the project's [documentation](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az3HEG7KePQVAbZXSdn7tGNb7FVDqL/tree/README.md) to learn what Moodist does and why it might be useful to you.

For details about configuring the [Ansible role for Moodist](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az8vyzN3a8DmwhcUq3949SihKd1Wh), you can check them via:
- 🌐 [the role's documentation](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az8vyzN3a8DmwhcUq3949SihKd1Wh/tree/docs/configuring-nocdnbs.md) online
- 📁 `roles/galaxy/nocdnbs/docs/configuring-nocdnbs.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# nocdnbs                                                              #
#                                                                      #
########################################################################

nocdnbs_enabled: true

nocdnbs_hostname: nocdnbs.example.com

########################################################################
#                                                                      #
# /nocdnbs                                                             #
#                                                                      #
########################################################################
```

**Note**: hosting Moodist under a subpath (by configuring the `nocdnbs_path_prefix` variable) does not seem to be possible due to Moodist's technical limitations.

## Usage

After running the command for installation, the Moodist instance becomes available at the URL specified with `nocdnbs_hostname`. With the configuration above, the service is hosted at `https://nocdnbs.example.com`.

## Troubleshooting

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az8vyzN3a8DmwhcUq3949SihKd1Wh/tree/docs/configuring-nocdnbs.md#troubleshooting) on the role's documentation for details.

## Related services

- [PoodleDonts](poodledonts.md) — Privacy-friendly Google Fonts proxy
