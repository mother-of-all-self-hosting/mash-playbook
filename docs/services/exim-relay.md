<!--
SPDX-FileCopyrightText: 2024 Slavi Pantaleev

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Exim-relay

Various services need to send out email.

The default playbook configuration (`examples/vars.yml`) recommends that you enable the Exim relay SMTP mailer service (powered by [exim-relay](https://github.com/devture/exim-relay) and the [ansible-role-exim-relay](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay) Ansible role).

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# exim_relay                                                           #
#                                                                      #
########################################################################

# Various services need to send out email.
#
# Enabling this Exim relay SMTP mailer service automatically wires
# all other services to send email through it.
#
# exim-relay then gives you a centralized place for configuring email-sending.

exim_relay_enabled: true

exim_relay_hostname: mash.example.com

exim_relay_sender_address: "someone@{{ exim_relay_hostname }}"

# By default, exim-relay attempts to deliver emails directly.
# To make it relay via an external SMTP server, see the "Relaying via an external SMTP server" section below.

########################################################################
#                                                                      #
# /exim_relay                                                          #
#                                                                      #
########################################################################
```

Enabling this service, **automatically wires various other services to send email through it**.


**By default, exim-relay attempts to deliver emails directly**. This may work to some extent on some servers, but deliverability may be low.
To make the exim-relay service relay all outgoing emails via an external SMTP server, see [Relaying via an external SMTP server](#relaying-via-an-external-smtp-server)

## Relaying via an external SMTP server

To make the exim-relay service relay all outgoing emails via an external SMTP server, add the following to your `vars.yml` configuration:

```yml
exim_relay_relay_use: true
exim_relay_relay_host_name: smtp.example.com
exim_relay_relay_host_port: 465
exim_relay_relay_auth: true
exim_relay_relay_auth_username: ''
exim_relay_relay_auth_password: ''
```

## Using a per-service sender address

By default, all roles that this playbook wires to `exim-relay` will all be configured to send emails using a `From` address as configured in `exim_relay_sender_address`.

To configure a given service to use another sender address, override the specific variables for the given service.

For example, to make [Vaultwarden](vaultwarden.md) (automatically wired to send via `exim-relay` if you have it enabled) send emails from a custom address (instead of the default, `exim_relay_sender_address`), use configuration like this:
```yml
vaultwarden_config_smtp_from: vaultwarden@example.com
```
