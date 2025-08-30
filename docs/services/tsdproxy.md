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

## Adjusting the playbook configuration

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

See [this page](https://almeidapaulopt.github.io/tsdproxy/docs/advanced/tailscale/) on the official documentation for details.

## Usage

After running the command for installation, the TSDProxy instance becomes available.

If [ansible-role-container-socket-proxy](https://github.com/mother-of-all-self-hosting/ansible-role-container-socket-proxy) is installed by the playbook (default), the container will use the proxy. If not, the container will mount the docker socket at `/var/run/docker.sock`. You can change it by configuring `tsdproxy_docker_socket`.

Do not forget to adjust the `tsdproxy_docker_endpoint_is_unix_socket` to `false` if a TCP endpoint is enabled.

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
YOUR-SERVICE_container_labels_additional_labels: |
  tsdproxy.enable: "true"
  tsdproxy.container_port: 8080
```

The following labels are optional. Please read the [official TSDProxy documentation](https://almeidapaulopt.github.io/tsdproxy/docs/docker/) for more information.

```yaml
  tsdproxy.name: "my-service"
  tsdproxy.autodetect: "false"
  tsdproxy.proxyprovider: "providername"
  tsdproxy.ephemeral: "false"
  tsdproxy.funnel: "false"
```

#### Connecting a service to the proxy via a Proxy list

An alternative way to add a service to the proxy is to use Proxy files.

Please read the [official TSDProxy documentation](https://almeidapaulopt.github.io/tsdproxy/docs/files/) for more information.

You will need to use the `tsdproxy_config_files` variable and add your proxy list file to the directory for configuration files, most likely `/mash/tsdproxy/config/`. It is possible to so so manually or by using [AUX-Files](auxiliary.md).

## Related services

- [Headscale](headscale.md) — Open source, self-hosted implementation of the [Tailscale](https://tailscale.com/) control server
