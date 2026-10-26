<!--
SPDX-FileCopyrightText: 2023 Nikita Chernyi
SPDX-FileCopyrightText: 2023 Slavi Pantaleev
SPDX-FileCopyrightText: 2023 aine-etke
SPDX-FileCopyrightText: 2025 MASH project contributors
SPDX-FileCopyrightText: 2025, 2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Soft Serve

The playbook can install and configure [Soft Serve](https://github.com/charmbracelet/soft-serve) for you.

Soft Serve is a self-hostable [Git](https://git-scm.com/) server for the command line.

See the project's [documentation](https://github.com/charmbracelet/soft-serve/blob/main/README.md) to learn what Soft Serve does and why it might be useful to you.

For details about configuring the [Ansible role for Soft Serve](https://github.com/mother-of-all-self-hosting/ansible-role-soft_serve), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-soft_serve/blob/main/docs/configuring-soft-serve.md) online
- 📁 `roles/galaxy/soft_serve/docs/configuring-soft-serve.md` locally, if you have [fetched the Ansible roles](../../docs/installing.md)

## Dependencies

This service requires the following other services:

- [Postgres](../postgres/README.md) / [SQLite](https://www.sqlite.org/) database

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../../docs/installing.md) process:

```yaml
########################################################################
#                                                                      #
# soft_serve                                                           #
#                                                                      #
########################################################################

soft_serve_enabled: true

soft_serve_hostname: soft-serve.example.com

########################################################################
#                                                                      #
# /soft_serve                                                          #
#                                                                      #
########################################################################
```

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-soft_serve/blob/main/docs/configuring-soft-serve.md#adjusting-the-playbook-configuration) on the role's documentation for details about other settings.

### Select database to use

The service can use either Postgres or SQLite, and you need to choose one. Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-soft_serve/blob/main/docs/configuring-soft-serve.md#specify-database) on the role's documentation for details.

>[!NOTE]
> If your current `vars.yml` file does not include `soft_serve_database_type`, the database driver of your existing installation is most likely to be `sqlite`.

## Usage

After running the command for installation, the Soft Serve instance becomes available at the hostname specified with `soft_serve_hostname`. With the configuration above, the service is hosted at `soft-serve.example.com`.

To get started, you can run a command `ssh example@soft-serve.example.com -p 2222` with the defined SSH key. Note that you need to [finish the configuration yourself](https://github.com/charmbracelet/soft-serve#configuration). **Otherwise any user with the SSH key will be able to log in as an administrator.**
