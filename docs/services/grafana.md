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
SPDX-FileCopyrightText: 2023 Borislav Pantaleev
SPDX-FileCopyrightText: 2023 Felix Stupp
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 Igor Goldenberg
SPDX-FileCopyrightText: 2024 Thomas Miceli
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara
SPDX-FileCopyrightText: 2025 MASH project contributors

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Grafana

The playbook can install and configure [Grafana](https://grafana.com/) for you.

Grafana is an open and composable observability and data visualization platform. It is often used with [Prometheus](prometheus.md).

See the project's [documentation](https://grafana.com/docs/) to learn what Grafana does and why it might be useful to you.

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server
- (optional) [exim-relay](exim-relay.md) mailer
- (optional) [ntfy](ntfy.md)

Note that Grafana is just a visualization tool and requires pulling data from a metrics (time-series) database.

## Adjusting the playbook configuration

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

### File provisioning

The fully configured Grafana instance is a system of multiple components, such as dashboards, data sources, notification points, other resources, and so on. All of these things can be configured via the UI, but many of them can also be configured directly via "File provisioning".

To see all components with file provisioning support see the roles [defaults/main.yml](https://github.com/mother-of-all-self-hosting/ansible-role-grafana/blob/main/defaults/main.yml) file and search for `grafana_provisioning_`

>[!NOTE]
> If you're enabling multiple of one component, you need to "merge" the configurations. Do not define `grafana_provisioning_datasources_datasources` twice, but combine them.

#### Datasources

For Grafana to create graphs, charts, and alerts it needs to pull data from a metrics (time-series) database like [Prometheus](prometheus.md). This can be set up with the `grafana_provisioning_datasources_datasources` variable.

By default Grafana will automatically delete previously provisioned data sources when they’re removed from `grafana_provisioning_datasources_datasources` via the `grafana_provisioning_datasources_prune` variable. If you want to manually delete provisioned datasources instead, add the following configuration:

```yaml
grafana_provisioning_datasources_prune: false
grafana_provisioning_datasources_deleteDatasources:
  - name: Prometheus
    orgId: 1

  - name: Loki
    orgId: 1
```

#### Integrating with a local Prometheus instance

If [Prometheus](prometheus.md) runs on the same server, you can hook Grafana to it over the container network with the following additional configuration:

```yaml
grafana_provisioning_datasources_datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: "http://{{ prometheus_identifier }}:9090"
    jsonData:
      timeInterval: "{{ prometheus_config_global_scrape_interval }}"
    # Enable below if connecting to a remote instance that uses Basic Auth.
    # basicAuth: true
    # basicAuthUser: loki
    # secureJsonData:
    #   basicAuthPassword: ""
```

For connecting to a remote Prometheus instance, you may need to adjust this configuration.

#### Integrating with a local Loki instance

If [Grafana Loki](grafana-loki.md) runs on the same server, you can hook Grafana to it over the container network with the following additional configuration:

```yaml
grafana_provisioning_datasources_datasources:
  - name: Loki (your-tenant-id)
    type: loki
    access: proxy
    url: "{{ loki_scheme }}://{{ loki_identifier }}:{{ loki_server_http_listen_port }}"
    # Enable below and also (basicAuthPassword) if connecting to a remote instance that uses Basic Auth.
    # basicAuth: true
    # basicAuthUser: loki
    jsonData:
      httpHeaderName1: X-Scope-OrgID
    secureJsonData:
      httpHeaderValue1: "your-tenant-id"
      # basicAuthPassword: ""
```

For connecting to a remote Loki instance, you may need to adjust this configuration.

If [Promtail](promtail.md) runs on the same server as Loki, by default it is configured to send `mash` as the tenant ID.

#### Alerts

With alerts you can receive notifications when specific conditions regarding your data are met. Since there is no "prune" option (like datasources) you need to add alerts to `grafana_provisioning_alerts_deleteRules` when you want it removed.

The example below is truncated. Refer to the [official example](https://github.com/grafana/provisioning-alerting-examples/blob/main/config-files/grafana/provisioning/alerting/alert_rules.yaml) for a full example. As you can see in the official example, these YAML alerts are not very human readable. It is recommended you create your alert in the UI and then select the "Export rules" option to create the proper values.

```yaml
grafana_provisioning_alerts_groups:
  - orgId: 1
    name: my_rule_group
    folder: my_first_folder
    interval: 60s
    rules:
      - uid: my_id_1

grafana_provisioning_alerts_deleteRules:
  - orgId: 1
    uid: my_id_1
```

#### Contact points

To specify the place where a firing alert should be routed to (Slack, Discord, Webhook URL, etc.) you need to configure a contact point. The prune support does not exist for contact points either, so you need to add the alert to `grafana_provisioning_contact_points_contactPoints` when you want it removed.

```yaml
grafana_provisioning_contact_points_contactPoints:
  - orgId: 1
    name: Matrix
    receivers:
      - uid: first_uid
        type: webhook
        disableResolveMessage: false
        settings:
          url: "https://matrix.example.com/_matrix/maubot/plugin/bot.maubot.alertbot/webhook/!roomid"

grafana_provisioning_contact_points_deleteContactPoints:
  - orgId: 1
    uid: first_uid
```

### Configuring the mailer (optional)

On Grafana you can set up a mailer for functions such as password recovery. If you enable the [exim-relay](exim-relay.md) service in your inventory configuration, the playbook will automatically configure it as a mailer for the service.

To actually have the service use (and get messages sent through the exim-relay service), you will need to adjust settings on the service's UI after the service is installed.

>[!WARNING]
> Without setting an authentication method such as DKIM, SPF, and DMARC for your hostname, emails are most likely to be quarantined as spam at recipient's mail servers. The worst scenario is that your server's IP address or hostname will be included in the spam list such as the one managed by [Spamhaus](https://www.spamhaus.org/), depending on the reputation. As the exim-relay service supports DKIM signing, refer to [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay/blob/main/docs/configuring-exim-relay.md#enable-dkim-support-optional) for details about how to set it up.

### Integrating with Prometheus Node Exporter

If you've installed [Prometheus Node Exporter](prometheus-node-exporter.md) on any host (target) scraped by Prometheus, you may wish to install a dashboard for Prometheus Node Exporter.

The Prometheus Node Exporter role exposes a list of URLs containing dashboards (JSON files) in its `prometheus_node_exporter_dashboard_urls` variable.

You can add this additional configuration to make the Grafana service pull these dashboards:

```yaml
grafana_dashboard_download_urls: |
  {{
    prometheus_node_exporter_dashboard_urls
  }}
```

### Single-Sign-On

Grafana supports Single-Sign-On (SSO) via OAuth. To make use of this you'll need an Identity Provider (IdP) like [authentik](authentik.md), [Authelia](authelia.md), [Keycloak](keycloak.md) or [Pocket ID](pocket-id.md).

Below are examples for Grafana configuration.

#### Single-Sign-On / authentik

- Create a new OAuth provider in authentik called `grafana`
- Create an application also named `grafana` in authentik using this provider
- Add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process (make sure to adjust `authentik.example.com`)

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

#### Single-Sign-On / Pocket ID

Refer to [this page](https://pocket-id.org/docs/client-examples/grafana) on Pocket ID's documentation for the instruction.

## Usage

After running the command for installation, the Grafana instance becomes available at the URL specified with `grafana_hostname` and `grafana_path_prefix`. With the configuration above, the service is hosted at `https://mash.example.com/grafana`.

To get started, open the URL with a web browser, and follow the set up wizard.

## Related services

- [Grafana Loki](grafana-loki.md) — Log aggregation system that helps collect, store, and analyze logs in a scalable and efficient manner
- [Prometheus](prometheus.md) — Metrics collection and alerting monitoring solution
