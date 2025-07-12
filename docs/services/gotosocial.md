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

# GoToSocial

The playbook can install and configure [GotoSocial](https://gotosocial.org/) for you.

GoToSocial is a self-hosted [ActivityPub](https://activitypub.rocks/) social network server. With GoToSocial, you can keep in touch with your friends, post, read, and share images and articles.

See the project's [documentation](https://docs.gotosocial.org/) to learn what GotoSocial does and why it might be useful to you.

For details about configuring the [Ansible role for GoToSocial](https://github.com/mother-of-all-self-hosting/ansible-role-gotosocial), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-gotosocial/blob/main/docs/configuring-gotosocial.md) online
- 📁 `roles/galaxy/gotosocial/docs/configuring-gotosocial.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- a [Postgres](postgres.md) database
- a [Traefik](traefik.md) reverse-proxy server
- (optional) the [exim-relay](exim-relay.md) mailer

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
gotosocial_hostname: 'social.example.com'

########################################################################
#                                                                      #
# /gotosocial                                                          #
#                                                                      #
########################################################################
```

### Set a shorter domain for your handle (optional)

On ActivityPub-powered platforms like GoToSocial, the user handle consists of two parts: username and server. For example, if your handle is `@user@social.example.com`, `user` is the username and `social.example.com` indicates the server.

By default, GoToSocial uses `gotosocial_hostname` that you provide for the server's domain, but you can use a shorter one without the subdomain (`example.com`). See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-gotosocial/blob/main/docs/configuring-gotosocial.md#set-a-shorter-domain-for-your-handle-optional) on the role's documentation for details about how to set it up.

> [!WARNING]
> Configuring it must be done before starting GoToSocial for the first time. Once you have federated with someone, you cannot change your domain layout.

## Usage

After running the command for installation, you can create user account(s).

Run this command to create an **administrator** user account:

```sh
just run-tags gotosocial-add-admin --extra-vars=username=USERNAME_HERE --extra-vars=password=PASSWORD_HERE --extra-vars=email=EMAIL_ADDRESS_HERE
```

Run this command to create a **regular** (non-administrator) user account:

```sh
just run-tags gotosocial-add-user --extra-vars=username=USERNAME_HERE --extra-vars=password=PASSWORD_HERE --extra-vars=email=EMAIL_ADDRESS_HERE
```

Now you should be able to visit the URL at the specified hostname like `https://social.example.com` and check your instance.

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-gotosocial/blob/main/docs/configuring-gotosocial.md#usage) on the role's documentation for details about how to use a CLI tool, etc.

## Migrate an existing instance

You can migrate your existing GoToSocial instance to the server which you manage with the MASH playbook. It is also possible to migrate on the same server (from an existing GoToSocial instance to the new one to start managing it with the MASH playbook, for example).

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-gotosocial/blob/main/docs/configuring-gotosocial.md#migrate-an-existing-instance) on the role's documentation for details.
