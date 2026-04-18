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
SPDX-FileCopyrightText: 2024 Tiz
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# GoToSocial

The playbook can install and configure [GoToSocial](https://gotosocial.org/) for you.

GoToSocial is a self-hosted [ActivityPub](https://activitypub.rocks/) social network server. With GoToSocial, you can keep in touch with your friends, post, read, and share images and articles.

See the project's [documentation](https://docs.gotosocial.org/) to learn what GoToSocial does and why it might be useful to you.

For details about configuring the [Ansible role for GoToSocial](https://github.com/mother-of-all-self-hosting/ansible-role-gotosocial), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-gotosocial/blob/main/docs/configuring-gotosocial.md) online
- 📁 `roles/galaxy/gotosocial/docs/configuring-gotosocial.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server
- (optional) [exim-relay](exim-relay.md) mailer
- (optional) [Postgres](postgres.md) database — GoToSocial will default to [SQLite](https://www.sqlite.org/) if Postgres is not enabled

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# gotosocial                                                           #
#                                                                      #
########################################################################

gotosocial_enabled: true

# Hostname that this server will be reachable at.
# DO NOT change this after your server has already run once, or you will break things!
# Examples: ["gts.example.org","some.server.com"]
gotosocial_hostname: gotosocial.example.com

########################################################################
#                                                                      #
# /gotosocial                                                          #
#                                                                      #
########################################################################
```

### Set a shorter domain for your handle (optional)

On ActivityPub-powered platforms like GoToSocial, the user handle consists of two parts: username and server. For example, if your handle is `@user@gotosocial.example.com`, `user` is the username and `gotosocial.example.com` indicates the server.

By default, GoToSocial uses `gotosocial_hostname` that you provide for the server's domain, but you can use a shorter one without the subdomain (`example.com`). See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-gotosocial/blob/main/docs/configuring-gotosocial.md#set-a-shorter-domain-for-your-handle-optional) on the role's documentation for details about how to set it up.

> [!WARNING]
> Configuring it must be done before starting GoToSocial for the first time. Once you have federated with someone, you cannot change your domain layout.

### Select database to use (optional)

By default GoToSocial is configured to use Postgres, but you can choose SQLite.

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-gotosocial/blob/main/docs/configuring-gotosocial.md#specify-database-optional) on the role's documentation for details.

### Configuring the mailer (optional)

On GoToSocial you can set up a mailer for functions such as password recovery. If you enable the [exim-relay](exim-relay.md) service in your inventory configuration, the playbook will automatically configure it as a mailer for the service.

To actually have the service use (and get messages sent through the exim-relay service), you will need to adjust settings on the service's UI after the service is installed.

>[!WARNING]
> Without setting an authentication method such as DKIM, SPF, and DMARC for your hostname, emails are most likely to be quarantined as spam at recipient's mail servers. The worst scenario is that your server's IP address or hostname will be included in the spam list such as the one managed by [Spamhaus](https://www.spamhaus.org/), depending on the reputation. As the exim-relay service supports DKIM signing, refer to [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay/blob/main/docs/configuring-exim-relay.md#enable-dkim-support-optional) for details about how to set it up.

## Usage

After installation, the GoToSocial instance becomes available at the URL specified with `gotosocial_hostname`. With the configuration above, the service is hosted at `https://gotosocial.example.com`.

To get started, create **an administrator user** first and open the URL with a web browser to log in to the instance. You can run the playbook with the `create-admin-gotosocial` or `ensure-gotosocial-users-created` tag to create users. See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-gotosocial/blob/main/docs/configuring-gotosocial.md#creating-users) on the role's documentation for details.

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-gotosocial/blob/main/docs/configuring-gotosocial.md#usage) on the role's documentation for details about how to use a CLI tool, etc.

## Migrate an existing instance

You can migrate your existing GoToSocial instance to the server which you manage with the MASH playbook. It is also possible to migrate on the same server (from an existing GoToSocial instance to the new one to start managing it with the MASH playbook, for example).

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-gotosocial/blob/main/docs/configuring-gotosocial.md#migrate-an-existing-instance) on the role's documentation for details.

## Related services

- [Funkwhale](funkwhale.md) — Community-driven project that lets you listen and share music and audio in the Fediverse
- [Misskey](misskey.md) — Free decentralized microblogging platform based on the ActivityPub protocol
- [PeerTube](peertube.md) — Tool for sharing online videos
