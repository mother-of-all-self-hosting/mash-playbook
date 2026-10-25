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
SPDX-FileCopyrightText: 2026 Bergruebe

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Beszel hub

The playbook can install and configure the [Beszel](https://beszel.dev/) hub for you.

Beszel is a lightweight server monitoring platform that includes Docker statistics, historical data, and alert functions. It consists of the **hub**, a web application which this playbook installs, and **agents**, which run on the systems you want to monitor and send their metrics to the hub.

See the project's [documentation](https://beszel.dev/guide/what-is-beszel) to learn what Beszel does and why it might be useful to you.

For details about configuring the [Ansible role for the Beszel hub](https://github.com/mother-of-all-self-hosting/ansible-role-beszel-hub), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-beszel-hub/blob/main/docs/configuring-beszel-hub.md) online
- 📁 `roles/galaxy/beszel_hub/docs/configuring-beszel-hub.md` locally, if you have [fetched the Ansible roles](../../docs/installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](../traefik/README.md) reverse-proxy server
- (optional) [Pocket ID](../pocket_id/README.md) — for single sign-on via OIDC
- (optional) [TSDProxy](../tsdproxy/README.md) — for reaching the hub over Tailscale

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../../docs/installing.md) process:

```yaml
########################################################################
#                                                                      #
# beszel_hub                                                           #
#                                                                      #
########################################################################

beszel_hub_enabled: true

beszel_hub_hostname: mash.example.com
beszel_hub_path_prefix: /beszel-hub

########################################################################
#                                                                      #
# /beszel_hub                                                          #
#                                                                      #
########################################################################
```

### Single sign-on with Pocket ID (optional)

The Beszel hub supports logging in with [Pocket ID](../pocket_id/README.md) or another OIDC provider. If Pocket ID runs on the same server, the hub can also reach it over its container network. Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-beszel-hub/blob/main/docs/configuring-beszel-hub.md#single-sign-on-with-oidc-eg-pocket-id-optional) on the role's documentation for details.

### Exposing the hub via TSDProxy (optional)

If [TSDProxy](../tsdproxy/README.md) is enabled, it can expose the hub in your Tailscale network, so that agents in the tailnet can connect to the hub without opening any port. To do so, add the following configuration to your `vars.yml` file:

```yaml
beszel_hub_container_labels_tsdproxy_enabled: true
```

The playbook then connects the hub to TSDProxy's container network automatically. Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-beszel-hub/blob/main/docs/configuring-beszel-hub.md#using-the-beszel-hub-with-tailscale-tsdproxy-optional) on the role's documentation for details, including how to make the web interface reachable over the tailnet only.

## Usage

After running the command for installation, the Beszel hub becomes available at the URL specified with `beszel_hub_hostname` (and `beszel_hub_path_prefix`). With the configuration above, the service is hosted at `https://mash.example.com/beszel-hub`.

To get started, open the URL with a web browser and create the first user account. Then add the systems to be monitored by clicking "Add System", and install an agent on each of them. Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-beszel-hub/blob/main/docs/configuring-beszel-hub.md#usage) on the role's documentation for details, and [this section](https://github.com/mother-of-all-self-hosting/ansible-role-beszel-hub/blob/main/docs/configuring-beszel-hub.md#connect-a-local-agent-via-unix-socket-optional) for connecting an agent on the same server via a Unix socket.

## Troubleshooting

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-beszel-hub/blob/main/docs/configuring-beszel-hub.md#troubleshooting) on the role's documentation for details.

## Related services

- [Uptime Kuma](../uptime_kuma/README.md) — Fancy self-hosted monitoring tool
- [Healthchecks](../healthchecks/README.md) — Cron job monitoring service
- [Grafana](../grafana/README.md) — Open observability platform
- [Pocket ID](../pocket_id/README.md) — Simple OIDC provider with passkey support
- [TSDProxy](../tsdproxy/README.md) — Proxy for exposing services in a Tailscale network
