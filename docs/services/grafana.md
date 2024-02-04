# Grafana

[Grafana](https://grafana.com/) is an open and composable observability and data visualization platform, often used with [Prometheus](prometheus.md).


## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# grafana                                                              #
#                                                                      #
########################################################################

grafana_enabled: true

grafana_hostname: mash.example.com
grafana_path_prefix: /grafana

grafana_default_admin_user: admin
# Generating a strong password (e.g. `pwgen -s 64 1`) is recommended
grafana_default_admin_password: ''

########################################################################
#                                                                      #
# /grafana                                                             #
#                                                                      #
########################################################################
```

In the example configuration above, we configure the service to be hosted at `https://mash.example.com/grafana`.

You can remove the `grafana_path_prefix` variable definition, to make it default to `/`, so that the service is served at `https://mash.example.com/`.

### Configuring data sources

Grafana is merely a visualization tool. It needs to pull data from a metrics (time-series) database, like [Prometheus](prometheus.md).

You can add multiple data sources to Grafana.

Below, we show a few examples of connecting Grafana to local datasources (running in containers on the same machine).
**If you're enabling multiple, you need to "merge" the configurations**. That is, don't define `grafana_provisioning_datasources` or `grafana_container_additional_networks_custom` twice, but combine them.

#### Integrating with a local Prometheus instance

If you're installing [Prometheus](prometheus.md) on the same server, you can hook Grafana to it over the container network with the following **additional** configuration:

```yaml
grafana_provisioning_datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: "http://{{ prometheus_identifier }}:9090"
	# Enable below if connecting to a remote instance that uses Basic Auth.
	# basicAuth: true
    # basicAuthUser: loki
    # secureJsonData:
    #   basicAuthPassword: ""

# Prometheus runs in another container network, so we need to connect to it.
grafana_container_additional_networks_custom:
  - "{{ prometheus_container_network }}"
```

For connecting to a **remote** Prometheus instance, you may need to adjust this configuration.

#### Integrating with a local Loki instance

If you're installing [Grafana Loki](grafana-loki.md) on the same server, you can hook Grafana to it over the container network with the following **additional** configuration:

```yaml
grafana_provisioning_datasources:
  - name: Loki (your-tenant-id)
    type: loki
    access: proxy
    url: "http://{{ loki_identifier }}:{{ loki_server_http_listen_port }}"
	# Enable below and also (basicAuthPassword) if connecting to a remote instance that uses Basic Auth.
	# basicAuth: true
    # basicAuthUser: loki
    jsonData:
      httpHeaderName1: X-Scope-OrgID
    secureJsonData:
      httpHeaderValue1: "your-tenant-id"
      # basicAuthPassword: ""

# Loki runs in another container network, so we need to connect to it.
grafana_container_additional_networks_custom:
  - "{{ loki_container_network }}"
```

For connecting to a **remote** Loki instance, you may need to adjust this configuration.

If you're installing [Promtail](./promtail.md) on the same server as Loki, by default it's configured to send `mash` as the tenant ID.

### Integrating with Prometheus Node Exporter

If you've installed [Prometheus Node Exporter](prometheus-node-exporter.md) on any host (target) scraped by Prometheus, you may wish to install a dashboard for Prometheus Node Exporter.

The Prometheus Node Exporter role exposes a list of URLs containing dashboards (JSON files) in its `prometheus_node_exporter_dashboard_urls` variable.

You can add this **additional** configuration to make the Grafana service pull these dashboards:

```yaml
grafana_dashboard_download_urls: |
  {{
    prometheus_node_exporter_dashboard_urls
  }}
```

### Single-Sign-On

Grafana supports Single-Sign-On (SSO) via OAUTH. To make use of this you'll need a Identity Provider like [authentik](./authentik.md), [Keycloak](./keycloak.md) or [Authelia](./authelia.md).

Below, you can find some examples for Grafana configuration.


#### Single-Sign-On / Authentik

* Create a new OAUTH provider in authentik called `grafana`
* Create an application also named `grafana` in authentik using this provider
* Add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process (make sure to adjust `authentik.example.com`)

```yaml
# To make Grafana honor the expiration time of JWT tokens, enable this experimental feature below.
# grafana_feature_toggles_enable: accessTokenExpirationCheck

grafana_environment_variables_additional_variables: |
  GF_AUTH_GENERIC_OAUTH_ENABLED=true
  GF_AUTH_GENERIC_OAUTH_NAME=authentik
  GF_AUTH_GENERIC_OAUTH_CLIENT_ID=COPIED-CLIENTID
  GF_AUTH_GENERIC_OAUTH_CLIENT_SECRET=COPIED-CLIENTSECRET
  GF_AUTH_GENERIC_OAUTH_SCOPES=openid profile email
  GF_AUTH_GENERIC_OAUTH_AUTH_URL=https://authentik.example.com/application/o/authorize/
  GF_AUTH_GENERIC_OAUTH_TOKEN_URL=https://authentik.example.com/application/o/token/
  GF_AUTH_GENERIC_OAUTH_API_URL=https://authentik.example.com/application/o/userinfo/
  GF_AUTH_SIGNOUT_REDIRECT_URL=https://authentik.example.com/application/o/grafana/end-session/
  # Optionally enable auto-login (bypasses Grafana login screen)
  #GF_AUTH_OAUTH_AUTO_LOGIN="true"
  GF_AUTH_GENERIC_OAUTH_ALLOW_ASSIGN_GRAFANA_ADMIN=true
  # Optionally map user groups to Grafana roles
  GF_AUTH_GENERIC_OAUTH_ROLE_ATTRIBUTE_PATH=contains(groups[*], 'Grafana Admins') && 'Admin' || contains(groups[*], 'Grafana Editors') && 'Editor' || 'Viewer'
```

Make sure the user you want to login as has an email address in authentik, otherwise there will be an error.


#### Single-Sign-On / Authelia

The configuration flow below assumes [Authelia](authelia.md) configured via the playbook, but you can run Authelia in another way too.

- Come up with a client ID you'd like to use. Example: `grafana`
- Generate a shared secret for the OpenID Connect application: `pwgen -s 64 1`. This is to be used in `GF_AUTH_GENERIC_OAUTH_CLIENT_SECRET` below
- Hash the shared secret for use in Authelia's configuration (`authelia_config_identity_providers_oidc_clients`): `php -r 'echo password_hash("PASSWORD_HERE",  PASSWORD_ARGON2ID);'`. Feel free to use another language (or tool) for creating a hash as well. A few different hash algorithms are supported besides Argon2id.
- Define this `grafana` client in Authelia via `authelia_config_identity_providers_oidc_clients`. See [example configuration](authelia.md#protecting-a-service-with-openid-connect) on the Authelia documentation page.

```yaml
# To make Grafana honor the expiration time of JWT tokens, enable this experimental feature below.
# grafana_feature_toggles_enable: accessTokenExpirationCheck

grafana_environment_variables_additional_variables: |
  GF_AUTH_GENERIC_OAUTH_ENABLED=true
  GF_AUTH_GENERIC_OAUTH_NAME=Authelia
  GF_AUTH_GENERIC_OAUTH_CLIENT_ID=grafana
  GF_AUTH_GENERIC_OAUTH_CLIENT_SECRET=PLAIN_TEXT_SHARED_SECRET
  GF_AUTH_GENERIC_OAUTH_SCOPES=openid profile email groups
  GF_AUTH_GENERIC_OAUTH_EMPTY_SCOPES=false
  GF_AUTH_GENERIC_OAUTH_AUTH_URL=https://authelia.example.com/api/oidc/authorization
  GF_AUTH_GENERIC_OAUTH_TOKEN_URL=https://authelia.example.com/api/oidc/token
  GF_AUTH_GENERIC_OAUTH_API_URL=https://authelia.example.com/api/oidc/userinfo
  GF_AUTH_GENERIC_OAUTH_LOGIN_ATTRIBUTE_PATH=preferred_username
  GF_AUTH_GENERIC_OAUTH_GROUPS_ATTRIBUTE_PATH=groups
  GF_AUTH_GENERIC_OAUTH_NAME_ATTRIBUTE_PATH=name
  GF_AUTH_GENERIC_OAUTH_USE_PKCE=true
```

## Usage

After installation, you should be able to access your new Grafana instance at the configured URL (see above).

Going there, you'll be taken to the initial setup wizard, which will let you assign some paswords and other configuration.


## Recommended other services

Grafana is just a visualization tool which requires pulling data from a metrics (time-series) database like.

You may be interested in combining it with [Prometheus](prometheus.md).
