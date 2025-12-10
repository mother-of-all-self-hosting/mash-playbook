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

# Ergo

The playbook can install and configure [Ergo](https://www.ergo.org) for you.

Ergo is a feature-rich free software for web based forms and surveys, which supports extensive survey logic.

See the project's [documentation](https://www.ergo.org/manual/Ergo_Manual) to learn what Ergo does and why it might be useful to you.

For details about configuring the [Ansible role for Ergo](https://github.com/mother-of-all-self-hosting/ansible-role-ergo), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-ergo/blob/main/docs/configuring-ergo.md) online
- 📁 `roles/galaxy/ergo/docs/configuring-ergo.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- MySQL / [MariaDB](mariadb.md) database
- [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# ergo                                                                 #
#                                                                      #
########################################################################

ergo_enabled: true

ergo_hostname: ergo.example.com

########################################################################
#                                                                      #
# /ergo                                                                #
#                                                                      #
########################################################################
```

**Note**: hosting Ergo under a subpath (by configuring the `ergo_path_prefix` variable) does not seem to be possible due to Ergo's technical limitations.

### Enable MariaDB

Ergo requires a MySQL-compatible database to work. This playbook supports MariaDB, and you can set up a MariaDB instance by enabling it on `vars.yml`.

Refer to [this page](mariadb.md) for the instruction to enable it.

### Set administrator's account details

You also need to create an instance's user to access to the admin UI after installation. To create one, add the following configuration to your `vars.yml` file.

```yaml
ergo_environment_variables_admin_user: LIMESURVEY_ADMIN_USERNAME_HERE
ergo_environment_variables_admin_password: LIMESURVEY_ADMIN_PASSWORD_HERE
ergo_environment_variables_admin_name: LIMESURVEY_ADMIN_NAME_HERE
ergo_environment_variables_admin_email: LIMESURVEY_ADMIN_EMAIL_ADDRESS_HERE
```

Make sure to replace the values with your own ones.

## Usage

After running the command for installation, the Ergo instance becomes available at the URL specified with `ergo_hostname`. With the configuration above, the service is hosted at `https://ergo.example.com`.

To get started, open the URL `https://ergo.example.com/index.php/admin` with a web browser, and log in to the instance with the administrator account credentials.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-ergo/blob/main/docs/configuring-ergo.md#troubleshooting) on the role's documentation for details.
