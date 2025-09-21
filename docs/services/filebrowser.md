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

# File Browser

The playbook can install and configure [File Browser](https://github.com/httpjamesm/File Browser) for you.

File Browser allows you to view StackOverflow threads without exposing your IP address, browsing habits, and other browser fingerprinting data to the website.

See the project's [documentation](https://github.com/httpjamesm/File Browser/blob/main/README.md) to learn what File Browser does and why it might be useful to you.

For details about configuring the [Ansible role for File Browser](https://github.com/mother-of-all-self-hosting/ansible-role-filebrowser), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-filebrowser/blob/main/docs/configuring-filebrowser.md) online
- 📁 `roles/galaxy/filebrowser/docs/configuring-filebrowser.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# filebrowser                                                          #
#                                                                      #
########################################################################

filebrowser_enabled: true

filebrowser_hostname: filebrowser.example.com

########################################################################
#                                                                      #
# /filebrowser                                                         #
#                                                                      #
########################################################################
```

**Note**: hosting File Browser under a subpath (by configuring the `filebrowser_path_prefix` variable) does not seem to be possible due to File Browser's technical limitations.

## Usage

After running the command for installation, the File Browser instance becomes available at the URL specified with `filebrowser_hostname`. With the configuration above, the service is hosted at `https://filebrowser.example.com`.

[Libredirect](https://libredirect.github.io/), an extension for Firefox and Chromium-based desktop browsers, has support for redirections to File Browser. See [this section](https://github.com/httpjamesm/File Browser/blob/main/README.md#how-to-make-stack-overflow-links-take-you-to-filebrowser-automatically) on the official documentation for more information.

If you would like to publish your instance so that it can be used by anyone including Libredirect, please consider to send a PR to the [upstream project](https://github.com/httpjamesm/File Browser) to add yours to [`instances.json`](https://github.com/httpjamesm/File Browser/blob/main/instances.json), which Libredirect automatically fetches using a script (see [this FAQ entry](https://libredirect.github.io/faq.html#where_the_hell_are_those_instances_coming_from)).

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-filebrowser/blob/main/docs/configuring-filebrowser.md#troubleshooting) on the role's documentation for details.

## Related services

- [Mozhi](mozhi.md) — Frontend for translation engines
- [Redlib](redlib.md) — Frontend for Reddit
