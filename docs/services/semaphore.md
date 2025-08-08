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

# Semaphore UI

The playbook can install and configure [Semaphore UI](https://semaphoreui.com) for you.

Semaphore UI is a modern UI for Ansible, Terraform/OpenTofu/Terragrunt, PowerShell and other DevOps tools.

See the project's [documentation](https://docs.semaphoreui.com/) to learn what Semaphore UI does and why it might be useful to you.

For details about configuring the [Ansible role for Semaphore UI](https://github.com/mother-of-all-self-hosting/ansible-role-semaphore), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-semaphore/blob/main/docs/configuring-semaphore.md) online
- 📁 `roles/galaxy/semaphore/docs/configuring-semaphore.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Postgres](postgres.md) / MySQL / [MariaDB](mariadb.md) database
- [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# semaphore                                                            #
#                                                                      #
########################################################################

semaphore_enabled: true

semaphore_hostname: semaphore.example.com

########################################################################
#                                                                      #
# /semaphore                                                           #
#                                                                      #
########################################################################
```

### Set details for the admin user

You need to create an instance's admin user by setting values to the `semaphore_admin_*` variables. See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-semaphore/blob/main/docs/configuring-semaphore.md#set-details-for-the-admin-user) on the role's documentation for details.

### Set a string for encrypting access keys

You also have to set a string used for encrypting access keys in database to `semaphore_access_key_encryption`. Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-semaphore/blob/main/docs/configuring-semaphore.md#set-a-string-for-encrypting-access-keys) on the role's documentation for details.

### Select database to use (optional)

By default Semaphore UI is configured to use Postgres, but you can choose other database such as MySQL (MariaDB) and BoltDB.

To use MariaDB, add the following configuration to your `vars.yml` file:

```yaml
semaphore_database_dialect: mysql
```

### Extending the configuration

There are some additional things you may wish to configure about the component.

Take a look at:

- [Semaphore UI](https://github.com/mother-of-all-self-hosting/ansible-role-semaphore)'s [`defaults/main.yml`](https://github.com/mother-of-all-self-hosting/ansible-role-semaphore/blob/main/defaults/main.yml) for some variables that you can customize via your `vars.yml` file.

See the [documentation](https://docs.semaphoreui.com/administration-guide/configuration/) for a complete list of Semaphore UI's config options such as [two-factor authentication with TOTP](https://github.com/mother-of-all-self-hosting/ansible-role-semaphore/blob/main/docs/configuring-semaphore.md#enable-2fa-authentication-with-totp-optional).

## Usage

After running the command for installation, Semaphore UI becomes available at the specified hostname like `https://semaphore.example.com`.

You can open the page with a web browser to log in to the instance. See [this official guide](https://docs.semaphoreui.com/user-guide/projects/) for details about how to use it.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-semaphore/blob/main/docs/configuring-semaphore.md#troubleshooting) on the role's documentation for details.
