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

# SilverBullet

The playbook can install and configure [SilverBullet](https://git.maid.zone/stuff/SilverBullet) for you.

SilverBullet allows you to browse SoundCloud without exposing your IP address, browsing habits, and other browser fingerprinting data to the website.

See the project's [documentation](https://git.maid.zone/stuff/SilverBullet/src/branch/main/README.md) to learn what SilverBullet does and why it might be useful to you.

For details about configuring the [Ansible role for SilverBullet](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az381JyLARWwSiZnYotVXehYcQEw7u), you can check them via:
- 🌐 [the role's documentation](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az381JyLARWwSiZnYotVXehYcQEw7u/tree/docs/configuring-silverbullet.md) online
- 📁 `roles/galaxy/silverbullet/docs/configuring-silverbullet.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# silverbullet                                                         #
#                                                                      #
########################################################################

silverbullet_enabled: true

silverbullet_hostname: silverbullet.example.com

########################################################################
#                                                                      #
# /silverbullet                                                        #
#                                                                      #
########################################################################
```

**Note**: hosting SilverBullet under a subpath (by configuring the `silverbullet_path_prefix` variable) does not seem to be possible due to SilverBullet's technical limitations.

## Usage

After running the command for installation, the SilverBullet instance becomes available at the URL specified with `silverbullet_hostname`. With the configuration above, the service is hosted at `https://silverbullet.example.com`.

## Troubleshooting

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az381JyLARWwSiZnYotVXehYcQEw7u/tree/docs/configuring-silverbullet.md#troubleshooting) on the role's documentation for details.

## Related services

- [AnonymousOverflow](anonymousoverflow.md) — Frontend for StackOverflow
- [GotHub](gothub.md) — Frontend for GitHub
- [Wikimore](wikimore.md) — Frontend for Wikipedia projects
