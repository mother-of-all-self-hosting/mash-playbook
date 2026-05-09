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

# Apprise API

The playbook can install and configure [Apprise API](https://github.com/caronc/apprise-api) for you.

[Apprise](https://github.com/caronc/apprise/) allows you to send a notification to almost all of the most popular notification services available to us today such as Matrix, Telegram, Discord, Slack, Amazon SNS, ntfy, Gotify, etc.

See the project's [documentation](https://github.com/caronc/apprise-api/blob/master/README.md) to learn what Apprise API does and why it might be useful to you.

For details about configuring the [Ansible role for Apprise API](https://radicle.network/nodes/seed.radicle.garden/rad%3Az292aD8q3r8xqhJvLe2zv1b24gu7a), you can check them via:

- 🌐 [the role's documentation](https://radicle.network/nodes/seed.radicle.garden/rad%3Az292aD8q3r8xqhJvLe2zv1b24gu7a/tree/docs/configuring-apprise.md) online
- 📁 `roles/galaxy/apprise/docs/configuring-apprise.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- (optional) [Traefik](traefik.md) — a reverse-proxy server for exposing Configuration Manager publicly

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# apprise                                                              #
#                                                                      #
########################################################################

apprise_enabled: true

########################################################################
#                                                                      #
# /apprise                                                             #
#                                                                      #
########################################################################
```

### Expose the Configuration Manager publicly (optional)

By default, the Apprise's built-in Configuration Manager where one can access and create configurations on the web browser is not exposed to the internet.

To expose it publicly, add the following configuration to your `vars.yml` file (adapt to your needs):

```yaml
# The hostname at which the Configuration Manager is served.
apprise_hostname: "apprise.example.com"
```

**Note**: hosting the Configuration Manager under a subpath (by configuring the `apprise_path_prefix` variable) does not seem to be possible due to Apprise's technical limitations.

### Integrating with Prometheus (optional)

Apprise API can natively expose metrics to [Prometheus](prometheus.md).

#### Expose metrics internally

If Apprise API and Prometheus do not share a network (like Traefik), you can connect the Apprise API container network to Prometheus by adding the following configuration to your `vars.yml` file:

```yaml
prometheus_container_additional_networks_custom:
  - "{{ apprise_container_network }}"
```

#### Expose metrics publicly

If Apprise API metrics are not scraped from a local Prometheus instance, you can expose the metrics publicly so that a remote instance can fetch them.

When exposing metrics publicly, you should consider to set up [HTTP Basic Authentication](https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication) **or anyone would be able to read your metrics**.

To expose the metrics publicly, add the following configuration to your `vars.yml` file (adapt to your needs):

```yaml
mash_playbook_metrics_exposure_enabled: true
mash_playbook_metrics_exposure_hostname: mash.example.com
```

It will expose the metrics at `https://mash.example.com/metrics/mash-apprise`.

To enable the HTTP Basic authentication, add the following configuration to your `vars.yml` file (adapt to your needs):

```yaml
apprise_container_labels_traefik_metrics_middleware_basic_auth_enabled: true

# See https://doc.traefik.io/traefik/middlewares/http/basicauth/#users for details.
apprise_container_labels_traefik_metrics_middleware_basic_auth_users: ""
```

## Usage

After running the command for installation, Apprise API becomes available. If the Configuration Manager is configured to be exposed to the internet, it becomes available at the URL specified with `apprise_hostname`. With the configuration above, it is hosted at `https://apprise.example.com`.

You can check the list of notification services supported by Apprise at <https://github.com/caronc/apprise/wiki#notification-services>. The instruction to use the Apprise CLI is available at <https://github.com/caronc/apprise/wiki/CLI_Usage>.

## Troubleshooting

See [this section](https://radicle.network/nodes/seed.radicle.garden/rad%3Az292aD8q3r8xqhJvLe2zv1b24gu7a/tree/docs/configuring-apprise.md#troubleshooting) on the role's documentation for details.

## Related services

- [Gotify](gotify.md) — Simple server for sending and receiving messages
- [ntfy](ntfy.md) — Simple HTTP-based pub-sub notification service to send you push notifications from any computer
