# Traefik

[Traefik](https://doc.traefik.io/traefik/) is a container-aware reverse-proxy server.

Many of the services installed by this playbook need to be exposed to the web (HTTP/HTTPS). This is handled by Traefik, which is installed by default if you have used the [example `vars.yml` file](../../examples/vars.yml).

Enabling the Traefik service will automatically wire all other services to use it.


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process.

### Traefik managed by the playbook

```yaml
########################################################################
#                                                                      #
# traefik                                                              #
#                                                                      #
########################################################################

mash_playbook_reverse_proxy_type: playbook-managed-traefik

########################################################################
#                                                                      #
# /traefik                                                             #
#                                                                      #
########################################################################
```

Enabling the Traefik service, as shown above, automatically installs a [tecnativa/docker-socket-proxy](https://github.com/Tecnativa/docker-socket-proxy) service/container (powered by the [com.devture.ansible.role.container_socket_proxy](https://github.com/devture/com.devture.ansible.role.container_socket_proxy) Ansible role) to improve security by not mounting a Docker socket into the Traefik container.

This [Ansible role we use for Traefik](https://github.com/mother-of-all-self-hosting/ansible-role-traefik) supports various configuration options. Feel free to consult [its `default/main.yml` variables file](https://github.com/mother-of-all-self-hosting/ansible-role-traefik/blob/main/defaults/main.yml).

Below, you can find some guidance about common tweaks you may wish to do.

### Traefik managed by you

Sometimes you may already have a Traefik instance running on the server and you may wish to not have the playbook install Traefik.

To tell the playbook that you're running a Traefik instance and you'd still like all services installed by the playbook to be connected to that Traefik instance, you need the following configuration:

```yml
# Tell the playbook you're using Traefik installed in another way.
# It won't bother installing Traefik.
mash_playbook_reverse_proxy_type: other-traefik-container

# Tell the playbook to attach services which require reverse-proxying to an additional network by default (e.g. traefik)
# This needs to match your Traefik network.
mash_playbook_reverse_proxyable_services_additional_network: traefik

# Uncomment and adjust the variables below if you'd like to enable HTTP-compression.
#
# For this to work, you will need to define a compress middleware (https://doc.traefik.io/traefik/middlewares/http/compress/) for your Traefik instance
# using a file (https://doc.traefik.io/traefik/providers/file/) or Docker (https://doc.traefik.io/traefik/providers/docker/) configuration provider.
#
# mash_playbook_reverse_proxy_traefik_middleware_compession_enabled: true
# mash_playbook_reverse_proxy_traefik_middleware_compession_name: my-compression-middleware@file
```

## Increase logging verbosity

```yaml
traefik_config_log_level: DEBUG
```

## Disable access logs

This will disable access logging.

```yaml
traefik_config_accessLog_enabled: false
```

## Enable Traefik Dashboard

This will enable a Traefik [Dashboard](https://doc.traefik.io/traefik/operations/dashboard/) UI at `https://traefik.mash.example.com/dashboard/` (note the trailing `/`).

```yaml
traefik_dashboard_enabled: true
traefik_dashboard_hostname: traefik.mash.example.com
traefik_dashboard_basicauth_enabled: true
traefik_dashboard_basicauth_user: YOUR_USERNAME_HERE
traefik_dashboard_basicauth_password: YOUR_PASSWORD_HERE
```

> [!WARNING]
> Enabling the dashboard on a hostname you use for something else (like `mash.example.com` in the configuration above) may cause conflicts. Enabling the Traefik Dashboard makes Traefik capture all `/dashboard` and `/api` requests and forward them to itself. If any of the services hosted on the same hostname requires any of these 2 URL prefixes, you will experience problems.

## Additional configuration

Use the `traefik_configuration_extension_yaml` variable provided by the Traefik Ansible role to override or inject additional settings, even when no dedicated variable exists.

```yaml
# This is a contrived example.
# You can enable and secure the Dashboard using dedicated variables. See above.
traefik_configuration_extension_yaml: |
  api:
    dashboard: true
```
