<!--
SPDX-FileCopyrightText: 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# APISIX

The playbook can install and configure [APISIX](https://apisix.apache.org/docs/apisix/getting-started/README/) for you.

APISIX is an [API Gateway](https://apisix.apache.org/docs/apisix/terminology/api-gateway/) and Ingress Controller.

For details about configuring the [Ansible role for APISIX](https://github.com/mother-of-all-self-hosting/ansible-role-apisix), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-apisix/blob/main/docs/configuring-apisix.md) online
- 📁 `roles/galaxy/apisix/docs/configuring-apisix.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [etcd](etcd.md) key-value store
- [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# apisix                                                               #
#                                                                      #
########################################################################

apisix_enabled: true

# Configure the hostname and path at which the API would be exposed
apisix_hostname: api.example.com
apisix_path_prefix: /api

########################################################################
#                                                                      #
# /apisix                                                              #
#                                                                      #
########################################################################
```

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-apisix/blob/main/docs/configuring-apisix.md#adjusting-the-playbook-configuration) on the role's documentation for other settings such as the one for exposing Admin API (with recommended configurations to reduce attack surfaces).

## Usage

After running the command for installation, the APISIX instance becomes available. Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-apisix/blob/main/docs/configuring-apisix.md#usage) on the role's documentation for details.

## Related services

- [etcd](etcd.md) — Distributed key-value store, where APISIX keeps its configuration
- [Traefik](traefik.md) — Reverse-proxy server which fronts APISIX's listeners
