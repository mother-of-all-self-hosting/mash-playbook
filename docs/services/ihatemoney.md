<!--
SPDX-FileCopyrightText: 2020 Aaron Raimist
SPDX-FileCopyrightText: 2020 Chris van Dijk
SPDX-FileCopyrightText: 2020 Dominik Zajac
SPDX-FileCopyrightText: 2020 Mickaël Cornière
SPDX-FileCopyrightText: 2020-2024 MDAD project contributors
SPDX-FileCopyrightText: 2020-2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2022 François Darveau
SPDX-FileCopyrightText: 2022 Julian Foad
SPDX-FileCopyrightText: 2022 Warren Bailey
SPDX-FileCopyrightText: 2023 Antonis Christofides
SPDX-FileCopyrightText: 2023 Felix Stupp
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 Thomas Miceli
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara
SPDX-FileCopyrightText: 2025 MASH project contributors

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# I hate money

The playbook can install and configure [I hate money](https://github.com/spiral-project/ihatemoney) for you.

"I hate money" is a self-hosted shared budget manager.

See the project's [documentation](https://ihatemoney.readthedocs.io/en/latest/) to learn what "I hate money" does and why it might be useful to you.

For details about configuring the [Ansible role for I hate money](https://github.com/IUCCA/ansible-role-ihatemoney), you can check them via:

- 🌐 [the role's documentation](https://github.com/IUCCA/ansible-role-ihatemoney/blob/main/docs/configuring-ihatemoney.md) online
- 📁 `roles/galaxy/ihatemoney/docs/configuring-ihatemoney.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Postgres](postgres.md) / MySQL / [MariaDB](mariadb.md) / [SQLite](https://www.sqlite.org/) database
- [Traefik](traefik.md) reverse-proxy server
- (optional) [exim-relay](exim-relay.md) mailer

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# ihatemoney                                                           #
#                                                                      #
########################################################################

ihatemoney_enabled: true

ihatemoney_hostname: mash.example.com
ihatemoney_path_prefix: /ihatemoney

########################################################################
#                                                                      #
# /ihatemoney                                                          #
#                                                                      #
########################################################################
```

### Select database to use (optional)

By default I hate money is configured to use Postgres, but you can choose other database such as SQLite and MySQL (MariaDB).

To use MariaDB, add the following configuration to your `vars.yml` file:

```yaml
ihatemoney_database_type: mysql
```

See [this section](https://github.com/IUCCA/ansible-role-ihatemoney/blob/main/docs/configuring-ihatemoney.md#specify-database-optional) on the role's documentation for details.

### Configuring the mailer (optional)

On "I hate money" you can set up a mailer for functions such as password recovery. If you enable the [exim-relay](exim-relay.md) service in your inventory configuration, the playbook will automatically configure it as a mailer for the service.

To actually have the service use (and get messages sent through the exim-relay service), you will need to adjust settings on the service's UI after the service is installed.

>[!WARNING]
> Without setting an authentication method such as DKIM, SPF, and DMARC for your hostname, emails are most likely to be quarantined as spam at recipient's mail servers. The worst scenario is that your server's IP address or hostname will be included in the spam list such as the one managed by [Spamhaus](https://www.spamhaus.org/), depending on the reputation. As the exim-relay service supports DKIM signing, refer to [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay/blob/main/docs/configuring-exim-relay.md#enable-dkim-support-optional) for details about how to set it up.

### Control project creation access (optional)

By default the instance is open to public and anyone can create a project. If you wish to limit who is capable of creating one, you can secure the instance with the admin password.

Note that the instance is automatically secured if the admin password is set to `ihatemoney_admin_password`. If you want to keep the instance public *while the admin password is set*, add the following configuration to your `vars.yml` file:

```yaml
ihatemoney_public_project_creation: true
```

## Usage

After running the command for installation, the "I hate money" instance becomes available at the URL specified with `ihatemoney_hostname` and `ihatemoney_path_prefix`. With the configuration above, the service is hosted at `https://mash.example.com/ihatemoney`.

### Enabling administrative tasks

By default all administrative tasks are disabled. You can enable them by defining the `ADMIN_PASSWORD` environment variable.

You can generate an administrator's hashed password by **SSH-ing into into the server** and running a command as below:

```sh
docker exec -it mash-ihatemoney ihatemoney generate_password_hash
```

The generated value needs to be specified to the `ihatemoney_admin_password` variable on your `vars.yml` file:

```yaml
ihatemoney_admin_password: YOUR_HASHED_PASSWORD_HERE
```

Note that the value should contain the whole output of the command, including the hashing prefix, salt and key in the format as below:

```yaml
ihatemoney_admin_password: "scrypt:32768:8:1$....$......."
```

After populating the variable, re-run the installation process.

## Related services

- [Actual](actual.md) — Local-first personal finance tool
