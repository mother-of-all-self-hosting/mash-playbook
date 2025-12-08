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

# MailCatcher

The playbook can install and configure [MailCatcher](https://mailcatcher.me) for you.

MailCatcher is the SMTP server which catches any message sent to it and displays in a web interface instead of sending it to the outside of the internal network, making it possible to check messages without using an actual email address.

See the project's [documentation](https://mailcatcher.me) to learn what MailCatcher does and why it might be useful to you.

For details about configuring the [Ansible role for MailCatcher](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az3QmarrgiC7ZGmd7UCTW2EZTheCZb), you can check them via:
- 🌐 [the role's documentation](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az3QmarrgiC7ZGmd7UCTW2EZTheCZb/tree/docs/configuring-mailcatcher.md) online
- 📁 `roles/galaxy/mailcatcher/docs/configuring-mailcatcher.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# mailcatcher                                                          #
#                                                                      #
########################################################################

mailcatcher_enabled: true

mailcatcher_hostname: mailcatcher.example.com

########################################################################
#                                                                      #
# /mailcatcher                                                         #
#                                                                      #
########################################################################
```

**Note**: hosting MailCatcher's web interface under a subpath (by configuring the `mailcatcher_path_prefix` variable) does not seem to be possible due to MailCatcher's technical limitations.

### Configuring HTTP Basic authentication

Since there does not exist an authentication system on the web interface, the HTTP Basic authentication on Traefik is enabled for the web interface by default, considering the nature of the service. See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az3QmarrgiC7ZGmd7UCTW2EZTheCZb/tree/docs/configuring-mailcatcher.md#configuring-http-basic-authentication) on the role's documentation for details about how to set it up.

## Usage

After running the command for installation, the MailCatcher instance becomes available at the hostname `mash-mailcatcher`. Its web interface is hosted at `https://mailcatcher.example.com`, with the configuration above.

### Configuring SMTP server settings

To use MailCatcher with other services of this playbook, you can configure the setting about the SMTP server to point it to `mash-mailcatcher` with the port number `1025`. As MailCatcher just works on the same network as those services do, you can set any random email address (even nonexistent one like `example@example.com` or `a@a.com`) to the service.

For example, you can get the [asciinema server](asciinema-server.md) send logging in or user registration messages to MailCatcher by adding the following configuration to your `vars.yml` file, so that the service will use the SMTP server instead of the default [exim-relay](exim-relay.md) mailer:

```yaml
asciinema_server_mailer_enabled: true
asciinema_server_environment_variable_smtp_host: "{{ mailcatcher_identifier }}"
asciinema_server_environment_variable_smtp_port: 1025
asciinema_server_environment_variable_mail_from_address: SET_ANY_EMAIL_ADDRESS_HERE
```

You can check the message sent by the asciinema server at `https://mailcatcher.example.com`.

💡 Since the message is not sent to the outside of the internal Docker network, the chance of man-in-the-middle attacks is drastically reduced.

>[!NOTE]
> Messages are not stored in the persistent storage. They will disappear after the container was stopped or removed.

## Troubleshooting

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az3QmarrgiC7ZGmd7UCTW2EZTheCZb/tree/docs/configuring-mailcatcher.md#troubleshooting) on the role's documentation for details.

## Related services

- [MailCrab](mailcrab.md) — SMTP server written in Rust, which catches any message sent to it and displays in a web interface; drop-in replacement of MailCatcher
