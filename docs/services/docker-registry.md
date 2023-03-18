# Docker Registry

[Docker Registry](https://docs.docker.com/registry/) is a container image distribution registry developed by [Docker Inc](https://www.docker.com/).

This playbook supports installing a container image registry which is:

- completely public, when it comes to pulling images
- IP-restricted, when it comes to pushing images

Authentication is not supported.


## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# docker-registry                                                      #
#                                                                      #
########################################################################

docker_registry_enabled: true

docker_registry_hostname: registry.example.com

# Uncomment the line below if you'd like to allow for image deletion.
# docker_registry_storage_delete_enabled: true

# Only whitelisted IPs will be able to perform DELETE, PATCH, POST, PUT requests against the registry.
# All other IP addresses get read-only (GET, HEAD) access.
docker_registry_private_services_whitelisted_ip_ranges:
  - 1.2.3.4/32
  - 4.3.2.1/32

########################################################################
#                                                                      #
# /docker-registry                                                     #
#                                                                      #
########################################################################
```

In the example configuration above, we configure the service to be hosted at `https://registry.example.com`.


## Usage

After installation, you should be able to:

- pull images from your registry from any IP address
- push images to your registry from the whitelisted IP addresses (`docker_registry_private_services_whitelisted_ip_ranges`)

With custom Traefik configuration (hint: see `docker_registry_container_labels_traefik_rule_*` variables in the [docker_registry role]()), you may be able to add additional restrictions.

To **test pushing** images, try the following:

```sh
docker pull docker.io/alpine:3.17.2
docker tag docker.io/alpine:3.17.2 registry.example.com/alpine:3.17.2
docker push registry.example.com/alpine:3.17.2
```

To **test pulling** images, try the following:

```sh
# Clean up from before
docker rmi registry.example.com/alpine:3.17.2

docker pull registry.example.com/alpine:3.17.2
```

The base URL (e.g. `https://registry.example.com`) serves an empty (blank) page. To browse your registry's images, you may need another piece of software, like [klausmeyer/docker-registry-browser](https://github.com/klausmeyer/docker-registry-browser/tree/master) which is not yet supported by this playbook, but will be supported soon.


## Recommended other services

- Docker Registry Browser - support coming to this playbook soon
- Docker Registry Purger - support coming to this playbook soon
