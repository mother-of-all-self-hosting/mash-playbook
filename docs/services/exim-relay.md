<!--
SPDX-FileCopyrightText: 2018 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2019 Eduardo Beltrame
SPDX-FileCopyrightText: 2020 - 2025 MDAD project contributors
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Exim-relay

Various services need to send out email.

The default playbook configuration (`examples/vars.yml`) recommends that you enable the Exim relay SMTP mailer service (powered by [exim-relay](https://github.com/devture/exim-relay) and the [ansible-role-exim-relay](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay) Ansible role).

The Ansible role for exim-relay is developed and maintained by [the MASH project](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay). For details about configuring exim-relay, you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay/blob/main/docs/configuring-exim-relay.md) online
- 📁 `roles/galaxy/exim_relay/docs/configuring-exim-relay.md` locally, if you have [fetched the Ansible roles](../installing.md)

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

### Relaying email through another SMTP server (optional)

By default, exim-relay attempts to deliver emails directly. This may or may not work, depending on your domain configuration (SPF settings, etc.)

**On some cloud providers such as Google Cloud, [port 25 is always blocked](https://cloud.google.com/compute/docs/tutorials/sending-mail/), so sending email directly from your server is not possible.** In this case, you will need to relay email through another SMTP server.

For details about configuration, refer [this section](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay/blob/main/docs/configuring-exim-relay.md#relaying-email-through-another-smtp-server) on the role's document.

💡 To improve deliverability, we recommend relaying email through another SMTP server anyway.

## Using a per-service sender address

By default, all roles that this playbook wires to `exim-relay` will all be configured to send emails using a `From` address as configured in `exim_relay_sender_address`.

To configure a given service to use another sender address, override the specific variables for the given service.

For example, to make [Vaultwarden](vaultwarden.md) (automatically wired to send via `exim-relay` if you have it enabled) send emails from a custom address (instead of the default, `exim_relay_sender_address`), use configuration like this:
```yml
vaultwarden_config_smtp_from: vaultwarden@example.com
```

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay/blob/main/docs/configuring-exim-relay.md#troubleshooting) on the role's documentation for details.
