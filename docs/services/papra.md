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

# Papra

The playbook can install and configure [Papra](https://github.com/papra-hq/papra) for you.

Papra is a document management and archiving platform.

See the project's [documentation](https://docs.papra.app/) to learn what Papra does and why it might be useful to you.

For details about configuring the [Ansible role for Papra](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az2LGSfc7ziSKvErzZAQdTyTQ4sJcs), you can check them via:
- 🌐 [the role's documentation](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az2LGSfc7ziSKvErzZAQdTyTQ4sJcs/tree/docs/configuring-papra.md) online
- 📁 `roles/galaxy/papra/docs/configuring-papra.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server
- (optional) [exim-relay](exim-relay.md) mailer

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# papra                                                                #
#                                                                      #
########################################################################

papra_enabled: true

papra_hostname: papra.example.com

########################################################################
#                                                                      #
# /papra                                                               #
#                                                                      #
########################################################################
```

**Note**: hosting Papra under a subpath (by configuring the `papra_path_prefix` variable) does not seem to be possible due to Papra's technical limitations.

### Set a random string

You also need to set a random string to the variable as below by adding the following configuration to your `vars.yml` file. The value can be generated with `pwgen -s 64 1` or in another way.

```yaml
papra_environment_variables_auth_secret: YOUR_SECRET_KEY_HERE
```

### Enabling signing up

By default account registration for the service is disabled. To enable it, add the following configuration to your `vars.yml` file:

```yaml
papra_environment_variables_auth_is_registration_enabled: true
```

### Configuring the mailer (optional)

On Papra you can set up a mailer for functions such as password recovery. The service is compatible with SMTP and [Resend](https://resend.com/).

If you enable the [exim-relay](exim-relay.md) service in your inventory configuration, the playbook will automatically configure it as a SMTP mailer for the service.

To actually have the service use (and get messages sent through the exim-relay service), you will need to adjust settings on the service's UI after the service is installed.

>[!WARNING]
> Without setting an authentication method such as DKIM, SPF, and DMARC for your hostname, emails are most likely to be quarantined as spam at recipient's mail servers. The worst scenario is that your server's IP address or hostname will be included in the spam list such as the one managed by [Spamhaus](https://www.spamhaus.org/), depending on the reputation. As the exim-relay service supports DKIM signing, refer to [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay/blob/main/docs/configuring-exim-relay.md#enable-dkim-support-optional) for details about how to set it up.

## Usage

After installation, the Papra instance becomes available at the URL specified with `papra_hostname`. With the configuration above, the service is hosted at `https://papra.example.com`.

To get started, open the URL with a web browser to create an account.

Since account registration is disabled by default, you need to enable it first by setting `papra_environment_variables_auth_is_registration_enabled` to `true` temporarily in order to create your own account.

## Troubleshooting

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az2LGSfc7ziSKvErzZAQdTyTQ4sJcs/tree/docs/configuring-papra.md#troubleshooting) on the role's documentation for details.

## Related services

- [Paperless-ngx](paperless-ngx.md) — Document management system that transforms your physical documents into a searchable online archive
