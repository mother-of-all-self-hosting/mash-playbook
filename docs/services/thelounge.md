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

# The Lounge

The playbook can install and configure [The Lounge](https://thelounge.chat) for you.

The Lounge is a modern web IRC client designed for self-hosting. It implements features such as push notification, link previews, and file uploading, and keeps a persistent connection to the IRC server while you are offline (meaning you do not need a bouncer). It is a progressiv web app (PWA), and can be accessed via a browser.

See the project's [documentation](https://thelounge.chat/docs) to learn what The Lounge does and why it might be useful to you.

For details about configuring the [Ansible role for The Lounge](https://codeberg.org/acioustick/ansible-role-thelounge), you can check them via:
- 🌐 [the role's documentation](https://codeberg.org/acioustick/ansible-role-thelounge/src/branch/master/docs/configuring-thelounge.md) online
- 📁 `roles/galaxy/thelounge/docs/configuring-thelounge.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Prerequisites

You may need to open some ports to your server, if you use another firewall in front of the server. Refer to [the role's documentation](https://codeberg.org/acioustick/ansible-role-thelounge/src/branch/master/docs/configuring-thelounge.md#prerequisites) to check which ones to be configured.

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# thelounge                                                            #
#                                                                      #
########################################################################

thelounge_enabled: true

thelounge_hostname: mash.example.com
thelounge_path_prefix: /thelounge

########################################################################
#                                                                      #
# /thelounge                                                           #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the The Lounge instance becomes available at the URL specified with `thelounge_hostname` and `thelounge_path_prefix`. With the configuration above, the service is hosted at `https://mash.example.com/thelounge`.

You can log in to the instance with the default login credential of the admin account (username: `admin`, password: `thelounge`).

To improve security regarding the admin account, **the role configures the instance on the intranet search mode by default**, so that it does not broadcast its existence to peers before you change the login credential.

See [this section](https://codeberg.org/acioustick/ansible-role-thelounge/src/branch/master/docs/configuring-thelounge.md#usage) on the role's documentation for details about changing the admin user password and search mode, including protecting the instance with the password.

## Troubleshooting

See [this section](https://codeberg.org/acioustick/ansible-role-thelounge/src/branch/master/docs/configuring-thelounge.md#troubleshooting) on the role's documentation for details.

## Related services

- [SearXNG](searxng.md) — a privacy-respecting, hackable [metasearch engine](https://en.wikipedia.org/wiki/Metasearch_engine). See [this section](searxng.md#add-your-thelounge-instance-optional) for the instruction to add your The Lounge instance to the SearXNG instance.
