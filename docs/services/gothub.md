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

# GotHub

The playbook can install and configure [GotHub](https://github.com/httpjamesm/GotHub) for you.

GotHub allows you to view StackOverflow threads without exposing your IP address, browsing habits, and other browser fingerprinting data to the website.

See the project's [documentation](https://github.com/httpjamesm/GotHub/blob/main/README.md) to learn what GotHub does and why it might be useful to you.

For details about configuring the [Ansible role for GotHub](https://github.com/mother-of-all-self-hosting/ansible-role-gothub), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-gothub/blob/main/docs/configuring-gothub.md) online
- 📁 `roles/galaxy/gothub/docs/configuring-gothub.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# gothub                                                               #
#                                                                      #
########################################################################

gothub_enabled: true

gothub_hostname: gothub.example.com

########################################################################
#                                                                      #
# /gothub                                                              #
#                                                                      #
########################################################################
```

**Note**: hosting GotHub under a subpath (by configuring the `gothub_path_prefix` variable) does not seem to be possible due to GotHub's technical limitations.

## Usage

After running the command for installation, the GotHub instance becomes available at the URL specified with `gothub_hostname`. With the configuration above, the service is hosted at `https://gothub.example.com`.

[Libredirect](https://libredirect.github.io/), an extension for Firefox and Chromium-based desktop browsers, has support for redirections to GotHub. See [this section](https://github.com/httpjamesm/GotHub/blob/main/README.md#how-to-make-stack-overflow-links-take-you-to-gothub-automatically) on the official documentation for more information.

If you would like to publish your instance so that it can be used by anyone including Libredirect, please consider to send a PR to the [upstream project](https://github.com/httpjamesm/GotHub) to add yours to [`instances.json`](https://github.com/httpjamesm/GotHub/blob/main/instances.json), which Libredirect automatically fetches using a script (see [this FAQ entry](https://libredirect.github.io/faq.html#where_the_hell_are_those_instances_coming_from)).

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-gothub/blob/main/docs/configuring-gothub.md#troubleshooting) on the role's documentation for details.

## Related services

- [Mozhi](mozhi.md) — Frontend for translation engines
- [Redlib](redlib.md) — Frontend for Reddit
