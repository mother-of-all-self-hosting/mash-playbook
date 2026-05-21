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
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# bitmagnet

The playbook can install and configure [bitmagnet](https://bitmagnet.io/) for you.

bitmagnet is a self-hosted BitTorrent indexer, DHT crawler, content classifier and search engine with web UI, GraphQL API and Servarr stack integration.

See the project's [documentation](https://bitmagnet.io/) to learn what bitmagnet does and why it might be useful to you.

For details about configuring the [Ansible role for bitmagnet](https://radicle.network/nodes/seed.radicle.garden/rad%3Azs18Rifa7437q7hTFhsx11nYeGhD), you can check them via:

- 🌐 [the role's documentation](https://radicle.network/nodes/seed.radicle.garden/rad%3Azs18Rifa7437q7hTFhsx11nYeGhD/tree/docs/configuring-bitmagnet.md) online
- 📁 `roles/galaxy/bitmagnet/docs/configuring-bitmagnet.md` locally, if you have [fetched the Ansible roles](../installing.md)

>[!NOTE]
> Currently there does not exist a mechanism to limit how many torrents might be crawled. While [this section](https://bitmagnet.io/faq.html#what-are-the-system-requirements-for-bitmagnet) on the FAQ page claims that leaving the service running for several months will have 10 million torrents crawled, whose metadata should take around 80 GB disk space, eventually it will take up all available disk space.

## Dependencies

This service requires the following other services:

- [Postgres](postgres.md) database
- [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# bitmagnet                                                            #
#                                                                      #
########################################################################

bitmagnet_enabled: true

bitmagnet_hostname: bitmagnet.example.com

########################################################################
#                                                                      #
# /bitmagnet                                                           #
#                                                                      #
########################################################################
```

### Configuring HTTP Basic authentication

Since there does not exist an authentication system on the web interface, the HTTP Basic authentication on Traefik is enabled for the web interface by default, considering the nature of the service. See [this section](https://radicle.network/nodes/seed.radicle.garden/rad%3Azs18Rifa7437q7hTFhsx11nYeGhD/tree/docs/configuring-bitmagnet.md#configuring-http-basic-authentication) on the role's documentation for details about how to set it up.

### Integrating with Prometheus (optional)

bitmagnet can natively expose metrics to [Prometheus](prometheus.md).

#### Expose metrics internally

If bitmagnet and Prometheus do not share a network (like Traefik), you can connect the bitmagnet container network to Prometheus by adding the following configuration to your `vars.yml` file:

```yaml
prometheus_container_additional_networks_custom:
  - "{{ bitmagnet_container_network }}"
```

#### Expose metrics publicly

If bitmagnet metrics are not scraped from a local Prometheus instance, you can expose the metrics publicly so that a remote instance can fetch them.

When exposing metrics publicly, you should consider to set up [HTTP Basic Authentication](https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication) **or anyone would be able to read your metrics**.

To expose the metrics publicly, add the following configuration to your `vars.yml` file (adapt to your needs):

```yaml
mash_playbook_metrics_exposure_enabled: true
mash_playbook_metrics_exposure_hostname: mash.example.com
```

It will expose the metrics at `https://mash.example.com/metrics/mash-bitmagnet`.

To enable the HTTP Basic authentication, add the following configuration to your `vars.yml` file (adapt to your needs):

```yaml
bitmagnet_container_labels_traefik_metrics_middleware_basic_auth_enabled: true

# See https://doc.traefik.io/traefik/middlewares/http/basicauth/#users for details.
bitmagnet_container_labels_traefik_metrics_middleware_basic_auth_users: ""
```

## Usage

After running the command for installation, the bitmagnet instance becomes available at the URL specified with `bitmagnet_hostname`. With the configuration above, the service is hosted at `https://bitmagnet.example.com`.

To use it, open the URL on the browser and log in to the service if authentication is enabled.

## Troubleshooting

See [this section](https://radicle.network/nodes/seed.radicle.garden/rad%3Azs18Rifa7437q7hTFhsx11nYeGhD/tree/docs/configuring-bitmagnet.md#troubleshooting) on the role's documentation for details.

## Related services

- [qBittorrent](qbittorrent.md) — BitTorrent client written in native C++
