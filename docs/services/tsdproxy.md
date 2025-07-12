# TSDProxy

[TSDProxy](https://almeidapaulopt.github.io/tsdproxy/) is an application that automatically creates a proxy to virtual addresses in your [Tailscale](https://tailscale.com/) network.


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

It is mandatory to set the following variables:

```yaml
########################################################################
#                                                                      #
# tsdproxy                                                             #
#                                                                      #
########################################################################

tsdproxy_enabled: true

tsdproxy_tailscale_authkey: '' # OR
tsdproxy_tailscale_authkeyfile: '' # use this to load authkey from file. If this is defined, Authkey is ignored

########################################################################
#                                                                      #
# /tsdproxy                                                            #
#                                                                      #
########################################################################
```

If [com.devture.ansible.role.container_socket_proxy](https://github.com/devture/com.devture.ansible.role.container_socket_proxy) is installed by the playbook (default), the container will use the proxy.
If not, the container will mount the docker socket at `/var/run/docker.sock`, but you can change that by setting `tsdproxy_docker_socket` to something else. Don't forget to adjust the `tsdproxy_docker_endpoint_is_unix_socket` to false if you are using a tcp endpoint.

## Usage

## Adding a new service

This proxy creates a separate Tailscale machine (node) in the Tailscale network for each service, without creating a sidecar container each time.

To add a new service, you have to make sure that the service and proxy are in a same container network. You can do this by adding the proxy to the network of the service or the other way round.

```yaml
tsdproxy_container_additional_networks_custom:
  - YOUR-SERVICE-NETWORK
# OR
YOUR-SERVICE_container_additional_networks_custom:
  - "{{ tsdproxy_container_network }}"
```

The next step is to add the service to the proxy.

### Connecting a service to the proxy via container labels

```yaml
YOUR-SERVICE_container_labels_additional_labels: |
  tsdproxy.enable: "true"
  tsdproxy.container_port: 8080
```

The following labels are optional, please read the [official TSDProxy documentation](https://almeidapaulopt.github.io/tsdproxy/docs/docker/) for more information.

```yaml
  tsdproxy.name: "my-service"
  tsdproxy.autodetect: "false"
  tsdproxy.proxyprovider: "providername"
  tsdproxy.ephemeral: "false"
  tsdproxy.funnel: "false"
```

### Connecting a service to the proxy via a Proxy list

An alternative way to add a service to the proxy is to use Proxy files.

Please read the [official TSDProxy documentation](https://almeidapaulopt.github.io/tsdproxy/docs/files/) for more information.

You will need to use the `tsdproxy_config_files` variable and add your proxy list file into the config folder, most likely `/mash/tsdproxy/config/`.
This is possible manually or by using [AUX-Files](./auxiliary.md).
