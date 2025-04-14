# Docker Registry Purger

[Docker Registry Purger](https://github.com/devture/docker-registry-purger) is a small tool used for purging a private Docker registry's old tags.


## Dependencies

This service requires to be pointed to a container registry. It may be a registry powered by [Docker Registry](docker-registry.md) or by some other software.


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# docker-registry-purger                                               #
#                                                                      #
########################################################################

docker_registry_purger_enabled: true

# To integrate with a locally running (in a container) Docker Registry (see `docker-registry.md`),
# point to its local container address and configure the purger to run in the registry's network.
docker_registry_purger_registry_url: "http://{{ docker_registry_identifier }}:5000"
docker_registry_purger_container_network: "{{ docker_registry_container_network }}"

# Alternatively, to use a registry running elsewhere, delete both lines above
# (docker_registry_purger_registry_url and docker_registry_purger_container_network),
# and use something this instead:
# docker_registry_purger_registry_url: "https://registry.example.com"

########################################################################
#                                                                      #
# /docker-registry-purger                                              #
#                                                                      #
########################################################################
```

You may wish to tweak some [default configuration]() variables, which ultimately control [environment variables](https://github.com/devture/docker-registry-purger#environment-variables) of the purger tool.


## Usage

After installation, you should be able to go to the URL as configured via `docker_registry_browser_hostname` and `docker_registry_browser_path_prefix`.

You should be able to browse the images and possibly delete them (if enabled via `docker_registry_browser_enabled_delete_images`).


## Recommended other services

- [Docker Registry](docker-registry.md) — a container image distribution registry developed by [Docker Inc](https://www.docker.com/)
