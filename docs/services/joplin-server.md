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

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Joplin Server

The playbook can install and configure [Joplin Server](https://joplinapp.org/help/dev/spec/architecture#joplin-server) for you.

Joplin Server is a self-hosted server component for [Joplin](https://joplinapp.org/) — a privacy-focused note taking and to-do application, which can handle a large number of notes organized into notebooks.

While Joplin is architectured to be "offline first", with a Joplin Server it is able to not only synchronize data among devices but also [share a notebook](https://joplinapp.org/help/apps/share_notebook/) with users and [publish a note](https://joplinapp.org/help/apps/publish_note/) on the internet to share it with anyone.

See the project's [documentation](https://joplinapp.org/help/) to learn what Joplin and Joplin Server do and why they might be useful to you.

For details about configuring the [Ansible role for Joplin Server](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3AzttNpUS7xCeDnn2e4No2dUvZv7L7), you can check them via:

- 🌐 [the role's documentation](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3AzttNpUS7xCeDnn2e4No2dUvZv7L7/tree/docs/configuring-joplin-server.md) online
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
# /joplin_server                                                       #
#                                                                      #
########################################################################
```

As the most of the necessary settings for the role have been taken care of by the playbook, you can enable Joplin Server on your server with this minimum configuration.

### Configuring the mailer (optional)

On Joplin Server you can set up a mailer for functions such as password recovery. If you enable the [exim-relay](exim-relay.md) service in your inventory configuration, the playbook will automatically configure it as a mailer for the service.

To actually have the service use (and get messages sent through the exim-relay service), you will need to adjust settings on the service's UI after the service is installed.

During installation, the Joplin Server by default creates its admin user with `admin@localhost` as its email address and `admin` as its password. To change the credentials from the admin page after logging in, authentication is required with an email sent to the updated email address. Email address authentication is also required by default for changing the credentials of non-admin users.

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3AzttNpUS7xCeDnn2e4No2dUvZv7L7/tree/docs/configuring-joplin-server.md#configure-the-mailer) on the role's documentation for details about configuring the mailer.

>[!WARNING]
> Without setting an authentication method such as DKIM, SPF, and DMARC for your hostname, emails are most likely to be quarantined as spam at recipient's mail servers. The worst scenario is that your server's IP address or hostname will be included in the spam list such as the one managed by [Spamhaus](https://www.spamhaus.org/), depending on the reputation. As the exim-relay service supports DKIM signing, refer to [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay/blob/main/docs/configuring-exim-relay.md#enable-dkim-support-optional) for details about how to set it up.

## Usage

To configure and manage the Joplin Server, open the URL `mash.example.com/joplin/login` specified with `joplin_server_hostname` and `joplin_server_path_prefix`, enter the admin credentials (email address: `admin@localhost`, password: `admin`) to log in. **After logging in, make sure to change the credentials.**

For security reason, the developer recommends to create a non-admin user for synchronization. You can create one on the "Users" page. After creating, you can use the email and password you specified for the user to synchronize data with your Joplin clients.

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3AzttNpUS7xCeDnn2e4No2dUvZv7L7/tree/docs/configuring-joplin-server.md#usage) on the role's documentation for details about configuring the Joplin Server and the client application.

## Troubleshooting

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3AzttNpUS7xCeDnn2e4No2dUvZv7L7/tree/docs/configuring-joplin-server.md#troubleshooting) on the role's documentation for details.
