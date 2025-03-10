<!--
SPDX-FileCopyrightText: 2018 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2019 Eduardo Beltrame
SPDX-FileCopyrightText: 2020 - 2025 MDAD project contributors
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Exim-relay

Various services need to send out email.

The default playbook configuration (`examples/vars.yml`) recommends that you enable the Exim relay SMTP mailer service (powered by [exim-relay](https://github.com/devture/exim-relay) and the [ansible-role-exim-relay](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay) Ansible role). Enabling this service **automatically wires various other services to send email through it**. Exim-relay then gives you a centralized place for configuring email-sending.

The [Ansible role for exim-relay](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay) is developed and maintained by the MASH project. For details about configuring exim-relay, you can check them via:
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

exim_relay_enabled: true

exim_relay_hostname: mash.example.com

exim_relay_sender_address: "someone@{{ exim_relay_hostname }}"

########################################################################
#                                                                      #
# /exim_relay                                                          #
#                                                                      #
########################################################################
```

### Enable DKIM authentication to improve deliverability (optional)

By default, exim-relay attempts to deliver emails directly. This may or may not work, depending on your domain configuration.

To improve email deliverability, you can configure authentication methods such as DKIM (DomainKeys Identified Mail), SPF, and DMARC for your domain. Without setting any of these authentication methods, your outgoing email is most likely to be quarantined as spam at recipient's mail servers.

For details about configuring DKIM, refer [this section](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay/blob/main/docs/configuring-exim-relay.md#enable-dkim-support-optional) on the role's documentation.

💡 If you cannot enable DKIM, SPF, or DMARC on your domain for some reason, we recommend relaying email through another SMTP server.

### Relaying email through another SMTP server (optional)

**On some cloud providers such as Google Cloud, [port 25 is always blocked](https://cloud.google.com/compute/docs/tutorials/sending-mail/), so sending email directly from your server is not possible.** In this case, you will need to relay email through another SMTP server.

For details about configuration, refer [this section](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay/blob/main/docs/configuring-exim-relay.md#relaying-email-through-another-smtp-server) on the role's document.

### Using a per-service sender address (optional)

By default, all roles that this playbook wires to `exim-relay` will all be configured to send emails using a `From` address as configured in `exim_relay_sender_address`.

To configure a given service to use another sender address, override the specific variables for the given service.

For example, to make [Vaultwarden](vaultwarden.md) (automatically wired to send via `exim-relay` if you have it enabled) send emails from a custom address (instead of the default, `exim_relay_sender_address`), add the following configuration to your `vars.yml` file:

```yml
vaultwarden_config_smtp_from: vaultwarden@example.com
```

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay/blob/main/docs/configuring-exim-relay.md#troubleshooting) on the role's documentation for details.
