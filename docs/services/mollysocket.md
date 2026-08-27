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

# MollySocket

The playbook can install and configure [MollySocket](https://github.com/mollyim/mollysocket) for you.

MollySocket is a service which allows [Molly](https://molly.im/) to receive [Signal](https://signal.org/) notifications via [UnifiedPush](https://unifiedpush.org/), the standard which makes it possible to send and receive push notifications without using Google's Firebase Cloud Messaging (FCM) service.

See the project's [documentation](https://github.com/mollyim/mollysocket/blob/main/README.md) to learn what MollySocket does and why it might be useful to you.

For details about configuring the [Ansible role for MollySocket](https://radicle.network/nodes/iris.radicle.network/rad%3Az2RnNwtTL5bKspfqmxQ2fX4JV4cXV), you can check them via:

- 🌐 [the role's documentation](https://radicle.network/nodes/iris.radicle.network/rad%3Az2RnNwtTL5bKspfqmxQ2fX4JV4cXV/tree/docs/configuring-mollysocket.md) online
- 📁 `roles/galaxy/mollysocket/docs/configuring-mollysocket.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- (optional) [Traefik](traefik.md) — Reverse-proxy server for exposing MollySocket web server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# mollysocket                                                          #
#                                                                      #
########################################################################

mollysocket_enabled: true

########################################################################
#                                                                      #
# /mollysocket                                                         #
#                                                                      #
########################################################################
```

### Configuring the web server

By default MollySocket's web server is configured to be exposed externally, and you need to set the hostname by adding the following configuration to your `vars.yml` file:

```yaml
# The hostname at which MollySocket's web server is served.
mollysocket_hostname: "mollysocket.example.com"
```

To disable it in favor of the "Air Gapped" mode, add the following configuration to your `vars.yml` file:

```yaml
mollysocket_environment_variables_molly_webserver: false
```

### Connecting to a ntfy instance (optional)

To use a MollySocket instance it is necessary to prepare a **Push Server**, such as the [ntfy](https://ntfy.sh/) server.

The ntfy server is available on the playbook. Enabling it automatically configures the mollysocket instance to connect to it.

See [this page](ntfy.md) for details about how to install it.

## Usage

After running the command for installation, the MollySocket instance becomes available, and its web server can be reached at the URL specified with `mollysocket_hostname`. With the configuration above, the web server is hosted at `https://mollysocket.example.com`.

To use a MollySocket instance it is necessary to prepare a **Distributor** running on Android and other devices (see [definitions on the official documentation of UnifiedPush](https://unifiedpush.org/developers/spec/definitions/) for the definition of the Distributor), such as [the ntfy application](https://docs.ntfy.sh/subscribe/phone/).

## Troubleshooting

See [this section](https://radicle.network/nodes/iris.radicle.network/rad%3Az2RnNwtTL5bKspfqmxQ2fX4JV4cXV/tree/docs/configuring-mollysocket.md#troubleshooting) on the role's documentation for details.

## Related services

- [ntfy](ntfy.md) — HTTP-based pub-sub notification service to send you push notifications from any computer
