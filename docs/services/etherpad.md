<!--
SPDX-FileCopyrightText: 2020 Aaron Raimist
SPDX-FileCopyrightText: 2020 Chris van Dijk
SPDX-FileCopyrightText: 2020 Dominik Zajac
SPDX-FileCopyrightText: 2020 Mickaël Cornière
SPDX-FileCopyrightText: 2020-2024 MDAD project contributors
SPDX-FileCopyrightText: 2020-2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2021 Béla Becker
SPDX-FileCopyrightText: 2021 pushytoxin
SPDX-FileCopyrightText: 2022 François Darveau
SPDX-FileCopyrightText: 2022 Jim Myhrberg
SPDX-FileCopyrightText: 2022 Julian Foad
SPDX-FileCopyrightText: 2022 Nikita Chernyi
SPDX-FileCopyrightText: 2022 Warren Bailey
SPDX-FileCopyrightText: 2022 felixx9
SPDX-FileCopyrightText: 2023 Antonis Christofides
SPDX-FileCopyrightText: 2023 Felix Stupp
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 Thomas Miceli
SPDX-FileCopyrightText: 2024 Tiz
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Etherpad

The playbook can install and configure [Etherpad](https://etherpad.org), an open source collaborative text editor, for you.

See the project's [documentation](https://docs.etherpad.org/) to learn what it does and why it might be useful to you.

For details about configuring the [Ansible role for the server](https://github.com/mother-of-all-self-hosting/ansible-role-etherpad), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-etherpad/blob/main/docs/configuring-etherpad.md) online
- 📁 `roles/galaxy/etherpad/docs/configuring-etherpad.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- a datapase supported by [ueberdb2](https://www.npmjs.com/package/ueberdb2) such as [CouchDB](couchdb.md) / [Postgres](postgres.md) / MySQL / [MariaDB](mariadb.md) database — Etherpad will default to [SQLite](https://www.sqlite.org/) if Postgres is not enabled
- a [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# etherpad                                                             #
#                                                                      #
########################################################################

etherpad_enabled: true

etherpad_hostname: etherpad.example.com

########################################################################
#                                                                      #
# /etherpad                                                            #
#                                                                      #
########################################################################
```

As the most of the necessary settings for the role have been taken care of by the playbook, you can enable Etherpad on your server with this minimum configuration.

See the role's documentation for details about configuring Etherpad per your preference (such as [database type](https://github.com/mother-of-all-self-hosting/ansible-role-etherpad/blob/main/docs/configuring-etherpad.md#configure-database), [the name of the instance](https://github.com/mother-of-all-self-hosting/ansible-role-etherpad/blob/main/docs/configuring-etherpad.md#set-the-name-of-the-instance-optional) and [the default pad text](https://github.com/mother-of-all-self-hosting/ansible-role-etherpad/blob/main/docs/configuring-etherpad.md#set-the-default-text-optional)).

### Create admin user (optional)

You probably might want to enable authentication to disallow anonymous access to your Etherpad.

It is possible to enable HTTP basic authentication by **creating an admin user** with `etherpad_admin_username` and `etherpad_admin_password` variables. The admin user account is also used by plugins for authentication and authorization.

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-etherpad/blob/main/docs/configuring-etherpad.md#create-admin-user-optional) on the role's documentation for details about how to create the admin user.

### Control Etherpad's availability on Jitsi conferences (optional)

If a Jitsi video-conferencing platform (see [our docs on Jitsi](jitsi.md)) is enabled on your server, you can configure it so to make Etherpad available on conferences.

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-jitsi/blob/main/docs/configuring-jitsi.md#control-etherpads-availability-on-jitsi-conferences) on the Jitsi role's documentation for details about how to set it up.

### Integrating with Prometheus (optional)

Etherpad can natively expose metrics to [Prometheus](prometheus.md).

#### Expose metrics internally

If Etherpad and Prometheus do not share a network (like Traefik), you can connect the Etherpad container network to Prometheus by adding the following configuration to your `vars.yml` file:

```yaml
prometheus_container_additional_networks_custom:
  - "{{ etherpad_container_network }}"
```

#### Expose metrics publicly

If Etherpad metrics are not scraped from a local Prometheus instance, you can expose the metrics publicly so that a remote instance can fetch them.

When exposing metrics publicly, you should consider to set up [HTTP Basic Authentication](https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication) **or anyone would be able to read your metrics**.

To expose the metrics publicly, add the following configuration to your `vars.yml` file (adapt to your needs):

```yaml
mash_playbook_metrics_exposure_enabled: true
mash_playbook_metrics_exposure_hostname: mash.example.com
```

It will expose the metrics at `https://mash.example.com/metrics/mash-etherpad`.

To enable the HTTP Basic authentication, add the following configuration to your `vars.yml` file (adapt to your needs):

```yaml
etherpad_container_labels_traefik_metrics_middleware_basic_auth_enabled: true

# See https://doc.traefik.io/traefik/middlewares/http/basicauth/#users for details.
etherpad_container_labels_traefik_metrics_middleware_basic_auth_users: ""
```

## Usage

After running the command for installation, the Etherpad instance becomes available at the URL specified with `etherpad_hostname`. With the configuration above, the service is hosted at `https://etherpad.example.com`. The admin UI (if enabled) becomes available at `https://etherpad.example.com/admin`.

💡 See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-etherpad/blob/main/docs/configuring-etherpad.md#usage) on the role's documentation for more information about usage.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-etherpad/blob/main/docs/configuring-etherpad.md#troubleshooting) on the role's documentation for details.

## Related services

- [CodiMD](codimd.md) — Realtime collaborative markdown notes on all platforms
- [SilverBullet](silverbullet.md) — Programmable, private, personal knowledge management platform
