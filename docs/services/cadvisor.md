# cAdvisor

This playbook can configure [cAdvisor](https://github.com/google/cadvisor)

## Dependencies

This service requires the following other services:

-   (optionally) [Traefik](traefik.md) - a reverse-proxy server for exposing cadvisor publicly
-   (optionally) [Prometheus](./prometheus.md) - a database for storing metrics
-   (optionally) [Grafana](./grafana.md) - a web UI that can query the prometheus datasource (connection) and display the logs

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# cadvisor                                                             #
#                                                                      #
########################################################################

cadvisor_enabled: true
# You will have to mount specific folders depending on your need
# cadvisor_container_extra_arguments:
#   - "--mount type=bind,source=/,destination=/rootfs,readonly"
#   - "--mount type=bind,source=/sys,destination=/sys,readonly"
#   - "--mount type=bind,source=/var/lib/docker/,destination=/var/lib/docker,readonly"
#   - "--mount type=bind,source=/dev/disk/,destination=/dev/disk,readonly"

########################################################################
#                                                                      #
# /cadvisor                                                            #
#                                                                      #
########################################################################
```

See the full list of options in the [default/main.yml](default/main.yml) file

cAdvisor can scrape metrics from system and containers. These metrics can be :

-   Displayed on the cAdvisor Web UI
-   Exposed to a metric-storage server like [Prometheus](./prometheus.md).

## Exposing publicly the Web UI

To expose cAdvisor to the web, you need to assign a hostname in `cadvisor_hostname` and optionally a path-prefix.

```yaml
# To expose the metrics publicly, enable and configure the lines below:
cadvisor_hostname: mash.example.com
cadvisor_path_prefix: /

# To protect the metrics with HTTP Basic Auth, enable and configure the lines below.
# See: https://doc.traefik.io/traefik/middlewares/http/basicauth/#users
cadvisor_container_labels_traefik_middleware_basic_auth_enabled: true
cadvisor_container_labels_traefik_middleware_basic_auth_users: ""
```

### Exposing metrics publicly

Unless you're scraping the cadvisor metrics from a local [Prometheus](prometheus.md) instance, as described in [Integrating with Prometheus](cadvisor.md#), you will probably wish to expose the metrics publicly so that a remote Prometheus instance can fetch them. When exposing publicly, it's natural to set up [HTTP Basic Authentication](https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication) **or anyone would be able to read your metrics**.

```yaml
cadvisor_container_labels_metrics_enabled: true

# To expose the metrics publicly, enable and configure the lines below:
<!-- cadvisor_hostname: mash.example.com -->
<!-- cadvisor_path_prefix: /metrics/mash-cadvisor -->

# To protect the metrics with HTTP Basic Auth, enable and configure the lines below.
# See: https://doc.traefik.io/traefik/middlewares/http/basicauth/#users
cadvisor_container_labels_metrics_middleware_basic_auth_enabled: true
cadvisor_container_labels_metrics_middleware_basic_auth_users: ""
```

## Integrating with Prometheus

cAdvisor can expose its metrics to [Prometheus](./prometheus.md).

### Prerequesites

The bare minimium is to ensure Prometheus can reach cadvisor.

-   If cadvisor is on a different host than Prometheus, refer to section [Expose metrics publicly](cadvisor.md#)
-   If cadvisor is on the same host than prometheus, refer to section [Ensure Prometheus is on the same container network as cadvisor.](cadvisor.md#)

### Ensure Prometheus is on the same container network as cAdvisor.

If you are using MASH playbook, cadvisor should already be connected to prometheus container network

If cadvisor and prometheus do not share a network, you will have to

-   Either connect Prometheus container network to cadvisor by editing `prometheus_container_additional_networks_auto`
-   Either connect cadvisor container network to Prometheus by editing `cadvisor_container_additional_networks_custom`

Exemple:

```yaml
prometheus_container_additional_networks:
    - "{{ cadvisor_container_network }}"
```

### Write the scrape config for prometheus

# Healthcheck

```yaml
cadvisor_environment_variables_extension: |

# CADVISOR_HEALTHCHECK_URL=http://localhost:8080/cadvisor/healthz
```

## Usage

After [installing](../installing.md), refer to the documentation of [cAdvisor](https://github.com/google/cadvisor).
