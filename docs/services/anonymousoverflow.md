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
- MySQL / [MariaDB](mariadb.md) database

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
# anonymousoverflow                                                    #
#                                                                      #
########################################################################
```

**Notes**:
- It is optionally possible to use a shorter hostname different from the main one. If doing so, make sure to point a DNS record for the domain to the server where the AnonymousOverflow instance is going to be hosted.
- Hosting AnonymousOverflow under a subpath (by configuring the `anonymousoverflow_path_prefix` variable) does not seem to be possible due to AnonymousOverflow's technical limitations.

### Enable MariaDB

You can enable a MariaDB instance by adding the following configuration:

```yaml
########################################################################
#                                                                      #
# mariadb                                                              #
#                                                                      #
########################################################################

mariadb_enabled: true

# Put a strong password below, generated with `pwgen -s 64 1` or in another way
mariadb_root_password: ''

########################################################################
#                                                                      #
# /mariadb                                                             #
#                                                                      #
########################################################################
```

### Set the admin username and password

You also need to create an instance's user to access to the admin UI after installation. To create one, add the following configuration to your `vars.yml` file. Make sure to replace `YOUR_ADMIN_USERNAME_HERE` and `YOUR_ADMIN_PASSWORD_HERE`.

```yaml
anonymousoverflow_environment_variable_user: YOUR_ADMIN_USERNAME_HERE
anonymousoverflow_environment_variable_pass: YOUR_ADMIN_PASSWORD_HERE
```

## Usage

After running the command for installation, AnonymousOverflow's admin UI is available at the specified hostname with `/admin/` such as `anonymousoverflow.example.com/admin/`.

First, open the page with a web browser to complete installation on the server by clicking "Install AnonymousOverflow" button. After that, click the anchor link "AnonymousOverflow Administration Page" to log in with the username (`anonymousoverflow_environment_variable_user`) and password (`anonymousoverflow_environment_variable_pass`).

The help file is available at `anonymousoverflow.example.com/readme.html`.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-anonymousoverflow/blob/main/docs/configuring-anonymousoverflow.md#troubleshooting) on the role's documentation for details.
