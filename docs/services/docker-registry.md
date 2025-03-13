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

With custom Traefik configuration (hint: see [`docker_registry_container_labels_traefik_rule_*` variables](https://github.com/mother-of-all-self-hosting/ansible-role-docker-registry/blob/main/defaults/main.yml) in the [docker-registry role](https://github.com/mother-of-all-self-hosting/ansible-role-docker-registry)), you may be able to add additional restrictions.

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

The base URL (e.g. `https://registry.example.com`) serves an empty (blank) page. To browse your registry's images via a web interface, you may need another piece of software, like [Docker Registry Browser](docker-registry-browser.md).


## Recommended other services

- [Docker Registry Browser](docker-registry-browser.md) — Web Interface for the Docker Registry HTTP API V2 written in Ruby on Rails
- [Docker Registry Purger](docker-registry-purger.md) — a small tool used for purging a private Docker Registry's old tags
