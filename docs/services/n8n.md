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
SPDX-FileCopyrightText: 2023 kinduff
SPDX-FileCopyrightText: 2024 Thomas Miceli
SPDX-FileCopyrightText: 2024 Tiz
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# n8n

The playbook can install and configure [n8n](https://n8n.io/) for you.

n8n is a workflow automation tool for technical people.

See the project's [documentation](https://docs.n8n.io/) to learn what n8n does and why it might be useful to you.

For details about configuring the [Ansible role for n8n](https://github.com/mother-of-all-self-hosting/ansible-role-n8n), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-n8n/blob/main/docs/configuring-n8n.md) online
- 📁 `roles/galaxy/actual/docs/configuring-actual.md` locally, if you have [fetched the Ansible roles](../installing.md)

>[!WARNING]
> n8n is licensed under [Sustainable Use License](https://github.com/n8n-io/n8n/blob/master/LICENSE.md). Because we had discouraged using [Redis](redis.md) as it was provided under "source available" model (note: Redis has retracted its stance in the end and since version 8.0 it was started to be released under multiple licenses, one of which is AGPL-3.0), we do not encourage using n8n either on the same ground.

## Dependencies

This service requires the following other services:

- [Postgres](postgres.md) / [SQLite](https://www.sqlite.org/) database
- [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# n8n                                                                  #
#                                                                      #
########################################################################

n8n_enabled: true

n8n_hostname: n8n.example.com

########################################################################
#                                                                      #
# /n8n                                                                 #
#                                                                      #
########################################################################
```

**Note**: hosting n8n under a subpath (by configuring the `n8n_path_prefix` variable) does not seem to be possible due to n8n's technical limitations.

### Select database to use

n8n can use either Postgres or SQLite, and you need to choose one. Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-n8n/blob/main/docs/configuring-n8n.md#specify-database) on the role's documentation for details.

>[!NOTE]
> If you have not disabled Postgres explicitly with this playbook, the database for your existing installation is most likely to be `postgres`.

### Integrating with Prometheus (optional)

n8n can natively expose metrics to [Prometheus](prometheus.md).

#### Expose metrics internally

If n8n and Prometheus do not share a network (like Traefik), you can connect the n8n container network to Prometheus by adding the following configuration to your `vars.yml` file:

```yaml
prometheus_container_additional_networks_custom:
  - "{{ n8n_container_network }}"
```

#### Expose metrics publicly

If n8n metrics are not scraped from a local Prometheus instance, you can expose the metrics publicly so that a remote instance can fetch them.

When exposing metrics publicly, you should consider to set up [HTTP Basic Authentication](https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication) **or anyone would be able to read your metrics**.

To expose the metrics publicly, add the following configuration to your `vars.yml` file (adapt to your needs):

```yaml
mash_playbook_metrics_exposure_enabled: true
mash_playbook_metrics_exposure_hostname: mash.example.com
```

It will expose the metrics at `https://mash.example.com/metrics/mash-n8n`.

To enable the HTTP Basic authentication, add the following configuration to your `vars.yml` file (adapt to your needs):

```yaml
n8n_container_labels_traefik_metrics_middleware_basic_auth_enabled: true

# See https://doc.traefik.io/traefik/middlewares/http/basicauth/#users for details.
n8n_container_labels_traefik_metrics_middleware_basic_auth_users: ""
```

## Usage

After running the command for installation, the n8n instance becomes available at the URL specified with `n8n_hostname` and `n8n_path_prefix`. With the configuration above, the service is hosted at `https://n8n.example.com/`.

To get started, open the URL with a web browser to create an account.

## Troubleshooting

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-n8n/blob/main/docs/configuring-n8n.md#troubleshooting) on the role's documentation for details.
