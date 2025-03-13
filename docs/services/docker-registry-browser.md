# Docker Registry Browser

[Docker Registry Browser](https://github.com/klausmeyer/docker-registry-browser) is a Web Interface for the Docker Registry HTTP API V2 written in Ruby on Rails.


## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# docker-registry-browser                                              #
#                                                                      #
########################################################################

docker_registry_browser_enabled: true

# Hosting under a subpath (such as `/browser`) allows the browser to co-exist
# on the same hostname as a Docker Registry instance (see `docker-registry.md`).
docker_registry_browser_hostname: registry.example.com
docker_registry_browser_path_prefix: /browser

# If the browser will be able to delete images and live on the same private container network
# as the registry itself (like we do below), it's recommended to protect it with HTTP Basic Auth.
#
# If you're running a read-only browser, you may leave it publicly accessible.
docker_registry_browser_basic_auth_enabled: true
docker_registry_browser_basic_auth_username: admin
# You can put any string here, but generating a strong one is preferred (e.g. `pwgen -s 64 1`).
docker_registry_browser_basic_auth_password: ''

# To integrate with a locally running (in a container) Docker Registry (see `docker-registry.md`),
# point to its local container address and configure the browser to run in the registry's network.
docker_registry_browser_docker_registry_url: "http://{{ docker_registry_identifier }}:5000"
docker_registry_browser_container_network: "{{ docker_registry_container_network }}"

# Alternatively, to use a registry running elsewhere, delete both lines above
# (docker_registry_browser_docker_registry_url and docker_registry_browser_container_network),
# and use something this instead:
# docker_registry_browser_docker_registry_url: "https://registry.example.com"

# Image deletion is disabled by default, so you need to explicitly enable it if you need it.
docker_registry_browser_enabled_delete_images: true

########################################################################
#                                                                      #
# /docker-registry-browser                                             #
#                                                                      #
########################################################################
```

In the example configuration above, we configure the service to be hosted at `https://registry.example.com/browser`.

If you make the registry browser live on the same container network as the [Docker Registry](docker-registry.md) itself (like we've done by overriding `docker_registry_browser_container_network` above), the browser will be able to talk to the registry over the private container network and IP restrictions (such as those defined in `docker_registry_private_services_whitelisted_ip_ranges`) will not be able to stop it.


## Usage

After installation, you should be able to go to the URL as configured via `docker_registry_browser_hostname` and `docker_registry_browser_path_prefix`.

You should be able to browse the images and possibly delete them (if enabled via `docker_registry_browser_enabled_delete_images`).


## Recommended other services

- [Docker Registry](docker-registry.md) — a container image distribution registry developed by [Docker Inc](https://www.docker.com/)
