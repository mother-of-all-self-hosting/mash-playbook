# APISIX Gateway

[APISIX Gateway](https://apisix.apache.org/docs/apisix/getting-started/README/) is an [API Gateway](https://apisix.apache.org/docs/apisix/terminology/api-gateway/) and Ingress Controller.

APISIX Gateway has a complex [architecture](https://apisix.apache.org/docs/apisix/architecture-design/apisix/) in which APISIX can serve multiple roles (data plane, control plane). There are different [deployment modes](https://apisix.apache.org/docs/apisix/deployment-modes/) for achieving a more decoupled setup.

What we're configuring here is a `traditional` deployment in which one APISIX instance acts as both the data plane and the control plane.
By tweaking the configuration, you may be able to install multiple instances (on separate machines), each serving a different role. This is beyond the scope of this documentation page.


## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server
- an [etcd](etcd.md) key-value store


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# apisix_gateway                                                       #
#                                                                      #
########################################################################

apisix_gateway_enabled: true

# Configure the hostname and path at which the API would be exposed
apisix_gateway_hostname: api.example.com
apisix_gateway_path_prefix: /api

apisix_gateway_config_deployment_admin_admin_key:
  - name: admin1
    key: secret-api-key-here
    role: admin
  - name: viewer1
    key: secret-api-key-here
    role: viewer

# You may also wish to enable the Admin API.
#
# If you'd be administrating APISIX via another service
# (e.g. APISIX Dashboard, which manipulates the etcd database directly),
# then enabling this Admin API is not strictly required.
apisix_gateway_container_labels_admin_enabled: true
apisix_gateway_container_labels_admin_hostname: admin.api.example.com
apisix_gateway_container_labels_admin_path_prefix: /

########################################################################
#                                                                      #
# /apisix_gateway                                                      #
#                                                                      #
########################################################################
```

If you'd like to do something more advanced, the [`ansible-role-apisix-gateway` Ansible role](https://github.com/mother-of-all-self-hosting/ansible-role-apisix-gateway) is very configurable and should not get in your way of exposing ports or configuring arbitrary settings.

Take a look at [its `default/main.yml` file](https://github.com/mother-of-all-self-hosting/ansible-role-apisix-gateway/blob/main/defaults/main.yml) for available Ansible variables you can use in your own `vars.yml` configuration file.

### URL

In the example configuration above, we configure APISIX to expose 2 services:

- Gateway API, to be reachable at `https://api.example.com/api`
- [Admin API](https://apisix.apache.org/docs/apisix/admin-api/), to be reachable at `https://api.example.com/api`

Path prefixes default to `/` for all services, so if you don't like the example above (using `/api`), consider removing the path prefix variables.

## Usage

After installation, you can send API requests to your API gateway (as specified in `apisix_gateway_hostname` and `apisix_gateway_path_prefix`).

Example: `curl https://api.example.com/api`

Since no routes are configured by default, you'd receive 404 requests. To configure routes, either use the Admin API (described below) or install [APISIX dashboard](./apisix-dashboard.md) to administrate APISIX using a web UI.

If you've enabled the [Admin API](https://apisix.apache.org/docs/apisix/admin-api/) (`apisix_gateway_container_labels_admin_enabled: true`), you will also be able to manage the APISIX configuration (managing routes, upstreams, etc.) by sending API requests to the Admin API URL (as specified in `apisix_gateway_container_labels_admin_hostname` and `apisix_gateway_container_labels_admin_path_prefix`).

Example: `curl -H 'X-API-KEY: YOUR_SECRET_API_KEY_HERE' https://admin.api.example.com/apisix/admin/routes`

## Recommended other services

- [APISIX dashboard](apisix-dashboard.md) — a dashboard (web UI) for APISIX
