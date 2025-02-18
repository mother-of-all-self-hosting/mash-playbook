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

The Ansible role for Jitsi is developed and maintained by [MASH (mother-of-all-self-hosting) project](https://github.com/mother-of-all-self-hosting/ansible-role-jitsi). For details about configuring Jitsi, you can check them via:
- [the role's documentation at the MASH project](https://github.com/mother-of-all-self-hosting/ansible-role-jitsi/blob/main/docs/configuring-jitsi.md)
- `roles/galaxy/jitsi/docs/configuring-jitsi.md` locally, if you have [fetched the Ansible roles](installing.md#update-ansible-roles)

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

### (Optional) Making your Jitsi server work on a LAN

By default the Jitsi Meet instance does not work with a client in LAN (Local Area Network), even if others are connected from WAN. There are no video and audio. In the case of WAN to WAN everything is ok.

The reason is the Jitsi VideoBridge git to LAN client the IP address of the docker image instead of the host. The [documentation](https://jitsi.github.io/handbook/docs/devops-guide/devops-guide-docker/#running-behind-nat-or-on-a-lan-environment) of Jitsi in docker suggest to add `JVB_ADVERTISE_IPS` in enviornment variable to make it work.

Here is how to do it in the playbook.

Use the following **additional** configuration:

```yaml
jitsi_jvb_container_extra_arguments:
  - '--env "JVB_ADVERTISE_IPS=<Local IP address of the host>"'
```

### Additional configuration

#### (Optional) Fine tune Jitsi

Sample **additional** configuration to save up resources (explained below):

```yaml
jitsi_web_custom_config_extension: |
  config.enableLayerSuspension = true;

  config.disableAudioLevels = true;

  // Limit the number of video feeds forwarded to each client
  config.channelLastN = 4;

jitsi_web_config_resolution_width_ideal_and_max: 480
jitsi_web_config_resolution_height_ideal_and_max: 240
```

You may want to **suspend unused video layers** until they are requested again, to save up resources on both server and clients.
Read more on this feature [here](https://jitsi.org/blog/new-off-stage-layer-suppression-feature/)

You may wish to **disable audio levels** to avoid excessive refresh of the client-side page and decrease the CPU consumption involved.

You may want to **limit the number of video feeds forwarded to each client**, to save up resources on both server and clients. As clients' bandwidth and CPU may not bear the load, use this setting to avoid lag and crashes.
This feature is found by default in other webconference applications such as Office 365 Teams (limit is set to 4).
Read how it works [here](https://github.com/jitsi/jitsi-videobridge/blob/master/doc/last-n.md) and performance evaluation on this [study](https://jitsi.org/wp-content/uploads/2016/12/nossdav2015lastn.pdf).

You may want to **limit the maximum video resolution**, to save up resources on both server and clients.

#### (Optional) Specify a Max number of participants on a Jitsi conference

The playbook allows a user to set a max number of participants allowed to join a Jitsi conference. By default there is no limit.

In order to set the max number of participants use the following **additional** configuration:

```yaml
jitsi_prosody_max_participants: 4 # example value
```


#### (Optional) Disable Gravatar

In the default upstream Jisti Meet configuration, [gravatar.com](https://gravatar.com/) is enabled as an avatar service. This results in third party request leaking data to Gravatar.

To disable Gravatar integration, use the following **additional** configuration:

```yaml
jitsi_disable_gravatar: false
```

## Usage

After installation, you can go to the [Jitsi URL](#url) and start an audio/video conference.


## Troubleshooting

### Rebuilding your Jitsi installation

**If you ever run into any trouble** or **if you change configuration (`jitsi_*` variables) too much**, we urge you to rebuild your Jitsi setup.

We normally don't require such manual intervention for other services, but Jitsi services generate a lot of configuration files on their own.

These files are not all managed by Ansible (at least not yet), so you may sometimes need to delete them all and start fresh.

To rebuild your Jitsi configuration:

- ask Ansible to stop all Jitsi services: `just run-tags stop-group --extra-vars=group=jitsi`
- SSH into the server and do this and remove all Jitsi configuration & data (`rm -rf /mash/jitsi`)
- ask Ansible to set up Jitsi anew and restart services (`just install-service jitsi`)
