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
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# ntfy

The playbook can install and configure the [ntfy](https://ntfy.sh/) (pronounced "notify") push notifications server for you.

ntfy lets you send push notifications to your phone or desktop via scripts from any computer, using simple HTTP PUT or POST requests. It enables you to send/receive notifications, without relying on servers owned and controlled by third parties.

See the project's [documentation](https://docs.ntfy.sh/) to learn what it does and why it might be useful to you.

The [Ansible role for ntfy](https://github.com/mother-of-all-self-hosting/ansible-role-ntfy) is developed and maintained by the MASH project. For details about configuring ntfy, you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-ntfy/blob/main/docs/configuring-ntfy.md) online
- 📁 `roles/galaxy/ntfy/docs/configuring-ntfy.md` locally, if you have [fetched the Ansible roles](../installing.md)

**Note**: you need to install [the ntfy Android/iOS app](https://docs.ntfy.sh/subscribe/phone/) on your device in order to receive push notifications from the ntfy server. Notifications can also be sent/received on the ntfy's web app if it is enabled (disabled by default). Refer [this section](#usage) for details about how to use the apps.

### How ntfy works with UnifiedPush

⚠️ [UnifiedPush does not work on iOS.](https://unifiedpush.org/users/faq/#will-unifiedpush-ever-work-on-ios)

ntfy implements [UnifiedPush](https://unifiedpush.org), the standard which makes it possible to send and receive push notifications without using Google's Firebase Cloud Messaging (FCM) service.

Working as a **Push Server**, a ntfy server can forward messages to a **Distributor** running on Android and other devices (see [here](https://unifiedpush.org/users/distributors/#definitions) for the definition of the Push Server and the Distributor).

This role installs and manages a self-hosted ntfy server as the Push Server, which the Distributor (such as the ntfy Android app) on your device listens to.

Your UnifiedPush-compatible applications (such as [Tusky](https://tusky.app/) and [DAVx⁵](https://www.davx5.com/)) listen to the Distributor, and push notitications are "distributed" from it. This means that the UnifiedPush-compatible applications cannot receive push notifications from the Push Server without the Distributor.

As the ntfy Android app functions as the Distributor too, you do not have to install something else on your device.

💡 **Notes**:
- Refer [this official documentation of UnifiedPush](https://unifiedpush.org/users/troubleshooting/#understand-unifiedpush) for a simple explanation about relationship among UnifiedPush-compatible application, Distributor, Push Server, and the application's server.
- [Here](https://unifiedpush.org/users/apps/) is a non-exhaustive list of the end-user applications that use UnifiedPush.
- Unlike push notifications using Google's FCM or Apple's APNs, each end-user can choose the Push Server which one prefer. This means that deploying a ntfy server cannot enforce a UnifiedPush-compatible application (and its users) to use the exact server.

### iOS instant notification

Because iOS heavily restricts background processing, it is impossible to implement instant push notifications without a central server.

To implement instant notification through the self-hosted ntfy server, see [this official documentation](https://docs.ntfy.sh/config/#ios-instant-notifications) for instructions.

## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server
- (optional) the [exim-relay](exim-relay.md) mailer

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# ntfy                                                                 #
#                                                                      #
########################################################################

ntfy_enabled: true

ntfy_hostname: ntfy.example.com

########################################################################
#                                                                      #
# /ntfy                                                                #
#                                                                      #
########################################################################
```

As the most of the necessary settings for the role have been taken care of by the playbook, you can enable ntfy on your server with this minimum configuration.

See the role's documentation for details about configuring ntfy per your preference (such as [setting access control with authentication](https://github.com/mother-of-all-self-hosting/ansible-role-ntfy/blob/main/docs/configuring-ntfy.md#enable-access-control-with-authentication-optional), [allowing attachments](https://github.com/mother-of-all-self-hosting/ansible-role-ntfy/blob/main/docs/configuring-ntfy.md#allow-attachments-optional), [enabling the web app](https://github.com/mother-of-all-self-hosting/ansible-role-ntfy/blob/main/docs/configuring-ntfy.md#enable-web-app-optional) and [e-mail notification](https://github.com/mother-of-all-self-hosting/ansible-role-ntfy/blob/main/docs/configuring-ntfy.md#enable-e-mail-notification-optional), etc.)

## Usage

To receive push notifications from the ntfy server, you need to **install [the ntfy Android/iOS app](https://docs.ntfy.sh/subscribe/phone/)**, **log in to the account on the ntfy app** if you have enabled the access control, and then **subscribe to a topic** where messages will be published. You can also send/receive notifications on the ntfy's web app at `example.com`.

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-ntfy/blob/main/docs/configuring-ntfy.md#usage) on the role's documentation for details.

If you enable [Uptime Kuma](uptime-kuma.md), the self-hosted monitoring tool (hint: this playbook enables it by default on its example `vars.yml` files), it is possible to set it up to have it send notifications to a topic when the monitored web service is down. You can subscribe to the topic both from the ntfy Android/iOS app and the web app.

### UnifiedPush-compatible application

To receive push notifications on a UnifiedPush-compatible application, it must be able to communicate with the ntfy Android app which works as the Distributor on the same device.

Consult to documentation of applications for instruction about how to enable UnifiedPush support. Note that some applications quietly detect and use the Distributor, so you do not always have to configure the applications.

If you are configuring UnifiedPush on a [Matrix](https://matrix.org) client, you can refer [this section](https://github.com/spantaleev/matrix-docker-ansible-deploy/blob/master/docs/configuring-playbook-ntfy.md#setting-up-a-unifiedpush-compatible-matrix-client) on matrix-docker-ansible-deploy (MDAD) playbook's documentation.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-ntfy/blob/main/docs/configuring-ntfy.md#troubleshooting) on the role's documentation for details.
