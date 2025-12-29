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
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 Thomas Miceli
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# PruneMate

The playbook can install and configure [PruneMate](https://github.com/anoniemerd/PruneMate) for you.

PruneMate is a web interface to automatically clean up Docker resources on a schedule by making use of Docker's native `prune` commands.

See the project's [documentation](https://github.com/anoniemerd/PruneMate/blob/main/README.md) to learn what PruneMate does and why it might be useful to you.

For details about configuring the [Ansible role for PruneMate](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3AzTsddBnXnhE3i4xhzsEX12deb4fx), you can check them via:
- 🌐 [the role's documentation](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3AzTsddBnXnhE3i4xhzsEX12deb4fx/tree/docs/configuring-prunemate.md) online
- 📁 `roles/galaxy/prunemate/docs/configuring-prunemate.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server
- (optional) docker-socket-proxy — required on the default configuration
- (optional) [Gotify](gotify.md)
- (optional) [ntfy](ntfy.md)

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# prunemate                                                            #
#                                                                      #
########################################################################

prunemate_enabled: true

prunemate_hostname: prunemate.example.com

########################################################################
#                                                                      #
# /prunemate                                                           #
#                                                                      #
########################################################################
```

### Setting up authentication

The playbook by default enables authentication implemented by the service. It supports the HTTP Basic authentication with Traefik as well. Though it is optional and can be disabled, **it is strongly encouraged to enable a certain authentication mechanism**, considering the nature of the service. See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad:zTsddBnXnhE3i4xhzsEX12deb4fx/tree/docs/configuring-prunemate.md#setting-up-authentication) on the role's documentation for details about how to set up authentication.

### Configuring Docker socket (optional)

By default the service is configured to use [docker-socket-proxy](https://github.com/Tecnativa/docker-socket-proxy). If you wish to use the Docker socket at `/var/run/docker.sock` directly for some reason, make sure to adjust the `prunemate_docker_endpoint_is_unix_socket` variable to `true`.

## Usage

After running the command for installation, the PruneMate instance becomes available at the URL specified with `prunemate_hostname`. With the configuration above, the service is hosted at `https://prunemate.example.com`.

To get started, open the URL with a web browser, and edit settings to enable a scheduled job.

Because the service is configured to use docker-socket-proxy which this playbook installs, you can set `tcp://mash-container-socket-proxy:2375` to the input area of the URL to add a new Docker host, unless the Docker socket at `/var/run/docker.sock` would be used instead of the proxy.

As a notification provider, it is possible to use Gotify and ntfy, both of which are supported by this playbook, along with Discord and Telegram. To use ntfy, make sure to create a topic at first, so that the PruneMate instance will send notifications to it. The URL of the ntfy instance should be set to `http://mash-ntfy:8080`. Gotify could be configured in a similar way.

💡 You can enable the web app of ntfy to configure and receive notifications on a web browser. Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-ntfy/blob/main/docs/configuring-ntfy.md#enable-web-app-optional) on the role's documentation for details about how to enable it.

To enable authentication, see [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3AzTsddBnXnhE3i4xhzsEX12deb4fx/tree/docs/configuring-prunemate.md#creating-a-user) on the role's documentation about how to create a user. Make sure to start the service first, before creating the user.

## Troubleshooting

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3AzTsddBnXnhE3i4xhzsEX12deb4fx/tree/docs/configuring-prunemate.md#troubleshooting) on the role's documentation for details.

## Related services

- [Gotify](gotify.md) — Simple server for sending and receiving messages
- [ntfy](ntfy.md) — Simple HTTP-based pub-sub notification service
