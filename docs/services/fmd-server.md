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
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# FMD Server

The playbook can install and configure [FMD Server](https://gitlab.com/fmd-foss/fmd-server) (aka. FindMyDeviceServer) for you.

FMD Server is the official server for [FMD (FindMyDevice)](https://gitlab.com/fmd-foss/fmd-android), which allows you to locate, ring, wipe and issue other commands to your Android device when it is lost.

See the project's [documentation](https://gitlab.com/fmd-foss/fmd-server/-/blob/master/README.md) to learn what FMD Server does and why it might be useful to you.

For details about configuring the [Ansible role for FMD Server](https://github.com/mother-of-all-self-hosting/ansible-role-fmd-server), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-fmd-server/blob/main/docs/configuring-fmd-server.md) online
- 📁 `roles/galaxy/fmd_server/docs/configuring-fmd-server.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# fmd_server                                                           #
#                                                                      #
########################################################################

fmd_server_enabled: true

fmd_server_hostname: fmd.example.com

########################################################################
#                                                                      #
# /fmd_server                                                          #
#                                                                      #
########################################################################
```

**Note**: hosting FMD Server under a subpath (by configuring the `fmd_server_path_prefix` variable) does not seem to be possible due to FMD Server's technical limitations.

### Set a registration token

The instance is configured to require a token for registration to be specified. Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-fmd-server/blob/main/docs/configuring-fmd-server.md#set-a-registration-token) on the role's documentation for details.

### Integrating with Prometheus (optional)

FMD Server can natively expose metrics to [Prometheus](prometheus.md).

#### Expose metrics internally

If FMD Server and Prometheus do not share a network (like Traefik), you can connect the FMD Server container network to Prometheus by adding the following configuration to your `vars.yml` file:

```yaml
prometheus_container_additional_networks_custom:
  - "{{ fmd_server_container_network }}"
```

#### Expose metrics publicly

If FMD Server metrics are not scraped from a local Prometheus instance, you can expose the metrics publicly so that a remote instance can fetch them.

When exposing metrics publicly, you should consider to set up [HTTP Basic Authentication](https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication) **or anyone would be able to read your metrics**.

To expose the metrics publicly, add the following configuration to your `vars.yml` file (adapt to your needs):

```yaml
mash_playbook_metrics_exposure_enabled: true
mash_playbook_metrics_exposure_hostname: mash.example.com
```

It will expose the metrics at `https://mash.example.com/metrics/mash-findmydeviceserver`.

To enable the HTTP Basic authentication, add the following configuration to your `vars.yml` file (adapt to your needs):

```yaml
fmd_server_container_labels_traefik_metrics_middleware_basic_auth_enabled: true

# See https://doc.traefik.io/traefik/middlewares/http/basicauth/#users for details.
fmd_server_container_labels_traefik_metrics_middleware_basic_auth_users: ""
```

## Usage

After running the command for installation, the FMD Server instance becomes available at the URL specified with `fmd_hostname`. With the configuration above, the service is hosted at `https://fmd.example.com`.

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-fmd-server/blob/main/docs/configuring-fmd-server.md#usage) on the role's documentation for details about how to set up the client (FMD).

>[!NOTE]
> As sending commands from FMD Server to your device requires a UnifiedPush Distributor application, you might be interested in self-hosting a [ntfy](ntfy.md) Push Server along with it.

## Troubleshooting

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-fmd-server/blob/main/docs/configuring-fmd-server.md#troubleshooting) on the role's documentation for details.
