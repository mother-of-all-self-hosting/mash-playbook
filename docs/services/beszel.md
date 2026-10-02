<!--
SPDX-FileCopyrightText: 2026 Bergruebe

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Beszel

The playbook can install and configure the [Beszel](https://beszel.dev/) hub for you.

Beszel is a lightweight server monitoring platform that includes Docker statistics, historical data, and alert functions. It consists of the **hub**, a web application which this playbook installs, and **agents**, which run on the systems you want to monitor and send their metrics to the hub.

See the project's [documentation](https://beszel.dev/guide/what-is-beszel) to learn what Beszel does and why it might be useful to you.

For details about configuring the [Ansible role for Beszel](https://github.com/Bergruebe/ansible-role-beszel), you can check them via:

- 🌐 [the role's documentation](https://github.com/Bergruebe/ansible-role-beszel/blob/main/docs/configuring-beszel.md) online
- 📁 `roles/galaxy/beszel/docs/configuring-beszel.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server
- (optional) [Pocket ID](pocket-id.md) — for single sign-on via OIDC
- (optional) [TSDProxy](tsdproxy.md) — for reaching the hub over Tailscale

Beszel needs no database server — the hub keeps its data in an embedded SQLite database.

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# beszel                                                               #
#                                                                      #
########################################################################

beszel_enabled: true

beszel_hostname: beszel.example.com

########################################################################
#                                                                      #
# /beszel                                                              #
#                                                                      #
########################################################################
```

**Note**: hosting Beszel under a subpath is possible by configuring the `beszel_path_prefix` variable (e.g. `/beszel`).

## Installation

After adjusting the configuration, run the playbook with [installing](../installing.md) to install the service:

```sh
just install-service beszel
```

## Usage

After running the command for installation, the Beszel hub becomes available at the URL specified with `beszel_hostname` (and `beszel_path_prefix`). With the configuration above, the service is hosted at `https://beszel.example.com`.

To get started, open the URL with a web browser and create the first user account. Then add the systems to be monitored by clicking "Add System", and install an agent on each of them with the public key and token shown in the dialog. See [this page](https://beszel.dev/guide/agent-installation) on the official documentation for details about installing agents.

Agents configured with the hub's URL and a token connect to the hub via WebSocket through Traefik, so no additional port needs to be opened on the server.

### Single sign-on with Pocket ID

If [Pocket ID](pocket-id.md) is enabled, the playbook connects the hub to Pocket ID's container network automatically (controlled by `beszel_pocket_id_integration_enabled`). This lets the hub request the OIDC token and user info from Pocket ID internally, while your browser uses Pocket ID's public URL.

To control the login behavior, add the following configuration to your `vars.yml` file as needed:

```yaml
# Create a Beszel user automatically on the first login via Pocket ID
beszel_environment_variable_user_creation: true

# Open Pocket ID's login page in the same window instead of a popup
beszel_environment_variable_oauth_disable_popup: true

# Allow logging in with Pocket ID only (enable it after confirming that the login works)
# beszel_environment_variable_disable_password_auth: true
```

The OIDC client still needs to be created on Pocket ID and added as a provider on Beszel's PocketBase admin interface. With the default MASH settings, use `https://pocketid.example.com/authorize` as the auth URL, and `http://mash-pocket-id:1411/api/oidc/token` and `http://mash-pocket-id:1411/api/oidc/userinfo` as the token and user info URLs. See [this section](https://github.com/Bergruebe/ansible-role-beszel/blob/main/docs/configuring-beszel.md#single-sign-on-with-oidc-eg-pocket-id-optional) on the role's documentation for the step-by-step instructions.

### Reaching the hub over Tailscale (TSDProxy)

If [TSDProxy](tsdproxy.md) is enabled, you can have it expose the hub in your tailnet by adding the following configuration to your `vars.yml` file:

```yaml
beszel_container_labels_tsdproxy_enabled: true
```

The playbook then connects the hub to TSDProxy's container network automatically, and the hub becomes available at `https://mash-beszel.<tailnet>.ts.net`. Agents which are members of the tailnet can connect to the hub at this URL (`HUB_URL`) without opening any port.

To make the web interface reachable over the tailnet only, disable the Traefik labels and use the tailnet hostname as `beszel_hostname`:

```yaml
beszel_container_labels_traefik_enabled: false

beszel_container_labels_tsdproxy_enabled: true

beszel_hostname: mash-beszel.tail1234.ts.net
```

See [this section](https://github.com/Bergruebe/ansible-role-beszel/blob/main/docs/configuring-beszel.md#using-beszel-with-tailscale-tsdproxy-optional) on the role's documentation for details, including how to set up agents.

>[!NOTE]
> Exposing the hub via TSDProxy cannot be combined with hosting Beszel under a subpath (`beszel_path_prefix`).

### Monitoring the MASH server itself

To monitor the server on which the hub runs, you can install an agent on it and have the hub connect to it via a Unix socket. See [this section](https://github.com/Bergruebe/ansible-role-beszel/blob/main/docs/configuring-beszel.md#connect-a-local-agent-via-unix-socket-optional) on the role's documentation for details.

### A note on container hardening

The hub container runs as the `mash` user with all capabilities dropped and a read-only root filesystem. Only its data directory, the optional agent socket directory, and a `tmpfs` mount at `/tmp` are writable.

## Troubleshooting

See [this section](https://github.com/Bergruebe/ansible-role-beszel/blob/main/docs/configuring-beszel.md#troubleshooting) on the role's documentation for details.

## Related services

- [Uptime Kuma](uptime-kuma.md) — Fancy self-hosted monitoring tool
- [Healthchecks](healthchecks.md) — Cron job monitoring service
- [Grafana](grafana.md) — Open observability platform
- [Pocket ID](pocket-id.md) — Simple OIDC provider with passkey support
- [TSDProxy](tsdproxy.md) — Proxy for exposing services in a Tailscale network
