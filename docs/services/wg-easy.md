# WireGuard Easy

[WireGuard Easy](https://github.com/wg-easy/wg-easy) is the easiest way to run [WireGuard](https://www.wireguard.com/) VPN + Web-based Admin UI.

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

- `51820` over **UDP**, controlled by `wg_easy_environment_variables_additional_variable_wg_port` and `wg_easy_container_wireguard_bind_port` — used for [Wireguard](https://www.wireguard.com/) connections

Docker automatically opens these ports in the server's firewall, so you **likely don't need to do anything**. If you use another firewall in front of the server, you may need to adjust it.

### Adjusting the host's iptables configuration

If you're running `iptables`/`ip6tables` on the host with a custom config (which whitelists some traffic and denies everything else), you may find that WireGuard clients cannot reach certain ports on server where wg-easy runs via its LAN IP address (e.g. `192.168.1.50`).

You may wish to adjust your iptables configuration (typically `/etc/iptables/iptables.rules`) like this:

```iptables
# ... Additional configuration ...

# Allow all private IPv4 ranges (RFC1918 private addresses) to access us via SSH.
#
# This allows wg-easy WireGuard clients which try to speak to us via our LAN IP to be able to reach us.
# They "exit" through mash-wg-easy's container subnet (e.g. 172.18.0.1).
-A INPUT -m tcp -p tcp --dport 22 -s 10.0.0.0/8 -j ACCEPT
-A INPUT -m tcp -p tcp --dport 22 -s 172.16.0.0/12 -j ACCEPT
-A INPUT -m tcp -p tcp --dport 22 -s 192.168.0.0/16 -j ACCEPT

# Allow private IPv4 ranges to access us via HTTP.
# This is like the above private IPv4 range rules for SSH.
-A INPUT -m tcp -p tcp --dport 80 -s 10.0.0.0/8 -j ACCEPT
-A INPUT -m tcp -p tcp --dport 80 -s 172.16.0.0/12 -j ACCEPT
-A INPUT -m tcp -p tcp --dport 80 -s 192.168.0.0/16 -j ACCEPT

# ... Additional configuration ...
```

or for ip6tables (typically `/etc/iptables/ip6tables.rules`) like this:

```iptables
# ... Additional configuration ...

# Allow all private IPv6 ranges to access us via SSH.
#
# This allows wg-easy WireGuard clients which try to speak to us via our LAN IP to be able to reach us.
# They "exit" through mash-wg-easy's container subnet (e.g. 172.18.0.1).
# Unique Local Addresses (ULA)
-A INPUT -p tcp --dport 22 -s fc00::/7 -j ACCEPT
# Link-local addresses
-A INPUT -p tcp --dport 22 -s fe80::/10 -j ACCEPT

# Allow private IPv6 ranges to access us via HTTP.
# This is like the above private IPv6 range rules for SSH.
-A INPUT -m tcp -p tcp --dport 80 -s fc00::/7 -j ACCEPT
-A INPUT -m tcp -p tcp --dport 80 -s fe80::/10 -j ACCEPT

# ... Additional configuration ...
```

After doing so, you'll wish to restart `iptables`/`ip6tables`. Restarting iptables typically necessitates restarting Docker (`docker.service`) as well.

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

You can then create various Clients and import the configuration for them onto your devices — either by downloading a file or by scanning a QR code.

## Recommended other services

- [AdGuard Home](adguard-home.md) — A network-wide DNS software for blocking ads & tracking
