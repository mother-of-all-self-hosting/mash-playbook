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

## Usage

After running the command for installation, Semaphore UI becomes available at the specified hostname like `https://semaphore.example.com`.

[Libredirect](https://libredirect.github.io/), an extension for Firefox and Chromium-based desktop browsers, has support for redirections to Semaphore UI. See [this section](https://semaphoreui.com/blob/main/README.md#how-to-make-stack-overflow-links-take-you-to-semaphore-automatically) on the official documentation for more information.

If you would like to publish your instance so that it can be used by anyone including Libredirect, please consider to send a PR to the [upstream project](https://semaphoreui.com) to add yours to [`instances.json`](https://semaphoreui.com/blob/main/instances.json), which Libredirect automatically fetches using a script (see [this FAQ entry](https://libredirect.github.io/faq.html#where_the_hell_are_those_instances_coming_from)).

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-semaphore/blob/main/docs/configuring-semaphore.md#troubleshooting) on the role's documentation for details.

## Related services

- [Mozhi](mozhi.md) — Frontend for translation engines
- [Redlib](redlib.md) — Frontend for Reddit
