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
SPDX-FileCopyrightText: 2024 Tiz
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Fider

The playbook can install and configure [Fider](https://github.com/getfider/fider) for you.

Fider is a feedback portal for feature requests and suggestions.

See the project's [documentation](https://docs.fider.io/) to learn what Fider does and why it might be useful to you.

For details about configuring the [Ansible role for Fider](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az3Fe49p3uVZpC43KdB5gDCTmr8u7Y), you can check them via:

- 🌐 [the role's documentation](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az3Fe49p3uVZpC43KdB5gDCTmr8u7Y/tree/docs/configuring-fider.md) online
- 📁 `roles/galaxy/fider/docs/configuring-fider.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Postgres](postgres.md) database
- [Traefik](traefik.md) reverse-proxy server
- [exim-relay](exim-relay.md) mailer — required on the default configuration; alternatively it is possible to use one of the SMTP servers which catch outgoing messages like [Mailpit](mailpit.md)

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# fider                                                                #
#                                                                      #
########################################################################

fider_enabled: true

fider_hostname: fider.example.com

########################################################################
#                                                                      #
# /fider                                                               #
#                                                                      #
########################################################################
```

**Note**: hosting Fider under a subpath (by configuring the `fider_path_prefix` variable) does not seem to be possible due to Fider's technical limitations.

### Configuring the mailer (optional)

On Fider you can set up a mailer for functions such as password recovery. If you enable the [exim-relay](exim-relay.md) service in your inventory configuration, the playbook will automatically configure it as a mailer for the service.

To actually have the service use (and get messages sent through the exim-relay service), you will need to adjust settings on the service's UI after the service is installed.

>[!WARNING]
> Without setting an authentication method such as DKIM, SPF, and DMARC for your hostname, emails are most likely to be quarantined as spam at recipient's mail servers. The worst scenario is that your server's IP address or hostname will be included in the spam list such as the one managed by [Spamhaus](https://www.spamhaus.org/), depending on the reputation. As the exim-relay service supports DKIM signing, refer to [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay/blob/main/docs/configuring-exim-relay.md#enable-dkim-support-optional) for details about how to set it up.

### Integrating with Prometheus (optional)

Fider can natively expose metrics to [Prometheus](prometheus.md).

#### Expose metrics internally

If Fider and Prometheus do not share a network (like Traefik), you can connect the Fider container network to Prometheus by adding the following configuration to your `vars.yml` file:

```yaml
prometheus_container_additional_networks_custom:
  - "{{ fider_container_network }}"
```

#### Expose metrics publicly

If Fider metrics are not scraped from a local Prometheus instance, you can expose the metrics publicly so that a remote instance can fetch them.

When exposing metrics publicly, you should consider to set up [HTTP Basic Authentication](https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication) **or anyone would be able to read your metrics**.

To expose the metrics publicly, add the following configuration to your `vars.yml` file (adapt to your needs):

```yaml
mash_playbook_metrics_exposure_enabled: true
mash_playbook_metrics_exposure_hostname: mash.example.com
```

It will expose the metrics at `https://mash.example.com/metrics/mash-fider`.

To enable the HTTP Basic authentication, add the following configuration to your `vars.yml` file (adapt to your needs):

```yaml
fider_container_labels_traefik_metrics_middleware_basic_auth_enabled: true

# See https://doc.traefik.io/traefik/middlewares/http/basicauth/#users for details.
fider_container_labels_traefik_metrics_middleware_basic_auth_users: ""
```

## Usage

After installation, the Fider instance becomes available at the URL specified with `fider_hostname`. With the configuration above, the service is hosted at `https://fider.example.com`.

To get started, open the URL with a web browser, and follow the set up wizard.

## Troubleshooting

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az3Fe49p3uVZpC43KdB5gDCTmr8u7Y/tree/docs/configuring-fider.md#troubleshooting) on the role's documentation for details.
