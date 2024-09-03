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

## Exposing publicly cAdvisor

To expose cAdvisor WebUI and metrics to the web, you need to assign a hostname in `cadvisor_hostname` and optionally a path-prefix.

```yaml
# To expose the metrics publicly, enable and configure the lines below:
cadvisor_hostname: mash.example.com
cadvisor_path_prefix: /

# To protect the web ui and your metrics with HTTP Basic Auth, enable and configure the lines below.
# See: https://doc.traefik.io/traefik/middlewares/http/basicauth/#users
cadvisor_container_labels_traefik_middleware_basic_auth_enabled: true
cadvisor_container_labels_traefik_middleware_basic_auth_users: ""
```

## Integrating with Prometheus

### Prerequesites

The bare minimium is to ensure Prometheus can reach cadvisor.

-   If cadvisor is on a different host than Prometheus, refer to section [Exposing publicly cAdvisor](cadvisor.md#Exposing-publicly-cAdvisor)
-   If cadvisor is on the same host than prometheus, refer to section [Ensure Prometheus is on the same container network as cadvisor.](cadvisor.md#)

### Ensure Prometheus is on the same container network as cAdvisor.

If cadvisor and prometheus do not share a network, you will have to

-   Either connect Prometheus container network to cadvisor by editing `prometheus_container_additional_networks_auto`
-   Either connect cadvisor container network to Prometheus by editing `cadvisor_container_additional_networks_custom`

Exemple:

```yaml
prometheus_container_additional_networks:
    - "{{ cadvisor_container_network }}"
```

### Write the scrape config for prometheus

```yaml
prometheus_config_scrape_configs_additional:
    - job_name: cadvisor
      scrape_interval: 5s
      scrape_timeout: 5s
      static_configs:
          - targets:
                - "{{ cadvisor_identifier }}:8080"
```

replace the target by your ip_adress:port if cAdvisor is on a different host than Prometheus

## Usage

After [installing](../installing.md), refer to the documentation of [cAdvisor](https://github.com/google/cadvisor).
