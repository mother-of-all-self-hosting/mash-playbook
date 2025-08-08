<!--
SPDX-FileCopyrightText: 2020 - 2024 MDAD project contributors
SPDX-FileCopyrightText: 2020 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2020 Aaron Raimist
SPDX-FileCopyrightText: 2020 Chris van Dijk
SPDX-FileCopyrightText: 2020 Dominik Zajac
SPDX-FileCopyrightText: 2020 Mickaël Cornière
SPDX-FileCopyrightText: 2022 François Darveau
SPDX-FileCopyrightText: 2022 Julian Foad
SPDX-FileCopyrightText: 2022 Warren Bailey
SPDX-FileCopyrightText: 2023 Antonis Christofides
SPDX-FileCopyrightText: 2023 Felix Stupp
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# APISIX Dashboard

The playbook can install and configure [APISIX Dashboard](https://apisix.apache.org/docs/dashboard/USER_GUIDE/) for you.

APISIX Dashboard is a web UI for [APISIX Gateway](./apisix-gateway.md). It works by directly editing the [etcd](./etcd.md) database that APISIX Gateway stores its data in.

See the project's [documentation](https://apisix.apache.org/docs/dashboard/USER_GUIDE/) to learn what APISIX Dashboard does and why it might be useful to you.

## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server
- an [etcd](etcd.md) key-value store
- (optional) [APISIX Gateway](./apisix-gateway.md) — there's no point in administrating APISIX Gateway configuration stored in etcd without having an APISIX Gateway instance to initialize and consume it

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# apisix_dashboard                                                     #
#                                                                      #
########################################################################

apisix_dashboard_enabled: true

apisix_dashboard_hostname: dashboard.api.example.com

# A strong secret for JWT authentication
apisix_dashboard_config_authentication_secret: ''

apisix_dashboard_config_authentication_users:
  - username: admin
    password: password-here

########################################################################
#                                                                      #
# /apisix_dashboard                                                    #
#                                                                      #
########################################################################
```

### Authentication

The example above uses the built-in login page of APISIX Dashboard with a list of users is defined via `apisix_dashboard_config_authentication_users`.

APISIX Dashboard also supports OpenID Connect providers. It can be enabled and configured via various `apisix_dashboard_config_oidc_*` Ansible variables.

### Extending the configuration

There are some additional things you may wish to configure about the component.

Take a look at:

- [`ansible-role-apisix-dashboard` Ansible role](https://github.com/mother-of-all-self-hosting/ansible-role-apisix-dashboard)'s [`defaults/main.yml`](https://github.com/mother-of-all-self-hosting/ansible-role-apisix-dashboard/blob/main/defaults/main.yml) for some variables that you can customize via your `vars.yml` file.

## Usage

After running the command for installation, the APISIX Dashboard instance becomes available at the URL specified with `apisix_dashboard_hostname`. With the configuration above, the service is hosted at `https://dashboard.api.example.com`.

You can open the APISIX Dashboard URL and authenticate with a credential as specified in `apisix_dashboard_config_authentication_users`. If you've enabled OpenID Connect, you may also be able to authenticate with that.
