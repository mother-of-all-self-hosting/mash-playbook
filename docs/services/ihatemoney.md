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

## Dependencies

This service requires the following other services:

- a [Postgres](postgres.md) database
- [Traefik](traefik.md) reverse-proxy server
- (optional) [exim-relay](exim-relay.md) mailer

## Adjusting the playbook configuration

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

### Configuring the mailer (optional)

On "I hate money" you can set up a mailer for functions such as password recovery. If you enable the [exim-relay](exim-relay.md) service in your inventory configuration, the playbook will automatically configure it as a mailer for the service.

To actually have the service use (and get messages sent through the exim-relay service), you will need to adjust settings on the service's UI after the service is installed.

>[!WARNING]
> Without setting an authentication method such as DKIM, SPF, and DMARC for your hostname, emails are most likely to be quarantined as spam at recipient's mail servers. The worst scenario is that your server's IP address or hostname will be included in the spam list such as the one managed by [Spamhaus](https://www.spamhaus.org/), depending on the reputation. As the exim-relay service supports DKIM signing, refer to [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay/blob/main/docs/configuring-exim-relay.md#enable-dkim-support-optional) for details about how to set it up.

### Enable the admin dashboard (optional)

You can enable the admin dashboard by adding the following configuration to your `vars.yml` file.

```yaml
ihatemoney_admin_password: ADMIN_PASSWORD_HERE
```

Having installed the service, generate a hashed password by **SSH-ing into into the server** and running a command as below:

```sh
docker exec -it mash-ihatemoney ihatemoney generate_password_hash
```

After populating the variable with the hashed password, run the installation process again.
Your variable should contain the whole output from above, including hashing prefix, salt and key:

```yaml
ihatemoney_admin_password: "scrypt:32768:8:1$....$......."
```

### Control project creation access (optional)

By default the instance is open to public and anyone can create a project. If you wish to limit who is capable of creating one, you can secure the instance with the admin password.

Note that the instance is automatically secured if the admin password is set to `ihatemoney_admin_password`. If you want to keep the instance public *while the admin password is set*, add the following configuration to your `vars.yml` file:

```yaml
ihatemoney_public_project_creation: true
```

## Usage

After running the command for installation, the "I hate money" instance becomes available at the URL specified with `ihatemoney_hostname` and `ihatemoney_path_prefix`. With the configuration above, the service is hosted at `https://mash.example.com/ihatemoney`.

## Related services

- [Actual](actual.md) — Local-first personal finance tool
