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

# Mailpit

The playbook can install and configure [Mailpit](https://mailpit.axllent.org/) for you.

Mailpit is the SMTP server which catches any messages sent to it and displays in a web interface instead of sending it to the outside of the internal network, making it possible to check messages without using an actual email address. It also implements [POP3 server](https://mailpit.axllent.org/docs/configuration/pop3/) to download captured messages directly to your email client, [spam checker](https://mailpit.axllent.org/docs/usage/spamassassin/) to check how much possible messages will be detected as spam, etc.

While the service is primarily intended to be used for testing (bulk mail sending simulation, etc), it can also be used to receive messages from other services of this playbook directly, improving the security related to sensitive information such as a temporary password.

See the project's [documentation](https://mailpit.axllent.org/docs/) to learn what Mailpit does and why it might be useful to you.

For details about configuring the [Ansible role for Mailpit](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az3BKJz8wwtQHfXm8MPX81h4izT2QS), you can check them via:
- 🌐 [the role's documentation](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az3BKJz8wwtQHfXm8MPX81h4izT2QS/tree/docs/configuring-mailpit.md) online
- 📁 `roles/galaxy/mailpit/docs/configuring-mailpit.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# mailpit                                                              #
#                                                                      #
########################################################################

mailpit_enabled: true

mailpit_hostname: mailpit.example.com

########################################################################
#                                                                      #
# /mailpit                                                             #
#                                                                      #
########################################################################
```

### Configuring HTTP Basic authentication

The HTTP Basic authentication on Traefik is enabled for the web interface by default, considering the nature of the service. See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az3BKJz8wwtQHfXm8MPX81h4izT2QS/tree/docs/configuring-mailpit.md#web-ui) on the role's documentation for details about how to set it up or disable it.

### Configuring POP3 server (optional)

While the SMTP server can be used without setting credentials, **the POP3 server requires you to specify a pair of username and password**. See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az3BKJz8wwtQHfXm8MPX81h4izT2QS/tree/docs/configuring-mailpit.md#pop3-server) on the role's documentation for details.

### Integrating with Prometheus (optional)

Mailpit can natively expose metrics to [Prometheus](prometheus.md).

#### Expose metrics internally

If Mailpit and Prometheus do not share a network (like Traefik), you can connect the Mailpit container network to Prometheus by adding the following configuration to your `vars.yml` file:

```yaml
prometheus_container_additional_networks_custom:
  - "{{ mailpit_container_network }}"
```

#### Expose metrics publicly

If Mailpit metrics are not scraped from a local Prometheus instance, you can expose the metrics publicly so that a remote instance can fetch them.

When exposing metrics publicly, you should consider to set up [HTTP Basic Authentication](https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication) **or anyone would be able to read your metrics**.

To expose the metrics publicly, add the following configuration to your `vars.yml` file (adapt to your needs):

```yaml
mash_playbook_metrics_exposure_enabled: true
mash_playbook_metrics_exposure_hostname: mash.example.com
```

It will expose the metrics at `https://mash.example.com/metrics/mash-mailpit`.

To enable the HTTP Basic authentication, add the following configuration to your `vars.yml` file (adapt to your needs):

```yaml
mailpit_container_labels_traefik_metrics_middleware_basic_auth_enabled: true

# See https://doc.traefik.io/traefik/middlewares/http/basicauth/#users for details.
mailpit_container_labels_traefik_metrics_middleware_basic_auth_users: ""
```

## Usage

After running the command for installation, the Mailpit instance becomes available at the hostname `mash-mailpit`. Its web interface is hosted at `https://mailpit.example.com`, with the configuration above.

### Configuring SMTP server settings

To use Mailpit with other services of this playbook, you can configure the setting about the SMTP server to point it to `mash-mailpit` with the port number `1025`. As Mailpit just works on the same network as those services do, you can set any random email address (even nonexistent one like `example@example.com` or `a@a.com`) to the service.

For example, you can get the [asciinema server](asciinema-server.md) send logging in or user registration messages to Mailpit by adding the following configuration to your `vars.yml` file, so that the service will use the SMTP server instead of the default [exim-relay](exim-relay.md) mailer:

```yaml
asciinema_server_mailer_enabled: true
asciinema_server_environment_variable_smtp_host: "{{ mailpit_identifier }}"
asciinema_server_environment_variable_smtp_port: 1025
asciinema_server_environment_variable_mail_from_address: SET_ANY_EMAIL_ADDRESS_HERE
```

You can check the message sent by the asciinema server at `https://mailpit.example.com`.

💡 Since the message is not sent to the outside of the internal Docker network, the chance of man-in-the-middle attacks is drastically reduced.

### Using POP3 server

To download messages from the POP3 server, you can configure your email client so that it connects to `mailpit.example.com` via the port **1110**. Make sure to set the username and password for authentication.

## Troubleshooting

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az3BKJz8wwtQHfXm8MPX81h4izT2QS/tree/docs/configuring-mailpit.md#troubleshooting) on the role's documentation for details.

## Related services

- [MailCatcher](mailcatcher.md) — SMTP server which catches any message sent to it and displays in a web interface
- [MailCrab](mailcrab.md) — SMTP server written in Rust, which catches any message sent to it and displays in a web interface; drop-in replacement of MailCatcher
