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

The playbook can install and configure [LimeSurvey](https://www.limesurvey.org) for you.

LimeSurvey is a feature-rich free software for web based forms and surveys, which supports extensive survey logic.

See the project's [documentation](https://www.limesurvey.org/manual/LimeSurvey_Manual) to learn what LimeSurvey does and why it might be useful to you.

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

**Note**: hosting LimeSurvey under a subpath (by configuring the `limesurvey_path_prefix` variable) does not seem to be possible due to LimeSurvey's technical limitations.

### Enable MariaDB

LimeSurvey requires a MySQL-compatible database to work. This playbook supports MariaDB, and you can set up a MariaDB instance by enabling it on `vars.yml`.

Refer to [this page](mariadb.md) for the instruction to enable it.

### Set administrator's account details

You also need to create an instance's user to access to the admin UI after installation. To create one, add the following configuration to your `vars.yml` file.

```yaml
limesurvey_environment_variables_admin_user: LIMESURVEY_ADMIN_USERNAME_HERE
limesurvey_environment_variables_admin_password: LIMESURVEY_ADMIN_PASSWORD_HERE
limesurvey_environment_variables_admin_name: LIMESURVEY_ADMIN_NAME_HERE
limesurvey_environment_variables_admin_email: LIMESURVEY_ADMIN_EMAIL_ADDRESS_HERE
```

Make sure to replace the values with your own ones.

## Usage

After running the command for installation, the LimeSurvey instance becomes available at the URL specified with `limesurvey_hostname`. With the configuration above, the service is hosted at `https://limesurvey.example.com`.

To get started, open the URL `https://limesurvey.example.com/index.php/admin` with a web browser, and log in to the instance with the administrator account credentials.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-limesurvey/blob/main/docs/configuring-limesurvey.md#troubleshooting) on the role's documentation for details.
