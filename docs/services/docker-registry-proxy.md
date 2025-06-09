<!--
SPDX-FileCopyrightText: 2024 Nikita Chernyi
SPDX-FileCopyrightText: 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Docker Registry Proxy

[Docker Registry Proxy](https://github.com/etkecc/docker-registry-proxy) is a pass-through Docker registry (distribution) proxy with metadata caching, Docker-compatible errors, Prometheus metrics, etc.

## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# docker-registry-proxy                                                #
#                                                                      #
########################################################################

docker_registry_proxy_enabled: true

docker_registry_proxy_hostname: registry.example.com

# List of the IPs allowed to access the registry (GET, HEAD, OPTIONS requests only)
docker_registry_proxy_allowed_ips: []

# List of the User Agent names(!) allowed to access the registry (GET, HEAD, OPTIONS requests only)
docker_registry_proxy_allowed_uas:
- docker

# List of the IPs trusted to access the registry (PATCH, POST, PUT, DELETE requests only)
docker_registry_proxy_trusted_ips: []

########################################################################
#                                                                      #
# /docker-registry-proxy                                               #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, Docker Registry Proxy becomes available at the specified hostname such as `https://registry.example.com`.

## Recommended other services

- [Docker Registry](docker-registry.md) — a container image distribution registry developed by [Docker Inc](https://www.docker.com/), wired automatically to the proxy, just disable registry's Traefik labels
- [Grafana](grafana.md) — a multi-platform open source analytics and interactive visualization web application, Docker Registry Proxy comes with [pre-configured grafana dashboard](https://gitlab.com/etke.cc/docker-registry-proxy/-/blob/main/contrib/grafana-dashboard.json)
