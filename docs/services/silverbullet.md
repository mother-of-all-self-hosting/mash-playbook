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

# SilverBullet

The playbook can install and configure [SilverBullet](https://silverbullet.md) for you.

SilverBullet is a programmable, private, personal knowledge management platform.

See the project's [documentation](https://silverbullet.md/Manual) to learn what SilverBullet does and why it might be useful to you.

For details about configuring the [Ansible role for SilverBullet](https://radicle.network/nodes/seed.radicle.garden/rad%3Az3PxyXm3EXE4xCNKcaKVKmtdjVNog), you can check them via:

- 🌐 [the role's documentation](https://radicle.network/nodes/seed.radicle.garden/rad%3Az3PxyXm3EXE4xCNKcaKVKmtdjVNog/tree/docs/configuring-silverbullet.md) online
- 📁 `roles/galaxy/silverbullet/docs/configuring-silverbullet.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# silverbullet                                                         #
#                                                                      #
########################################################################

silverbullet_enabled: true

silverbullet_hostname: silverbullet.example.com

########################################################################
#                                                                      #
# /silverbullet                                                        #
#                                                                      #
########################################################################
```

**Note**: hosting SilverBullet under a subpath (by configuring the `silverbullet_path_prefix` variable) does not seem to be possible due to SilverBullet's technical limitations.

### Set the username and password

You also need to create an instance's user to access to the UI after installation. See [this section](https://radicle.network/nodes/seed.radicle.garden/rad%3Az3PxyXm3EXE4xCNKcaKVKmtdjVNog/tree/docs/configuring-silverbullet.md#set-the-username-and-password) on the role's documentation for details.

### Integrating with Prometheus (optional)

SilverBullet can natively expose metrics to [Prometheus](prometheus.md).

#### Expose metrics internally

If SilverBullet and Prometheus do not share a network (like Traefik), you can connect the SilverBullet container network to Prometheus by adding the following configuration to your `vars.yml` file:

```yaml
prometheus_container_additional_networks_custom:
  - "{{ silverbullet_container_network }}"
```

#### Expose metrics publicly

If SilverBullet metrics are not scraped from a local Prometheus instance, you can expose the metrics publicly so that a remote instance can fetch them.

When exposing metrics publicly, you should consider to set up [HTTP Basic Authentication](https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication) **or anyone would be able to read your metrics**.

To expose the metrics publicly, add the following configuration to your `vars.yml` file (adapt to your needs):

```yaml
mash_playbook_metrics_exposure_enabled: true
mash_playbook_metrics_exposure_hostname: mash.example.com
```

It will expose the metrics at `https://mash.example.com/metrics/mash-silverbullet`.

To enable the HTTP Basic authentication, add the following configuration to your `vars.yml` file (adapt to your needs):

```yaml
silverbullet_container_labels_traefik_metrics_middleware_basic_auth_enabled: true

# See https://doc.traefik.io/traefik/middlewares/http/basicauth/#users for details.
silverbullet_container_labels_traefik_metrics_middleware_basic_auth_users: ""
```

## Usage

After running the command for installation, the SilverBullet instance becomes available at the URL specified with `silverbullet_hostname`. With the configuration above, the service is hosted at `https://silverbullet.example.com`.

## Troubleshooting

See [this section](https://radicle.network/nodes/seed.radicle.garden/rad%3Az3PxyXm3EXE4xCNKcaKVKmtdjVNog/tree/docs/configuring-silverbullet.md#troubleshooting) on the role's documentation for details.

## Related services

- [CodiMD](codimd.md) — Realtime collaborative markdown notes on all platforms
- [Etherpad](etherpad.md) — Collaborative text editor
- [flatnotes](flatnotes.md) — Database-less note taking web app that utilises a flat folder of markdown files for storage
