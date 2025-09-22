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

# LimeSurvey

The playbook can install and configure [LimeSurvey](https://limesurvey.org) for you.

LimeSurvey is a set of PHP scripts that will allow you to run Your Own URL Shortener, on your server.

See the project's [documentation](https://limesurvey.org/docs) to learn what LimeSurvey does and why it might be useful to you.

For details about configuring the [Ansible role for LimeSurvey](https://github.com/mother-of-all-self-hosting/ansible-role-limesurvey), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-limesurvey/blob/main/docs/configuring-limesurvey.md) online
- 📁 `roles/galaxy/limesurvey/docs/configuring-limesurvey.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- MySQL / [MariaDB](mariadb.md) database
- [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# limesurvey                                                           #
#                                                                      #
########################################################################

limesurvey_enabled: true

limesurvey_hostname: limesurvey.example.com

########################################################################
#                                                                      #
# /limesurvey                                                          #
#                                                                      #
########################################################################
```

**Notes**:
- It is optionally possible to use a shorter hostname different from the main one. If doing so, make sure to point a DNS record for the domain to the server where the LimeSurvey instance is going to be hosted.
- Hosting LimeSurvey under a subpath (by configuring the `limesurvey_path_prefix` variable) does not seem to be possible due to LimeSurvey's technical limitations.

### Enable MariaDB

LimeSurvey requires a MySQL-compatible database to work. This playbook supports MariaDB, and you can set up a MariaDB instance by enabling it on `vars.yml`.

Refer to [this page](mariadb.md) for the instruction to enable it.

### Set the admin username and password

You also need to create an instance's user to access to the admin UI after installation. To create one, add the following configuration to your `vars.yml` file. Make sure to replace `YOUR_ADMIN_USERNAME_HERE` and `YOUR_ADMIN_PASSWORD_HERE`.

```yaml
limesurvey_environment_variable_user: YOUR_ADMIN_USERNAME_HERE
limesurvey_environment_variable_pass: YOUR_ADMIN_PASSWORD_HERE
```

## Usage

After running the command for installation, the LimeSurvey instance becomes available at the URL specified with `limesurvey_hostname` and `/admin/`. With the configuration above, the service is hosted at `https://limesurvey.example.com/admin/`.

First, open the URL with a web browser to complete installation on the server by clicking "Install LimeSurvey" button. After that, click the anchor link "LimeSurvey Administration Page" to log in with the username (`limesurvey_environment_variable_user`) and password (`limesurvey_environment_variable_pass`).

The help file is available at `limesurvey.example.com/readme.html`.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-limesurvey/blob/main/docs/configuring-limesurvey.md#troubleshooting) on the role's documentation for details.

## Related services

- [Kutt](kutt.md) — Modern URL shortener with support for custom domains
