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

# AnonymousOverflow

The playbook can install and configure [AnonymousOverflow](https://github.com/httpjamesm/AnonymousOverflow) for you.

AnonymousOverflow allows you to view StackOverflow threads without exposing your IP address, browsing habits, and other browser fingerprinting data to the website.

See the project's [documentation](https://github.com/httpjamesm/AnonymousOverflow/blob/main/README.md) to learn what AnonymousOverflow does and why it might be useful to you.

For details about configuring the [Ansible role for AnonymousOverflow](https://github.com/mother-of-all-self-hosting/ansible-role-anonymousoverflow), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-anonymousoverflow/blob/main/docs/configuring-anonymousoverflow.md) online
- 📁 `roles/galaxy/anonymousoverflow/docs/configuring-anonymousoverflow.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# anonymousoverflow                                                    #
#                                                                      #
########################################################################

anonymousoverflow_enabled: true

anonymousoverflow_hostname: anonymousoverflow.example.com

########################################################################
#                                                                      #
# /anonymousoverflow                                                   #
#                                                                      #
########################################################################
```

**Note**: hosting AnonymousOverflow under a subpath (by configuring the `anonymousoverflow_path_prefix` variable) does not seem to be possible due to AnonymousOverflow's technical limitations.

## Usage

After running the command for installation, AnonymousOverflow becomes available at the specified hostname like `https://anonymousoverflow.example.com`.

[Libredirect](https://libredirect.github.io/), an extension for Firefox and Chromium-based desktop browsers, has support for redirections to AnonymousOverflow. See [this section](https://github.com/httpjamesm/AnonymousOverflow/blob/main/README.md#how-to-make-stack-overflow-links-take-you-to-anonymousoverflow-automatically) on the official documentation for more information.

If you would like to publish your instance so that it can be used by anyone including Libredirect, please consider to send a PR to the [upstream project](https://github.com/httpjamesm/AnonymousOverflow) to add yours to [`instances.json`](https://github.com/httpjamesm/AnonymousOverflow/blob/main/instances.json), which Libredirect automatically fetches using a script (see [this FAQ entry](https://libredirect.github.io/faq.html#where_the_hell_are_those_instances_coming_from)).

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-anonymousoverflow/blob/main/docs/configuring-anonymousoverflow.md#troubleshooting) on the role's documentation for details.
