<!--
SPDX-FileCopyrightText: 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# APISIX

The playbook can install and configure [APISIX](https://apisix.apache.org/docs/apisix/getting-started/README/) for you.

APISIX is an [API Gateway](https://apisix.apache.org/docs/apisix/terminology/api-gateway/) and Ingress Controller.

APISIX has a complex [architecture](https://apisix.apache.org/docs/apisix/architecture-design/apisix/) in which APISIX can serve multiple roles (data plane, control plane). There are different [deployment modes](https://apisix.apache.org/docs/apisix/deployment-modes/) for achieving a more decoupled setup.

What we're configuring here is a `traditional` deployment in which one APISIX instance acts as both the data plane and the control plane. By tweaking the configuration, you may be able to install multiple instances (on separate machines), each serving a different role. This is beyond the scope of this documentation page.

## Dependencies

This service requires the following other services:

- [etcd](etcd.md) key-value store
- [Traefik](traefik.md) reverse-proxy server

## Configuration

> [!NOTE]
> This service used to be called `apisix-gateway` and all of its variables were prefixed `apisix_gateway_`. Both lost the `_gateway`, because the service stopped being only a gateway when APISIX 3.13 started shipping the dashboard inside the image. If your `vars.yml` still uses the old names, the playbook fails with the full list of what to rename. The tags changed with them: `just install-service apisix`, not `just install-service apisix-gateway`.
>
> Only the names changed. The systemd service, the container, the container network and the data path on your server keep the names they have now, so nothing is reinstalled or moved.

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# apisix                                                               #
#                                                                      #
########################################################################

apisix_enabled: true

# Configure the hostname and path at which the API would be exposed
apisix_hostname: api.example.com
apisix_path_prefix: /api

apisix_config_deployment_admin_admin_key:
  - name: admin1
    key: secret-api-key-here
    role: admin
  - name: viewer1
    key: secret-api-key-here
    role: viewer

# You may also wish to expose the Admin API publicly.
#
# ⚠️ Read the "Reaching the bundled dashboard" section below before you do.
# This same listener also serves APISIX's built-in web UI, which has no
# authentication of its own, and you can reach both through an SSH tunnel
# instead of publishing them.
apisix_container_labels_admin_enabled: true
apisix_container_labels_admin_hostname: admin.api.example.com
apisix_container_labels_admin_path_prefix: /

########################################################################
#                                                                      #
# /apisix                                                              #
#                                                                      #
########################################################################
```

If you'd like to do something more advanced, the [`ansible-role-apisix` Ansible role](https://github.com/mother-of-all-self-hosting/ansible-role-apisix) is very configurable and should not get in your way of exposing ports or configuring arbitrary settings.

Take a look at [its `default/main.yml` file](https://github.com/mother-of-all-self-hosting/ansible-role-apisix/blob/main/defaults/main.yml) for available Ansible variables you can use in your own `vars.yml` configuration file.

### URL

In the example configuration above, we configure APISIX to expose 2 services:

- Gateway API, to be reachable at `https://api.example.com/api`
- [Admin API](https://apisix.apache.org/docs/apisix/admin-api/), to be reachable at `https://admin.api.example.com/`

Path prefixes default to `/` for all services, so if you don't like the example above (using `/api`), consider removing the path prefix variables.

## Usage

After running the command for installation, you can send API requests to your API gateway (as specified in `apisix_hostname` and `apisix_path_prefix`).

Example: `curl https://api.example.com/api`

Since no routes are configured by default, you'd receive 404 requests. To configure routes, either use the Admin API or the bundled web UI — both are described below.

If you've enabled the [Admin API](https://apisix.apache.org/docs/apisix/admin-api/) (`apisix_container_labels_admin_enabled: true`), you will also be able to manage the APISIX configuration (managing routes, upstreams, etc.) by sending API requests to the Admin API URL (as specified in `apisix_container_labels_admin_hostname` and `apisix_container_labels_admin_path_prefix`).

Example: `curl -H 'X-API-KEY: YOUR_SECRET_API_KEY_HERE' https://admin.api.example.com/apisix/admin/routes`

### Reaching the bundled dashboard

Since APISIX 3.13, the [APISIX Dashboard](apisix-dashboard.md) is no longer a separate project — it ships inside the `apache/apisix` image as a pure front-end, and APISIX serves it at `/ui/`. The playbook used to install the standalone dashboard as a service of its own; it [no longer does](apisix-dashboard.md), and no longer needs to.

There is nothing to install and nothing to enable, as long as you run APISIX 3.13 or newer (see [`VERSIONS.md`](../../VERSIONS.md) for the version the playbook currently installs, and [upgrade](../maintenance-upgrading-services.md) if you are behind). The only question is how you reach it, and it deserves a careful answer.

> [!WARNING]
> **The bundled UI is served from inside the Admin API's `server` block.** It shares that listener's port (`apisix_config_deployment_admin_admin_listen_port`, `9180` by default) and its `allow_admin` allowlist. **Making the UI reachable makes the Admin API reachable** — there is no way to publish one without the other.
>
> What protects each of them is different:
>
> - the Admin API rejects requests without a valid key from `apisix_config_deployment_admin_admin_key`
> - **the UI itself has no authentication at all.** It is static files. It asks you for an Admin API key and talks to the Admin API from your browser
>
> This is a real difference from the standalone APISIX Dashboard, which had a login page and its own user list.

Reaching it, from least to most exposed:

- **Through an SSH tunnel** — nothing is published to the network. Add `apisix_container_admin_http_bind_port: "127.0.0.1:9180"` to your `vars.yml`, re-run the [installation](../installing.md) process, then run `ssh -L 9180:127.0.0.1:9180 you@your-server` from your own machine and open <http://127.0.0.1:9180/ui/>.

- **Through Traefik, with authentication** — enable the Admin API as in the example configuration above and put a [basic-auth middleware](https://doc.traefik.io/traefik/reference/routing-configuration/http/middlewares/basicauth/) in front of it. The role has no dedicated variable for this (unlike the metrics route), so you declare the middleware yourself and then reference it by name:

  ```yaml
  apisix_container_labels_additional_labels_custom:
    # Generate the entry with `htpasswd -nb USERNAME PASSWORD`
    - "traefik.http.middlewares.mash-apisix-gateway-admin-auth.basicauth.users=someone:$apr1$..."

  apisix_container_labels_admin_middlewares:
    - mash-apisix-gateway-admin-auth
  ```

  The UI is then at `https://admin.api.example.com/ui/`. **Without such a middleware, you are publishing an admin console to the internet.**

If you expose the Admin API but would rather not publish the console alongside it, set `apisix_config_deployment_admin_enable_admin_ui: false`. `/ui/` then returns a 404 while the Admin API keeps working on the same port.

## Related services

- [etcd](etcd.md) — Distributed key-value store, where APISIX keeps its configuration
- [Traefik](traefik.md) — Reverse-proxy server which fronts APISIX's listeners
