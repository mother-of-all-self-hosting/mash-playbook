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

Grafana is a web-based tool for visualizing your [Prometheus](../prometheus/README.md) metrics (time-series).

See the project's [documentation](https://grafana.com/docs/) to learn what Grafana does and why it might be useful to you.

For details about configuring the [Ansible role for Grafana](https://github.com/mother-of-all-self-hosting/ansible-role-grafana), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-grafana/blob/main/docs/configuring-grafana.md) online
- 📁 `roles/galaxy/grafana/docs/configuring-grafana.md` locally, if you have [fetched the Ansible roles](../../docs/installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](../traefik/README.md) reverse-proxy server
- (optional) [exim-relay](../exim_relay/README.md) mailer
- (optional) [ntfy](../ntfy/README.md)

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../../docs/installing.md) process:

```yaml
########################################################################
#                                                                      #
# grafana                                                              #
#                                                                      #
########################################################################

grafana_enabled: true

grafana_hostname: mash.example.com
grafana_path_prefix: /grafana

########################################################################
#                                                                      #
# /grafana                                                             #
#                                                                      #
########################################################################
```

### Setting administrator's account details (optional)

While Grafana creates a user with `admin` as the username and password by default, it is possible to specify your own values.

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-grafana/blob/main/docs/configuring-grafana.md#setting-administrators-account-details-optional) on the role's documentation for details.

### File provisioning

The fully configured Grafana instance is a system of multiple components, such as dashboards, data sources, notification points, other resources, and so on. All of these things can be configured via the UI, but many of them can also be configured directly via "File provisioning".

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-grafana/blob/main/docs/configuring-grafana.md#file-provisioning) on the role's documentation for details.

### Integrating with Prometheus Node Exporter

If you've installed [Prometheus Node Exporter](../prometheus_node_exporter/README.md) on any host (target) scraped by Prometheus, you may wish to install a dashboard for Prometheus Node Exporter.

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-grafana/blob/main/docs/configuring-grafana.md#integrating-with-prometheus-node-exporter) on the role's documentation for details.

### Single-Sign-On

Grafana supports Single-Sign-On (SSO) via OAuth. To make use of this you'll need an Identity Provider (IdP) like [authentik](../authentik/README.md), [Authelia](../authelia/README.md), [Keycloak](../keycloak/README.md) or [Pocket ID](../pocket_id/README.md).

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-grafana/blob/main/docs/configuring-grafana.md#configuring-single-sign-on) on the role's documentation for details.

### Configuring the mailer (optional)

On Grafana you can set up a mailer for functions such as password recovery. If you enable the [exim-relay](../exim_relay/README.md) service in your inventory configuration, the playbook will automatically configure it as a mailer for the service.

To actually have the service use (and get messages sent through the exim-relay service), you will need to adjust settings on the service's UI after the service is installed.

>[!WARNING]
> Without setting an authentication method such as DKIM, SPF, and DMARC for your hostname, emails are most likely to be quarantined as spam at recipient's mail servers. The worst scenario is that your server's IP address or hostname will be included in the spam list such as the one managed by [Spamhaus](https://www.spamhaus.org/), depending on the reputation. As the exim-relay service supports DKIM signing, refer to [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay/blob/main/docs/configuring-exim-relay.md#enable-dkim-support-optional) for details about how to set it up.

## Usage

After running the command for installation, the Grafana instance becomes available at the URL specified with `grafana_hostname` and `grafana_path_prefix`. With the configuration above, the service is hosted at `https://mash.example.com/grafana`.

To get started, open the URL with a web browser, and follow the set up wizard.

## Related services

- [Grafana Loki](../loki/README.md) — Log aggregation system that helps collect, store, and analyze logs in a scalable and efficient manner
- [Prometheus](../prometheus/README.md) — Metrics collection and alerting monitoring solution
