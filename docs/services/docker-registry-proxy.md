# Docker Registry Proxy

[Docker Registry Proxy](https://gitlab.com/etke.cc/docker-registry-proxy/) is a pass-through docker registry (distribution) proxy with metadata caching, docker-compatible errors, prometheus metrics, etc.


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
# /docker-registry-proxy                                             #
#                                                                      #
########################################################################
```

In the example configuration above, we configure the service to be hosted at `https://registry.example.com`.

## Usage

After installation, you should be able to go to the URL as configured via `docker_registry_proxy_hostname`.

## Recommended other services

- [Docker Registry](docker-registry.md) — a container image distribution registry developed by [Docker Inc](https://www.docker.com/), wired automatically to the proxy, just disable registry's traefik labels
- [Grafana](grafana.md) — a multi-platform open source analytics and interactive visualization web application, Docker Registry Proxy comes with [pre-configured grafana dashboard](https://gitlab.com/etke.cc/docker-registry-proxy/-/blob/main/contrib/grafana-dashboard.json)
