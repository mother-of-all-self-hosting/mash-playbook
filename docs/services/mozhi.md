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

# Mozhi

The playbook can install and configure [Mozhi](https://codeberg.org/aryak/mozhi) for you.

Mozhi is a frontend for translation engines which supports Google, Reverso, LibreTranslate, etc.

See the project's [documentation](https://codeberg.org/aryak/mozhi/src/branch/master/README.md) to learn what Mozhi does and why it might be useful to you.

For details about configuring the [Ansible role for Mozhi](https://github.com/mother-of-all-self-hosting/ansible-role-mozhi), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-mozhi/blob/main/docs/configuring-mozhi.md) online
- 📁 `roles/galaxy/mozhi/docs/configuring-mozhi.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# mozhi                                                                #
#                                                                      #
########################################################################

mozhi_enabled: true

mozhi_hostname: mozhi.example.com

########################################################################
#                                                                      #
# /mozhi                                                               #
#                                                                      #
########################################################################
```

**Note**: hosting Mozhi under a subpath (by configuring the `mozhi_path_prefix` variable) does not seem to be possible due to Mozhi's technical limitations.

## Usage

After running the command for installation, the Mozhi instance becomes available at the URL specified with `mozhi_hostname`. With the configuration above, the service is hosted at `https://mozhi.example.com`.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-mozhi/blob/main/docs/configuring-mozhi.md#troubleshooting) on the role's documentation for details.

## Related services

- [AnonymousOverflow](anonymousoverflow.md) — Frontend for StackOverflow
- [Redlib](redlib.md) — Frontend for Reddit
