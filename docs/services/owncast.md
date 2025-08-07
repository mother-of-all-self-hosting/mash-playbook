<!--
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Owncast

[Owncast](https://owncast.online/) is a free and open source live video and web chat server for use with existing popular broadcasting software. This playbook can install owncast, powered by the [mother-of-all-self-hosting/ansible-role-owncast](https://github.com/mother-of-all-self-hosting/ansible-role-owncast) Ansible role.


## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# owncast                                                              #
#                                                                      #
########################################################################

owncast_enabled: true

owncast_hostname: owncast.example.com

########################################################################
#                                                                      #
# /owncast                                                             #
#                                                                      #
########################################################################
```


### Networking

By default, the following ports will be exposed by the container on **all network interfaces**:

- `1935` over **TCP**, controlled by `owncast_container_rtmp_bind_port` — used for TCP based [RTMP](https://en.wikipedia.org/wiki/Real-Time_Messaging_Protocol)

Docker automatically opens this port in the server's firewall, so you **likely don't need to do anything**. If you use another firewall in front of the server, you may need to adjust it.

## Usage

After running the command for installation, the Owncast instance becomes available at the URL specified with `owncast_hostname`. With the configuration above, the service is hosted at `https://owncast.example.com`.

To customize your installation visit `owncast.example.com/admin`. **You should immediately change the stream key which is set to `abc123` by default**.
