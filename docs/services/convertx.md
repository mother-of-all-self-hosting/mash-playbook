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

# ConvertX

The playbook can install and configure [ConvertX](https://github.com/C4illin/ConvertX) for you.

ConvertX is a self-hosted online file converter which supports a lot of different formats for pictures, video, images, document files, etc.

See the project's [documentation](https://github.com/C4illin/ConvertX/blob/main/README.md) to learn what ConvertX does and why it might be useful to you.

For details about configuring the [Ansible role for ConvertX](https://github.com/mother-of-all-self-hosting/ansible-role-convertx), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-convertx/blob/main/docs/configuring-convertx.md) online
- 📁 `roles/galaxy/convertx/docs/configuring-convertx.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# convertx                                                             #
#                                                                      #
########################################################################

convertx_enabled: true

convertx_hostname: convertx.example.com

########################################################################
#                                                                      #
# /convertx                                                            #
#                                                                      #
########################################################################
```

**Note**: hosting ConvertX under a subpath (by configuring the `convertx_path_prefix` variable) is technically possible but not recommended, as most of the functions do not work as expected due to ConvertX's technical limitations (pages and resources are not correctly loaded, and links are broken).

### Configure instance and user settings (optional)

There are various options for the instance and user settings. See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-convertx/blob/main/docs/configuring-convertx.md#configure-instance-and-user-settings-optional) on the role's documentation for details.

## Usage

After running the command for installation, ConvertX becomes available at the specified hostname like `https://convertx.example.com`.

[Libredirect](https://libredirect.github.io/), an extension for Firefox and Chromium-based desktop browsers, has support for redirections to ConvertX.

If you would like to make your instance public so that it can be used by anyone including Libredirect, please consider to send a PR to the [upstream project](https://github.com/convertx-org/convertx-instances) to add yours to the list, which Libredirect automatically fetches using a script (see [this FAQ entry](https://libredirect.github.io/faq.html#where_the_hell_are_those_instances_coming_from)). See [here](https://github.com/convertx-org/convertx-instances/blob/main/README.md) for details about how to do so.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-convertx/blob/main/docs/configuring-convertx.md#troubleshooting) on the role's documentation for details.
