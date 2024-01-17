# Traefik

[Traefik](https://doc.traefik.io/traefik/) is a container-aware reverse-proxy server.

Many of the services installed by this playbook need to be exposed to the web (HTTP/HTTPS). This is handled by Traefik, which is installed by default if you have used the [example `vars.yml` file](../../examples/vars.yml).

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


This [Ansible role we use for Traefik](https://github.com/devture/com.devture.ansible.role.traefik) supports various configuration options. Feel free to consult [its `default/main.yml` variables file](https://github.com/devture/com.devture.ansible.role.traefik/blob/main/defaults/main.yml).

Below, you can find some guidance about common tweaks you may wish to do.

## Using another Traefik instance (not installing Traefik)

Sometimes you may already have a Traefik instance running on the server and you may wish to not have the playbook install Traefik.

To tell the playbook that you're running a Traefik instance and you'd still like all services installed by the playbook to be connected to that Traefik instance, you need the following configuration:

```yml
# Tell the playbook you're using Traefik installed in another way.
# It won't bother installing Traefik.
mash_playbook_reverse_proxy_type: other-traefik-container

# Tell the playbook to attach services which require reverse-proxying to an additional network by default (e.g. traefik)
# This needs to match your Traefik network.
mash_playbook_reverse_proxyable_services_additional_network: traefik
```

## Increase logging verbosity

```yaml
devture_traefik_config_log_level: DEBUG
```

## Disable access logs

This will disable access logging.

```yaml
devture_traefik_config_accessLog_enabled: false
```

## Enable Traefik Dashboard

This will enable a Traefik [Dashboard](https://doc.traefik.io/traefik/operations/dashboard/) UI at `https://traefik.mash.example.com/dashboard/` (note the trailing `/`).

```yaml
devture_traefik_dashboard_enabled: true
devture_traefik_dashboard_hostname: traefik.mash.example.com
devture_traefik_dashboard_basicauth_enabled: true
devture_traefik_dashboard_basicauth_user: YOUR_USERNAME_HERE
devture_traefik_dashboard_basicauth_password: YOUR_PASSWORD_HERE
```

**WARNING**: enabling the dashboard on a hostname you use for something else (like `mash.example.com` in the configuration above) may cause conflicts. Enabling the Traefik Dashboard makes Traefik capture all `/dashboard` and `/api` requests and forward them to itself. If any of the services hosted on the same hostname requires any of these 2 URL prefixes, you will experience problems.

## Additional configuration

Use the `devture_traefik_configuration_extension_yaml` variable provided by the Traefik Ansible role to override or inject additional settings, even when no dedicated variable exists.

```yaml
# This is a contrived example.
# You can enable and secure the Dashboard using dedicated variables. See above.
devture_traefik_configuration_extension_yaml: |
  api:
    dashboard: true
```
