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

# Redlib

The playbook can install and configure [Redlib](https://github.com/redlib-org/redlib) for you.

Redlib allows you to browse Reddit without exposing your IP address, browsing habits, and other browser fingerprinting data to the website.

See the project's [documentation](https://github.com/redlib-org/redlib/blob/main/README.md) to learn what Redlib does and why it might be useful to you.

For details about configuring the [Ansible role for Redlib](https://github.com/mother-of-all-self-hosting/ansible-role-redlib), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-redlib/blob/main/docs/configuring-redlib.md) online
- 📁 `roles/galaxy/redlib/docs/configuring-redlib.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# redlib                                                               #
#                                                                      #
########################################################################

redlib_enabled: true

redlib_hostname: redlib.example.com

########################################################################
#                                                                      #
# /redlib                                                              #
#                                                                      #
########################################################################
```

**Note**: hosting Redlib under a subpath (by configuring the `redlib_path_prefix` variable) is technically possible but not recommended, as most of the functions do not work as expected due to Redlib's technical limitations (pages and resources are not correctly loaded, and links are broken).

### Configure instance and user settings (optional)

There are various options for the instance and user settings. See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-redlib/blob/main/docs/configuring-redlib.md#configure-instance-and-user-settings-optional) on the role's documentation for details.

## Usage

After running the command for installation, Redlib becomes available at the specified hostname like `https://redlib.example.com`.

[Libredirect](https://libredirect.github.io/), an extension for Firefox and Chromium-based desktop browsers, has support for redirections to Redlib.

If you would like to make your instance public so that it can be used by anyone including Libredirect, please consider to send a PR to the [upstream project](https://github.com/redlib-org/redlib-instances) to add yours to the list, which Libredirect automatically fetches using a script (see [this FAQ entry](https://libredirect.github.io/faq.html#where_the_hell_are_those_instances_coming_from)). See [here](https://github.com/redlib-org/redlib-instances/blob/main/README.md) for details about how to do so.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-redlib/blob/main/docs/configuring-redlib.md#troubleshooting) on the role's documentation for details.
