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
SPDX-FileCopyrightText: 2023 Niels Bouma
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Changedetection.io

The playbook can install and configure [Changedetection.io](https://github.com/dgtlmoon/changedetection.io) for you.

Changedetection.io is a simple website change detection and restock monitoring solution.

See the project's [documentation](https://github.com/dgtlmoon/changedetection.io/blob/master/README.md) to learn what Changedetection.io does and why it might be useful to you.

For details about configuring the [Ansible role for Changedetection.io](https://github.com/mother-of-all-self-hosting/ansible-role-changedetection), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-changedetection/blob/main/docs/configuring-changedetection.md) online
- 📁 `roles/galaxy/changedetection/docs/configuring-changedetection.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server
- (optional) Notification services which [Apprise API](apprise.md) supports, including [exim-relay](exim-relay.md) mailer, [Gotify](gotify.md), and [ntfy](ntfy.md)

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# Changedetection.io                                                   #
#                                                                      #
########################################################################

changedetection_enabled: true

changedetection_hostname: mash.example.com
changedetection_path_prefix: /changedetection

########################################################################
#                                                                      #
# /Changedetection.io                                                  #
#                                                                      #
########################################################################
```

### Enable Playwright webdriver for advanced options (optional)

Some advanced options like using Javascript or the Visual Selector tool require an additional Playwright webdriver. See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-changedetection/blob/main/docs/configuring-changedetection.md#enable-playwright-webdriver-for-advanced-options-optional) on the role's documentation for details.

## Usage

After running the command for installation, the Changedetection.io instance becomes available at the URL specified with `changedetection_hostname` and `changedetection_path_prefix`. With the configuration above, the service is hosted at `https://mash.example.com/changedetection`.

### Configuring notification services (optional)

On Changedetection.io you can add configuration settings of notification services. If you enable the ones which [Apprise API](apprise.md) supports in your inventory configuration, including [exim-relay](exim-relay.md) as a SMTP server, [Gotify](gotify.md), and [ntfy](ntfy.md), the playbook will automatically connect them to the Changedetection.io service.

As the Changedetection.io instance does not support configuring the notification services with environment variables, you can add default options for them on its UI. Refer to [this page](https://github.com/dgtlmoon/changedetection.io/wiki/Notification-configuration-notes) on the official documentation as well about how to configure them.

To set up notification URLs, open `https://mash.example.com/changedetection/settings#notifications` and add entries by following [the Apprise's URL format](https://github.com/caronc/apprise/blob/master/README.md#supported-notifications). For example, you can have the service send notifications to the ntfy service by adding a line as below:

```
ntfy://YOUR_NTFY_USERNAME_HERE:YOUR_NTFY_PASSWORD_HERE@mash-ntfy:8080/YOUR_NTFY_TOPIC_HERE
```

After setting the configuration, you can have the Changedetection.io instance send a test notification.

>[!WARNING]
> Without setting an authentication method such as DKIM, SPF, and DMARC for your hostname, emails are most likely to be quarantined as spam at recipient's mail servers. The worst scenario is that your server's IP address or hostname will be included in the spam list such as the one managed by [Spamhaus](https://www.spamhaus.org/), depending on the reputation. As the exim-relay service supports DKIM signing, refer to [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay/blob/main/docs/configuring-exim-relay.md#enable-dkim-support-optional) for details about how to set it up.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-changedetection/blob/main/docs/configuring-changedetection.md#troubleshooting) on the role's documentation for details.
