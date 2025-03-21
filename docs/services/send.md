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
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Joplin Server

The playbook can install and configure [Joplin Server](https://joplinapp.org/help/dev/spec/architecture#joplin-server) for you.

Joplin Server is a self-hosted server component for [Joplin](https://joplinapp.org/) — a privacy-focused note taking and to-do application, which can handle a large number of notes organized into notebooks.

While Joplin is architectured to be "offline first", with a Joplin Server it is able to not only synchronize data among devices but also [share a notebook](https://joplinapp.org/help/apps/share_notebook/) with users and [publish a note](https://joplinapp.org/help/apps/publish_note/) on the internet to share it with anyone.

See the project's [documentation](https://joplinapp.org/help/) to learn what Joplin and Joplin Server do and why they might be useful to you.

For details about configuring the [Ansible role for Joplin Server](https://codeberg.org/acioustick/ansible-role-joplin-server), you can check them via:
- 🌐 [the role's documentation](https://codeberg.org/acioustick/ansible-role-joplin-server/src/branch/master/docs/configuring-joplin-server.md) online
- 📁 `roles/galaxy/joplin_server/docs/configuring-joplin-server.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Postgres](postgres.md) database
- [Traefik](traefik.md) reverse-proxy server
- (optional) [exim-relay](exim-relay.md) mailer

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# joplin_server                                                        #
#                                                                      #
########################################################################

joplin_server_enabled: true

joplin_server_hostname: mash.example.com
joplin_server_path_prefix: /joplin

########################################################################
#                                                                      #
# joplin_server                                                        #
#                                                                      #
########################################################################
```

As the most of the necessary settings for the role have been taken care of by the playbook, you can enable Joplin Server on your server with this minimum configuration.

### Configure the mailer

During installation, the Joplin Server by default creates its admin user with `admin@localhost` as its email address and `admin` as its password. To change the credentials from the admin page after logging in, authentication is required with an email sent to the updated email address. Email address authentication is also required by default for changing the credentials of non-admin users.

Though the mailer is technically not requisite, it is highly recommended to set it up for the log in credentials update function to work.

See [this section](https://codeberg.org/acioustick/ansible-role-joplin-server/src/branch/master/docs/configuring-joplin-server.md#configure-the-mailer) on the role's documentation for details about configuring the mailer.

**Notes**:
- **You can use exim-relay as the mailer, which is enabled on this playbook by default.** See [here](exim-relay.md) for details about how to set it up.
- Without setting an authentication method such as DKIM, SPF, and DMARC for your hostname, emails are most likely to be quarantined as spam at recipient's mail servers. If you have set up a mail server with the [exim-relay Ansible role](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay), you can enable DKIM signing with it. Refer [its documentation](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay/blob/main/docs/configuring-exim-relay.md#enable-dkim-support-optional) for details.

## Usage

To configure and manage the Joplin Server, go to `mash.example.com/joplin/login` specified with `joplin_server_hostname` and `joplin_server_path_prefix`, enter the admin credentials (email address: `admin@localhost`, password: `admin`) to log in. **After logging in, make sure to change the credentials.**

For security reason, the developer recommends to create a non-admin user for synchronization. You can create one on the "Users" page. After creating, you can use the email and password you specified for the user to synchronize data with your Joplin clients.

See [this section](https://codeberg.org/acioustick/ansible-role-joplin-server/src/branch/master/docs/configuring-joplin-server.md#usage) on the role's documentation for details about configuring the Joplin Server and the client application.

## Troubleshooting

See [this section](https://codeberg.org/acioustick/ansible-role-joplin-server/src/branch/master/docs/configuring-joplin-server.md#troubleshooting) on the role's documentation for details.
