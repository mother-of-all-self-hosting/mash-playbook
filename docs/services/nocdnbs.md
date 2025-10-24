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

# noCDNbs

The playbook can install and configure [noCDNbs](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az4JAZNsXXS8yVoW8NuvAgNEHfbgTc) (a fork of the [original project](https://git.private.coffee/PrivateCoffee/nocdnbs)) for you.

noCDNbs allows you to use Google Fonts without exposing your IP address, browsing habits, and other browser fingerprinting data to the website.

See the project's [documentation](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az4JAZNsXXS8yVoW8NuvAgNEHfbgTc/src/branch/main/README.md) to learn what noCDNbs does and why it might be useful to you.

For details about configuring the [Ansible role for noCDNbs](https://codeberg.org/acioustick/ansible-role-nocdnbs), you can check them via:
- 🌐 [the role's documentation](https://codeberg.org/acioustick/ansible-role-nocdnbs/src/branch/master/docs/configuring-nocdnbs.md) online
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

**Note**: hosting noCDNbs under a subpath (by configuring the `nocdnbs_path_prefix` variable) does not seem to be possible due to noCDNbs's technical limitations.

## Usage

After running the command for installation, the noCDNbs instance becomes available at the URL specified with `nocdnbs_hostname`. With the configuration above, the service is hosted at `https://nocdnbs.example.com`.

## Troubleshooting

See [this section](https://codeberg.org/acioustick/ansible-role-nocdnbs/src/branch/master/docs/configuring-nocdnbs.md#troubleshooting) on the role's documentation for details.

## Related services

- [Mozhi](mozhi.md) — Frontend for translation engines
- [Redlib](redlib.md) — Frontend for Reddit
