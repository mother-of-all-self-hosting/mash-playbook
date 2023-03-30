# Traefik

[Traefik](https://doc.traefik.io/traefik/) is a container-aware reverse-proxy server.

Many of the services installed by this playbook need to be exposed to the web (HTTP/HTTPS). This is handled by Traefik.

Enabling the Traefik service will automatically wire all other services to use it.


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# devture-traefik                                                      #
#                                                                      #
########################################################################

mash_playbook_reverse_proxy_type: playbook-managed-traefik

# The email address that Traefik will pass to Let's Encrypt when obtaining SSL certificates
devture_traefik_config_certificatesResolvers_acme_email: your-email@example.com

# Or, if you'd like to install Traefik yourself:
#
# mash_playbook_reverse_proxy_type: other-traefik-container
# mash_playbook_reverse_proxyable_services_additional_network: traefik

########################################################################
#                                                                      #
# /devture-traefik                                                     #
#                                                                      #
########################################################################
```

Enabling the Traefik service, as shown above, automatically installs a [tecnativa/docker-socket-proxy](https://github.com/Tecnativa/docker-socket-proxy) service/container (powered by the [com.devture.ansible.role.container_socket_proxy](https://github.com/devture/com.devture.ansible.role.container_socket_proxy) Ansible role) to improve security by not mounting a Docker socket into the Traefik container.
