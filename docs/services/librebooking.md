<!--
SPDX-FileCopyrightText: 2020 Aaron Raimist
SPDX-FileCopyrightText: 2020 Chris van Dijk
SPDX-FileCopyrightText: 2020 Dominik Zajac
SPDX-FileCopyrightText: 2020 Mickaël Cornière
SPDX-FileCopyrightText: 2020-2024 MDAD project contributors
SPDX-FileCopyrightText: 2020-2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2022 François Darveau
SPDX-FileCopyrightText: 2022 Julian Foad
SPDX-FileCopyrightText: 2022 Warren Bailey
SPDX-FileCopyrightText: 2023 Antonis Christofides
SPDX-FileCopyrightText: 2023 Felix Stupp
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 Mother-of-All-Self-Hosting contributors
SPDX-FileCopyrightText: 2024 Thomas Miceli
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara
SPDX-FileCopyrightText: 2026 shukon

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# LibreBooking

The playbook can install and configure [LibreBooking](https://github.com/LibreBooking/app) for you.

LibreBooking is a resource scheduling and booking application for any organization. It is an actively maintained FOSS fork of Booked Scheduler.

See the project's [documentation](https://librebooking.readthedocs.io/) to learn what LibreBooking does and why it might be useful to you.

For details about configuring the [Ansible role for LibreBooking](https://github.com/mother-of-all-self-hosting/ansible-role-librebooking), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-librebooking/blob/main/docs/configuring-librebooking.md) online
- 📁 `roles/galaxy/librebooking/docs/configuring-librebooking.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [MariaDB](mariadb.md) database
- [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# librebooking                                                         #
#                                                                      #
########################################################################

librebooking_enabled: true

librebooking_hostname: librebooking.example.com

########################################################################
#                                                                      #
# /librebooking                                                        #
#                                                                      #
########################################################################
```

### Enable MariaDB

LibreBooking requires a MySQL-compatible database to work. This playbook supports MariaDB, and you can set up a MariaDB instance by enabling it on `vars.yml`.

Refer to [this page](mariadb.md) for the instruction about how to enable it.

### Set a string for protecting setup wizard

You also have to set a string used for protecting the `/Web/install/` setup wizard. Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-librebooking/blob/main/docs/configuring-librebooking.md#set-a-string-for-protecting-setup-wizard) on the role's documentation for details.

## Usage

After running the command for installation, the LibreBooking instance becomes available at the URL specified with `librebooking_hostname`. With the configuration above, the service is hosted at `https://librebooking.example.com`.

To get started, open the URL with a web browser, and follow the set up wizard. Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-librebooking/blob/main/docs/configuring-librebooking.md#usage) on the role's documentation for details.

## Troubleshooting

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-librebooking/blob/main/docs/configuring-librebooking.md#troubleshooting) on the role's documentation for details.
