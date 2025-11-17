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
SPDX-FileCopyrightText: 2024 Thomas Miceli
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Apache Answer

The playbook can install and configure [Apache Answer](https://answer.apache.org/) for you.

Apache Answer is a Q&A community platform software for teams.

See the project's [documentation](https://answer.apache.org/docs/) to learn what Apache Answer does and why it might be useful to you.

For details about configuring the [Ansible role for Apache Answer](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az4Cd3nL74nNap51RBB6mtC1jipeH9), you can check them via:
- 🌐 [the role's documentation](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az4Cd3nL74nNap51RBB6mtC1jipeH9/tree/docs/configuring-answer.md) online
- 📁 `roles/galaxy/answer/docs/configuring-answer.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Postgres](postgres.md) / MySQL / [MariaDB](mariadb.md) / [SQLite](https://www.sqlite.org/) database
- [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# answer                                                               #
#                                                                      #
########################################################################

answer_enabled: true

answer_hostname: answer.example.com

########################################################################
#                                                                      #
# /answer                                                              #
#                                                                      #
########################################################################
```

**Note**: hosting Apache Answer under a subpath (by configuring the `answer_path_prefix` variable) does not seem to be possible due to Apache Answer's technical limitations.

### Select database to use

It is necessary to select a database used by Apache Answer from a MySQL compatible database, Postgres, and SQLite. See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az4Cd3nL74nNap51RBB6mtC1jipeH9/tree/docs/configuring-answer.md#specify-database) on the role's documentation for details.

### Automatic installation with environment variables

By default the role is configured to install the service with environment variables automatically when running the installation command.

For automatic installation, you need to set the name, email address, password for the administrator, and the email address for the contact who is responsible for the instance as well.

To do so, add the following configuration to your `vars.yml` file:

```yaml
answer_environment_variables_admin_name: ADMIN_NAME_HERE
answer_environment_variables_admin_email: ADMIN_EMAIL_ADDRESS_HERE
answer_environment_variables_admin_password: ADMIN_PASSWORD_HERE
answer_environment_variables_contact_email: CONTACT_EMAIL_ADDRESS_HERE
```

## Usage

After running the command for installation, the Apache Answer instance becomes available at the URL specified with `answer_hostname`. With the configuration above, the service is hosted at `https://answer.example.com`.

To get started, open the URL with a web browser to log in to the instance.

## Troubleshooting

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az4Cd3nL74nNap51RBB6mtC1jipeH9/tree/docs/configuring-answer.md#troubleshooting) on the role's documentation for details.

## Related services

- [NodeBB](nodebb.md) — Node.js based free forum software
