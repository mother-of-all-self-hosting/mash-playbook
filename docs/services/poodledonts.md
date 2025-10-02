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

# PoodleDonts

The playbook can install and configure [PoodleDonts](https://codeberg.org/poodledonts/poodledonts) for you.

PoodleDonts allows you to view GitHub repositories without exposing your IP address, browsing habits, and other browser fingerprinting data to the website.

See the project's [documentation](https://codeberg.org/poodledonts/poodledonts/src/branch/dev/README.md) to learn what PoodleDonts does and why it might be useful to you.

For details about configuring the [Ansible role for PoodleDonts](https://codeberg.org/acioustick/ansible-role-poodledonts), you can check them via:
- 🌐 [the role's documentation](https://codeberg.org/acioustick/ansible-role-poodledonts/src/branch/master/docs/configuring-poodledonts.md) online
- 📁 `roles/galaxy/poodledonts/docs/configuring-poodledonts.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# poodledonts                                                          #
#                                                                      #
########################################################################

poodledonts_enabled: true

poodledonts_hostname: poodledonts.example.com

########################################################################
#                                                                      #
# /poodledonts                                                         #
#                                                                      #
########################################################################
```

**Note**: hosting PoodleDonts under a subpath (by configuring the `poodledonts_path_prefix` variable) does not seem to be possible due to PoodleDonts's technical limitations.

There are other settings which need configuring such as ones about instance's management and its transparency. See [this section](https://codeberg.org/acioustick/ansible-role-poodledonts/src/branch/master/docs/configuring-poodledonts.md#enable-disable-proxying-non-essential-data) on the role's documentation for details.

## Usage

After running the command for installation, the PoodleDonts instance becomes available at the URL specified with `poodledonts_hostname`. With the configuration above, the service is hosted at `https://poodledonts.example.com`.

[Libredirect](https://libredirect.github.io/), an extension for Firefox and Chromium-based desktop browsers, has support for redirections to PoodleDonts.

If you would like to make your instance public so that it can be used by anyone including Libredirect, please consider to send a PR to the [upstream project](https://codeberg.org/poodledonts/poodledonts-instances) to add yours to [`instances.json`](https://codeberg.org/poodledonts/poodledonts-instances/src/branch/master/instances.json), which Libredirect automatically fetches using a script (see [this FAQ entry](https://libredirect.github.io/faq.html#where_the_hell_are_those_instances_coming_from)).

## Troubleshooting

See [this section](https://codeberg.org/acioustick/ansible-role-poodledonts/src/branch/master/docs/configuring-poodledonts.md#troubleshooting) on the role's documentation for details.

## Related services

- [Mozhi](mozhi.md) — Frontend for translation engines
- [Redlib](redlib.md) — Frontend for Reddit
