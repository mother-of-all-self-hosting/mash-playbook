<!--
SPDX-FileCopyrightText: 2024 Nikita Chernyi
SPDX-FileCopyrightText: 2025, 2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Docker Registry Proxy

The playbook can install and configure [Docker Registry Proxy](https://github.com/etkecc/docker-registry-proxy) for you.

Docker Registry Proxy is a pass-through Docker registry (distribution) proxy with metadata caching, Docker-compatible errors, Prometheus metrics, etc.

See the project's [documentation](https://github.com/etkecc/docker-registry-proxy/blob/main/README.md) to learn what Docker Registry Proxy does and why it might be useful to you.

For details about configuring the [Ansible role for Docker Registry Proxy](https://github.com/mother-of-all-self-hosting/ansible-role-docker-registry-proxy), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-docker-registry-proxy/blob/main/docs/configuring-docker-registry-proxy.md) online
- 📁 `roles/galaxy/docker_registry_proxy/docs/configuring-docker-registry-proxy.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# docker_registry_proxy                                                #
#                                                                      #
########################################################################

docker_registry_proxy_enabled: true

docker_registry_proxy_hostname: registry.example.com

########################################################################
#                                                                      #
# /docker_registry_proxy                                               #
#                                                                      #
########################################################################
```

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-docker-registry-proxy/blob/main/docs/configuring-docker-registry-proxy.md#adjusting-the-playbook-configuration) on the role's documentation for details about other settings.

## Usage

After running the command for installation, the Docker Registry Proxy instance becomes available at the URL specified with `registry_hostname`. With the configuration above, the service is hosted at `https://registry.example.com`.

## Related services

- [Distribution Registry](docker-registry.md) — Container image distribution registry
  - Wired automatically to the proxy
- [Grafana](grafana.md) — Web-based tool for visualizing your Prometheus metrics (time-series)
  - Docker Registry Proxy comes with [pre-configured grafana dashboard](https://github.com/etkecc/docker-registry-proxy/blob/main/contrib/grafana-dashboard.json)
