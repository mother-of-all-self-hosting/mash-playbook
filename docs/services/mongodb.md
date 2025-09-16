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

# MongoDB

The playbook can install and configure [MongoDB](https://mongodb.com) for you.

MongoDB is a source-available cross-platform document-oriented (NoSQL) database program.

See the project's [documentation](https://www.mongodb.com/docs/) to learn what MongoDB does and why it might be useful to you.

Some of the services installed by this playbook require a MongoDB database. Enabling the MongoDB database service will automatically wire all other services which require such a database to use it.

For details about configuring the [Ansible role for MongoDB](https://github.com/mother-of-all-self-hosting/ansible-role-mongodb), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-mongodb/blob/main/docs/configuring-mongodb.md) online
- 📁 `roles/galaxy/mongodb/docs/configuring-mongodb.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# mongodb                                                              #
#                                                                      #
########################################################################

mongodb_enabled: true

# Put a strong password below, generated with `pwgen -s 64 1` or in another way
mongodb_root_password: ''

########################################################################
#                                                                      #
# /mongodb                                                             #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the MongoDB instance becomes available.

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-mongodb/blob/main/docs/configuring-mongodb.md#maintenance) on the role's documentation for details about how to conduct maintenance tasks, such backing up its database and importing it.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-mongodb/blob/main/docs/configuring-mongodb.md#troubleshooting) on the role's documentation for details.
