<!--
SPDX-FileCopyrightText: 2020 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2020 - 2024 MDAD project contributors
SPDX-FileCopyrightText: 2020 Aaron Raimist
SPDX-FileCopyrightText: 2020 Mickaël Cornière
SPDX-FileCopyrightText: 2020 Chris van Dijk
SPDX-FileCopyrightText: 2020 Dominik Zajac
SPDX-FileCopyrightText: 2022 François Darveau
SPDX-FileCopyrightText: 2022 Warren Bailey
SPDX-FileCopyrightText: 2023 Antonis Christofides
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Jitsi

The playbook can install and configure the [Jitsi](https://jitsi.org/) video-conferencing platform for you.

The [Ansible role for Jitsi](https://github.com/mother-of-all-self-hosting/ansible-role-jitsi) is developed and maintained by the MASH project. For details about configuring Jitsi, you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-jitsi/blob/main/docs/configuring-jitsi.md) online
- 📁 `roles/galaxy/jitsi/docs/configuring-jitsi.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Prerequisites

Before proceeding, make sure to check server's requirements recommended by [the official deployment guide](https://jitsi.github.io/handbook/docs/devops-guide/devops-guide-requirements).

You may need to open some ports to your server, if you use another firewall in front of the server. Refer [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-jitsi/blob/main/docs/configuring-jitsi.md#prerequisites) to check which ones to be configured.

## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# jitsi                                                                #
#                                                                      #
########################################################################

jitsi_enabled: true

jitsi_hostname: mash.example.com
jitsi_path_prefix: /jitsi

########################################################################
#                                                                      #
# /jitsi                                                               #
#                                                                      #
########################################################################
```

**Since Jitsi's performance heavily depends on server resource (bandwidth, RAM, and CPU), it is recommended to review settings and optimize them as necessary before deployment.** You can check [here](https://github.com/mother-of-all-self-hosting/ansible-role-jitsi/blob/main/docs/configuring-jitsi.md#example-configurations) for an example set of configurations to set up a Jitsi instance, focusing on performance. If you will host a large conference, you probably might also want to consider to provision additional JVBs ([Jitsi VideoBridge](https://github.com/jitsi/jitsi-videobridge)). See [here](https://github.com/mother-of-all-self-hosting/ansible-role-jitsi/blob/main/docs/configuring-jitsi.md#set-up-additional-jvbs-for-more-video-conferences-optional) for details about setting them up with the playbook.

See the role's documentation for details about configuring Jitsi per your preference (such as setting [a custom hostname](https://github.com/mother-of-all-self-hosting/ansible-role-jitsi/blob/main/docs/configuring-jitsi.md#set-the-hostname) and [the environment variable for running Jitsi in a LAN](https://github.com/mother-of-all-self-hosting/ansible-role-jitsi/blob/main/docs/configuring-jitsi.md#configure-jvb_advertise_ips-for-running-behind-nat-or-on-a-lan-environment-optional)).

### Adjusting the Jitsi URL

In the example configuration above, we configure the service to be hosted at `https://mash.example.com/jitsi`.

You can remove the `jitsi_path_prefix` variable definition, to make it default to `/`, so that the service is served at `https://mash.example.com/`.

**Note**: there are minor quirks when hosting under a subpath, such as:

- [When hosting under a subpath, pwa-worker.js is attempted to be loaded from the base domain without a subpath](https://github.com/jitsi/docker-jitsi-meet/issues/1515)
- [When hosting under a subpath, ending the meeting redirects to the base domain without subpath](https://github.com/jitsi/docker-jitsi-meet/issues/1514)

### Enable authentication and guests mode (optional)

By default the Jitsi Meet instance **does not require for anyone to log in, and is open to use without an account**.

If you would like to control who is allowed to start meetings on your instance, you'd need to enable Jitsi's authentication and optionally guests mode.

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-jitsi/blob/main/docs/configuring-jitsi.md#configure-jitsi-authentication-and-guests-mode-optional) on the role's documentation for details about how to configure the authentication and guests mode.

## Usage

After installation, open the specified URL such as `https://mash.example.com/jitsi`, and you can start a videoconference. Note that you'll need to log in to your Jitsi's account if you have configured authentication with `internal` auth.

Check [the official user guide](https://jitsi.github.io/handbook/docs/category/user-guide) for details about how to use Jitsi Meet.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-jitsi/blob/main/docs/configuring-jitsi.md#troubleshooting) on the role's documentation for details.
