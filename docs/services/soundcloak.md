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

# soundcloak

The playbook can install and configure [soundcloak](https://git.maid.zone/stuff/soundcloak) for you.

soundcloak allows you to browse SoundCloud without exposing your IP address, browsing habits, and other browser fingerprinting data to the website.

See the project's [documentation](https://git.maid.zone/stuff/soundcloak/src/branch/main/README.md) to learn what soundcloak does and why it might be useful to you.

For details about configuring the [Ansible role for soundcloak](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az381JyLARWwSiZnYotVXehYcQEw7u), you can check them via:
- 🌐 [the role's documentation](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az381JyLARWwSiZnYotVXehYcQEw7u/tree/docs/configuring-soundcloak.md) online
- 📁 `roles/galaxy/soundcloak/docs/configuring-soundcloak.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# soundcloak                                                           #
#                                                                      #
########################################################################

soundcloak_enabled: true

soundcloak_hostname: soundcloak.example.com

########################################################################
#                                                                      #
# /soundcloak                                                          #
#                                                                      #
########################################################################
```

**Note**: hosting soundcloak under a subpath (by configuring the `soundcloak_path_prefix` variable) does not seem to be possible due to soundcloak's technical limitations.

## Usage

After running the command for installation, the soundcloak instance becomes available at the URL specified with `soundcloak_hostname`. With the configuration above, the service is hosted at `https://soundcloak.example.com`.

## Troubleshooting

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az381JyLARWwSiZnYotVXehYcQEw7u/tree/docs/configuring-soundcloak.md#troubleshooting) on the role's documentation for details.

## Related services

- [AnonymousOverflow](anonymousoverflow.md) — Frontend for StackOverflow
- [GotHub](gothub.md) — Frontend for GitHub
- [Wikimore](wikimore.md) — Frontend for Wikipedia projects
