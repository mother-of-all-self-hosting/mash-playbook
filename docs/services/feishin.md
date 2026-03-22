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

# Feishin

The playbook can install and configure [Feishin](https://github.com/jeffvli/feishin) for you.

Feishin is a music player for servers which implement a [Navidrome](https://www.navidrome.org/), [Jellyfin](https://jellyfin.org/), or OpenSubsonic compatible API such as [Funkwhale](https://www.funkwhale.audio/).

See the project's [documentation](https://github.com/jeffvli/feishin/blob/development/README.md) to learn what Feishin does and why it might be useful to you.

For details about configuring the [Ansible role for Feishin](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Azmszzm7ynZe8nt5ZwaLctssyJcNm), you can check them via:
- 🌐 [the role's documentation](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Azmszzm7ynZe8nt5ZwaLctssyJcNm/tree/docs/configuring-feishin.md) online
- 📁 `roles/galaxy/feishin/docs/configuring-feishin.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server
- [Navidrome](navidrome.md) / [Jellyfin](jellyfin.md) / [Funkwhale](funkwhale.md)

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# feishin                                                              #
#                                                                      #
########################################################################

feishin_enabled: true

feishin_hostname: feishin.example.com

########################################################################
#                                                                      #
# /feishin                                                             #
#                                                                      #
########################################################################
```

### Enabling server lock (optional)

By default one can have Feishin connect to any server as specified. Refer to [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Azmszzm7ynZe8nt5ZwaLctssyJcNm/tree/docs/configuring-feishin.md#enabling-server-lock-optional) on the role's documentation about how to activate "server lock".

## Usage

After running the command for installation, the Feishin instance becomes available at the URL specified with `feishin_hostname`. With the configuration above, the service is hosted at `https://feishin.example.com`.

To get started, open the URL with a web browser to create an account.

## Troubleshooting

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Azmszzm7ynZe8nt5ZwaLctssyJcNm/tree/docs/configuring-feishin.md#troubleshooting) on the role's documentation for details.
