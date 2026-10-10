<!--
SPDX-FileCopyrightText: 2020 - 2024 MDAD project contributors
SPDX-FileCopyrightText: 2020 - 2025 Slavi Pantaleev
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
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara
SPDX-FileCopyrightText: 2025 MASH project contributors

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# TSDProxy

The playbook can install and configure [TSDProxy](https://almeidapaulopt.github.io/tsdproxy/) for you.

TSDProxy is an application that automatically creates a proxy to virtual addresses in your [Tailscale](https://tailscale.com/) network.

See the project's [documentation](https://almeidapaulopt.github.io/tsdproxy/docs/) to learn what TSDProxy does and why it might be useful to you.

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# tsdproxy                                                             #
#                                                                      #
########################################################################

tsdproxy_enabled: true

########################################################################
#                                                                      #
# /tsdproxy                                                            #
#                                                                      #
########################################################################
```

### Set authkey for Tailscale

You also need to set an authkey for Tailscale by adding the following configuration to your `vars.yml` file:

```yaml
tsdproxy_tailscale_authkey: '' # OR

tsdproxy_tailscale_authkeyfile: '' # use this to load authkey from file. If this is defined, tsdproxy_tailscale_authkey is ignored
```

Refer to [this page](https://almeidapaulopt.github.io/tsdproxy/docs/advanced/tailscale/) on the official documentation for details.

## Usage

After running the command for installation, the TSDProxy instance becomes available.

If [ansible-role-container-socket-proxy](https://github.com/mother-of-all-self-hosting/ansible-role-container-socket-proxy) is installed by the playbook (default), the container will use the proxy. If not, the container will mount the Docker socket at `/var/run/docker.sock`. You can change the path by configuring `tsdproxy_docker_endpoint`.

Do not forget to adjust the `tsdproxy_docker_endpoint_is_unix_socket` variable to `false` if a TCP endpoint is enabled.

### Adding a new service

This proxy creates a separate Tailscale machine (node) in the Tailscale network for each service, without creating a sidecar container each time.

To add a new service, you have to make sure that the service and proxy are in a same container network. You can do this by adding the proxy to the network of the service or the other way round.

```yaml
tsdproxy_container_additional_networks_custom:
  - YOUR-SERVICE-NETWORK
# OR
YOUR-SERVICE_container_additional_networks_custom:
  - "{{ tsdproxy_container_network }}"
```

The next step is to add the service to the proxy. There are two ways of doing so; one with container labels and the other with a Proxy list.

#### Connecting a service to the proxy via container labels

```yaml
YOUR-SERVICE_container_labels_additional_labels_custom:
  - tsdproxy.enable=true
  - tsdproxy.port.1=443/https:8080/http
```

The port label exposes HTTPS on port 443 of the service's Tailscale node and forwards to HTTP on port 8080 of the container. Additional labels use the same `key=value` format and can be appended to the list above.

The following labels are optional. Please read the [official TSDProxy documentation](https://almeidapaulopt.github.io/tsdproxy/docs/providers/docker/) for more information.

```yaml
  - tsdproxy.name=my-service
  - tsdproxy.proxyprovider=providername
  - tsdproxy.ephemeral=false
```

#### Connecting a service to the proxy via a Proxy list

An alternative way to add a service to the proxy is to use proxy lists.

Please read the [official TSDProxy documentation](https://almeidapaulopt.github.io/tsdproxy/docs/providers/lists/) for more information.

Refer to the [role documentation](https://github.com/Bergruebe/ansible-role-tsdproxy#via-proxy-list) for the configuration format. You will need to use the `tsdproxy_config_lists` variable and add your proxy list file to the directory for configuration files, most likely `/mash/tsdproxy/config/`. It is possible to do so manually or by using [AUX-Files](auxiliary.md).

## Related services

- [Headscale](headscale.md) — Tailscale-compatible control server for managing Tailscale devices
