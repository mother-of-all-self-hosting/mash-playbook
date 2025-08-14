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
SPDX-FileCopyrightText: 2024 Tiz

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# LanguageTool

The playbook can install and configure [LanguageTool](https://languagetool.org/) for you.

LanguageTool is an open source online grammar, style and spell checker.

See the project's [documentation](https://languagetool.org/dev) to learn what LanguageTool does and why it might be useful to you.

For details about configuring the [Ansible role for LanguageTool](https://github.com/mother-of-all-self-hosting/ansible-role-languagetool), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-languagetool/blob/main/docs/configuring-languagetool.md) online
- 📁 `roles/galaxy/languagetool/docs/configuring-languagetool.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) — a reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# languagetool                                                         #
#                                                                      #
########################################################################

languagetool_enabled: true

languagetool_hostname: mash.example.com
languagetool_path_prefix: /languagetool

########################################################################
#                                                                      #
# /languagetool                                                        #
#                                                                      #
########################################################################
```

### Enable n-gram data (optional)

LanguageTool can make use of large n-gram data sets to detect errors with words that are often confused, like "their" and "there". See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-languagetool/blob/main/docs/configuring-languagetool.md#enable-n-gram-data-optional) on the role's documentation for details.

## Usage

After running the command for installation, the LanguageTool instance becomes available at the URL specified with `languagetool_hostname` and `languagetool_path_prefix`. With the configuration above, the service is hosted at `https://mash.example.com/languagetool`.

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-languagetool/blob/main/docs/configuring-languagetool.md#usage) on the role's documentation for usage.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-languagetool/blob/main/docs/configuring-languagetool.md#troubleshooting) on the role's documentation for details.
