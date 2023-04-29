# WireGuard Easy

[WireGuard Easy](https://github.com/WeeJeWel/wg-easy) is the easiest way to run [WireGuard](https://www.wireguard.com/) VPN + Web-based Admin UI.

Another more powerful alternative for a self-hosted WireGuard VPN server is [Firezone](firezone.md). WireGuard Easy is easier, lighter and more compatible with various ARM devices.


## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server
- a modern Linux kernel which supports WireGuard


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# wg-easy                                                              #
#                                                                      #
########################################################################

wg_easy_enabled: true

wg_easy_hostname: mash.example.com

wg_easy_path_prefix: /wg-easy

wg_easy_environment_variables_additional_variable_wg_host: mash.example.com

# Put a strong password below, generated with `pwgen -s 64 1` or in another way
wg_easy_environment_variables_additional_variable_password: ''

# The default WireGuard port is 51820.
# Uncomment and change the lines below to use another one.
#
# The port that wg-easy advertises for WireGuard connectivity in profile files.
# wg_easy_environment_variables_additional_variable_wg_port: 51820
#
# The port that is actually published from the container.
# wg_easy_container_wireguard_bind_port: 51820

# The default DNS is 1.1.1.1.
# Uncomment and change the line below to use another one.
# wg_easy_environment_variables_additional_variable_wg_default_dns: 1.1.1.1

########################################################################
#                                                                      #
# /wg-easy                                                             #
#                                                                      #
########################################################################
```

### URL

In the example configuration above, we configure the service to be hosted at `https://mash.example.com/wg-easy`.

You can remove the `wg_easy_path_prefix` variable definition, to make it default to `/`, so that the service is served at `https://mash.example.com/`.


### Networking

**In addition** to ports `80` and `443` exposed by the [Traefik](traefik.md) reverse-proxy, the following ports will be exposed by the WireGuard containers on **all network interfaces**:

- `51820` over **UDP**, controlled by `wg_easy_environment_variables_additional_variable_wg_port` and `wg_easy_container_wireguard_bind_port` - used for [Wireguard](https://www.wireguard.com/) connections

Docker automatically opens these ports in the server's firewall, so you **likely don't need to do anything**. If you use another firewall in front of the server, you may need to adjust it.

### Additional configuration

For additional configuration options, see the upstream documentation's [Options](https://github.com/WeeJeWel/wg-easy#options) section.

You can inject additional environment variables with this additional configuration:

```yaml
wg_easy_environment_variables_additional_variables: |
  WG_DEFAULT_ADDRESS: 10.6.0.x
  WG_MTU: 1420
```

## Usage

After installation, you can go to the WireGuard Easy URL, as defined in `wg_easy_hostname` and `wg_easy_path_prefix`.

You can authenticate with the password set in `wg_easy_environment_variables_additional_variable_password`.

You can then create various Clients and import the configuration for them onto your devices - either by downloading a file or by scanning a QR code.


## Recommended other services

- [AdGuard Home](adguard-home.md) - A network-wide DNS software for blocking ads & tracking
