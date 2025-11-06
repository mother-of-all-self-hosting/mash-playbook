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

# phpMyAdmin

The playbook can install and configure [phpMyAdmin](https://www.phpmyadmin.org) for you.

phpMyAdmin is a feature-rich free software for web based forms and surveys, which supports extensive survey logic.

See the project's [documentation](https://www.phpmyadmin.org/manual/phpMyAdmin_Manual) to learn what phpMyAdmin does and why it might be useful to you.

For details about configuring the [Ansible role for phpMyAdmin](https://github.com/mother-of-all-self-hosting/ansible-role-phpmyadmin), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-phpmyadmin/blob/main/docs/configuring-phpmyadmin.md) online
- 📁 `roles/galaxy/phpmyadmin/docs/configuring-phpmyadmin.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- MySQL / [MariaDB](mariadb.md) database
- [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# phpmyadmin                                                           #
#                                                                      #
########################################################################

phpmyadmin_enabled: true

phpmyadmin_hostname: phpmyadmin.example.com

########################################################################
#                                                                      #
# /phpmyadmin                                                          #
#                                                                      #
########################################################################
```

**Note**: hosting phpMyAdmin under a subpath (by configuring the `phpmyadmin_path_prefix` variable) does not seem to be possible due to phpMyAdmin's technical limitations.

### Enable MariaDB

phpMyAdmin requires a MySQL-compatible database to work. This playbook supports MariaDB, and you can set up a MariaDB instance by enabling it on `vars.yml`.

Refer to [this page](mariadb.md) for the instruction to enable it.

### Set administrator's account details

You also need to create an instance's user to access to the admin UI after installation. To create one, add the following configuration to your `vars.yml` file.

```yaml
phpmyadmin_environment_variables_admin_user: LIMESURVEY_ADMIN_USERNAME_HERE
phpmyadmin_environment_variables_admin_password: LIMESURVEY_ADMIN_PASSWORD_HERE
phpmyadmin_environment_variables_admin_name: LIMESURVEY_ADMIN_NAME_HERE
phpmyadmin_environment_variables_admin_email: LIMESURVEY_ADMIN_EMAIL_ADDRESS_HERE
```

Make sure to replace the values with your own ones.

## Usage

After running the command for installation, the phpMyAdmin instance becomes available at the URL specified with `phpmyadmin_hostname`. With the configuration above, the service is hosted at `https://phpmyadmin.example.com`.

To get started, open the URL `https://phpmyadmin.example.com/index.php/admin` with a web browser, and log in to the instance with the administrator account credentials.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-phpmyadmin/blob/main/docs/configuring-phpmyadmin.md#troubleshooting) on the role's documentation for details.
