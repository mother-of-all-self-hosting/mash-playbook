# WireGuard Easy

[WireGuard Easy](https://github.com/wg-easy/wg-easy) is the easiest way to run [WireGuard](https://www.wireguard.com/) VPN + Web-based Admin UI.

Another more powerful alternative for a self-hosted WireGuard VPN server is [Firezone](firezone.md). WireGuard Easy is easier, lighter and more compatible with various ARM devices.


## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server
- a modern Linux kernel which supports WireGuard
- `devture_systemd_docker_base_ipv6_enabled: true` if you'd like IPv6 support


## Configuration

To enable this service, add the following configuration to your `vars.yml` file:

```yaml
########################################################################
#                                                                      #
# wg-easy                                                              #
#                                                                      #
########################################################################

wg_easy_enabled: true

wg_easy_hostname: wg-easy.example.com

# The username for the initial setup.
# It needs to be strong enough (at least 8 characters).
# Subsequent changes will not have any effect.
wg_easy_environment_variables_additional_variable_init_username: ''

# The password for the initial setup.
# Generating a strong password (e.g. `pwgen -s 64 1`) is recommended.
# Subsequent changes will not have any effect.
wg_easy_environment_variables_additional_variable_init_password: ''

########################################################################
#                                                                      #
# /wg-easy                                                             #
#                                                                      #
########################################################################
```

> [!WARNING]
> There are a few other **variables that you may wish to adjust before doing the initial [unattended setup](https://github.com/wg-easy/wg-easy/blob/c133446f9ced12942d8a6d5b06388301a46b55e7/docs/content/advanced/config/unattended-setup.md)**. See the sections below for details.
> The reason it's important to do this early on, is because certain variables (`wg_easy_environment_variables_additional_variable_init_*`)
> only take effect during the initial setup phase.

Once you're all done with preparing your `vars.yml` configuration, re-run the [installation](../installing.md) process:

### Adjusting the web UI URL

In the example configuration above, we configure the service to be hosted at `https://wg-easy.example.com/`.

You can adjust the hostname of the web UI with the `wg_easy_hostname` variable.

Previously (prior to wg-easy v15), a `wg_easy_path_prefix` variable could allow you to host wg-easy at a subpath (e.g. `wg_easy_path_prefix: /wg-easy`), but this is [no longer possible](https://github.com/wg-easy/wg-easy/issues/1704#issuecomment-2705873936) and such a feature [may re-appear later](https://github.com/wg-easy/wg-easy/issues/1704#issuecomment-2706575504).

💡 WireGuard clients may optionally be pointed to a different hostname than the one used for the web UI. See [Adjusting the WireGuard endpoint](#adjusting-the-wireguard-endpoint) for details.

### Adjusting the Wireguard endpoint

By default, the WireGuard endpoint that clients are configured to connect to uses:

- the same hostname as the web UI (controlled by the `wg_easy_hostname` variable)
- the port `51820`, configured via the `wg_easy_environment_variables_additional_variable_init_port` and `wg_easy_container_wireguard_bind_port` variables

Sometimes, you may wish to use a different hostname or port for the WireGuard endpoint. You can do so with the following variables:

```yml
# Controls the public hostname of the WireGuard endpoint that will be configured during initial unattended setup.
wg_easy_environment_variables_additional_variable_init_host: wg-easy.example.com

# Controls the public port of the WireGuard endpoint that will be configured during initial unattended setup.
# Also points to the port actually used in the container (in case you've reconfigured it via the web UI).
wg_easy_environment_variables_additional_variable_init_port: 51820

# Controls the exposed (published) port of the WireGuard container.
# By default, this matches the `wg_easy_environment_variables_additional_variable_init_port` value.
wg_easy_container_wireguard_bind_port: 51820
```

> [!WARNING]
> If you need to change the hostname or port after the initial setup, you need to do so from the Admin Panel -> Config section (`/admin/config` URL path) of the web UI.

### Adjusting the default DNS servers

If you'd like to provide custom DNS servers (instead of the default ones seen below), you can do so with the following **initial unattended setup** variables:

```yml
wg_easy_environment_variables_additional_variable_init_dns: "1.1.1.1,2606:4700:4700::1111"
```

> [!WARNING]
> If you need to change the DNS servers after the initial setup, you need to do so from the Admin Panel -> Config section (`/admin/config` URL path) of the web UI.

💡 DNS configuration can also be adjusted later on, on a per-client basis, but these changes need to be made before one downloads the WireGuard configuration profile files, because they do hardcode the DNS configuration (and all lots of other configuration) inside them.

### Adjusting the IPv4/IPv6 CIDR

If you'd like to provide custom IPv4 and IPv6 CIDRs (instead of the default ones seen below), you can do so with the following **initial unattended setup** variables:

```yml
wg_easy_environment_variables_additional_variable_init_ipv4_cidr: "10.8.0.0/24"

# This looks like the documentation-reserved IPv6 CIDR value, because it is. Read why below.
wg_easy_environment_variables_additional_variable_init_ipv6_cidr: "2001:db8::/32"
```

💡 The `wg_easy_environment_variables_additional_variable_init_ipv6_cidr` value you see above is what we use by default. It represents the documentation-reserved IPv6 CIDR value, but we're not only using it for documentation purposes, but because it's a GUA-like CIDR value. See [Note about the IPv6 CIDR and IPv6 connectivity](#note-about-the-ipv6-cidr-and-ipv6-connectivity) for more details and for a recommended alternative if you can use your own GUA address.

> [!WARNING]
> If you need to change the IPv4/IPv6 CIDRs after the initial setup, you need to do so from the Admin Panel -> Interface page of the web UI, via the Change CIDR button. After changing the CIDR in wg-easy's settings, you must restart the wg-easy service for the changes to take effect.

### Adjusting your firewall

**In addition** to ports `80` and `443` exposed by the [Traefik](traefik.md) reverse-proxy, the following ports will be exposed by the WireGuard containers on **all network interfaces**:

- `51820` over **UDP**, controlled by `wg_easy_container_wireguard_bind_port` — used for [Wireguard](https://www.wireguard.com/) connections

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

The new wg-easy version (after the v15 release) does not support most of the environment variables that were supported in previous versions.
Most of the configuration happens via the web UI after installation. See [Adjusting the post-installation configuration](#adjusting-the-post-installation-configuration) for more details.

Nevertheless, if you need to inject additional environment variables, you can do so with this additional configuration:

```yaml
wg_easy_environment_variables_additional_variables: |
  INSECURE=true
```

💡 Injecting this `INSECURE` environment variable like this is pointless, since the Ansible role provides a dedicated variable for controlling it (`wg_easy_environment_variables_additional_variable_insecure`).


## Usage

After installation, you can go to the wg-easy [URL](#url).

Most users can log in with the credentials they provided before the first installation and can log in and proceed to [create WireGuard clients](#creating-wireguard-clients).

Depending on your configuration, you may need to go through a setup wizard first. Details are below.

If you have provided a username (`wg_easy_environment_variables_additional_variable_init_username`) and password (`wg_easy_environment_variables_additional_variable_init_password`) before the first installation, the unattended setup process would have created these credentials for you, so you can log in with them. Otherwise, you'll see a setup wizard and can create your own credentials.

Similarly, if you have provided a hostname (`wg_easy_hostname` and/or `wg_easy_environment_variables_additional_variable_init_host`) and port (`wg_easy_environment_variables_additional_variable_init_port`) before the first installation, the unattended setup process would have initialized the wg-easy service with these values. Otherwise, you'll see a setup wizard about this.

### Creating WireGuard clients

You can then create various Clients and import the configuration for them onto your devices — either by downloading a file or by scanning a QR code.


## Note about the IPv6 CIDR and IPv6 connectivity

> [!WARNING]
> For IPv6 to work, you need your container networks to have been created with IPv6 support (`devture_systemd_docker_base_ipv6_enabled: true`) as mentioned in the [Prerequisites](#prerequisites). If your wg-easy container network (`mash-wg-easy`) was created before you flipped this setting to `true`, you may need to stop the wg-easy service, delete the container network manually (`docker network rm mash-wg-easy`) and re-run the playbook to have it create the container network anew.

💡 The Ansible wg-easy role goes against the upstream default and uses a [Global Unicast Address (GUA)](https://www.oreilly.com/library/view/ipv6-fundamentals-a/9780134670584/ch05.html)-like CIDR value (a documentation-reserved CIDR (`2001:db8::/32`) as per [RFC 3849](https://datatracker.ietf.org/doc/html/rfc3849)) instead of a [Unique Local Address (ULA)](https://en.wikipedia.org/wiki/Unique_local_address) one, as described below.
Due to this, you should have outgoing IPv6 connectivity and it should be preferred over IPv4, as expected. **Most users can rely on our defaults and leave things as they are**, without having to do anything.

Below, we describe what upstream wg-easy does by default, why we're doing things differently and how you can improve on what we do by default (using a documentation-reserved IPv6 CIDR value).

By default, upstream wg-easy uses a [default CIDR value](https://github.com/wg-easy/wg-easy/blob/0597470f4cea239b4a572208ef01d490e2ade2d2/src/server/database/migrations/0001_classy_the_stranger.sql#L6) of `fdcc:ad94:bacf:61a4::cafe:0/112`.

Most operating systems, when dealing with a network interface with a ULA address (instead of a GUA address), will prefer IPv4 instead of IPv6 for outgoing connections.

This means that you may get a `10/10` score on the [test-ipv6.com](https://test-ipv6.com/) test, but you'll also see a warning message like this:

> [!WARNING]
> Your browser has real working IPv6 address - but is avoiding using it. We're concerned about this. [more info](https://test-ipv6.com/faq_avoids_ipv6.html)

We don't like this behavior of defaulting to IPv4 and avoiding IPv6. We believe that just like IPv6 is typically preferred over IPv4 (when **not** using a VPN), the same should happen when you are using a VPN. If your computer is avoiding IPv6 and is preferring IPv4, then you don't really have "proper IPv6" connectivity. In this day and age, most services on the internet are either IPv4-only or dual-stack (and less often IPv6 only), so a client that prefers IPv4 will pretty much always stick to IPv4 in practice.

📖 This issue is also discussed [here](https://www.reddit.com/r/WireGuard/comments/q8t9bj/wireguard_doesnt_seem_to_work_with_ipv6/) and a workaround is documented [here](https://www.reddit.com/r/ipv6/comments/ngug1e/comment/gyw1ni8/). We'll summarize these findings and propose alternatives below.

To get full IPv6 connectivity and have it be preferred on most operating systems, you'll:

- either need to fiddle with the `/etc/gai.conf` file and make your operating system prefer IPv6 even when dealing with a ULA address. This is difficult, requires manual work and is potentially impossible on certain systems (iOS)

- or you fix this globally by switching from ULA addresses to GUA addresses

To do the latter, **you need to change the IPv6 CIDR used by wg-easy** to a GUA or GUA-like one. The proposed workaround [here](https://www.reddit.com/r/ipv6/comments/ngug1e/comment/gyw1ni8/) suggests using a random real/global/public IPv6 subnet for your WireGuard clients. While these addresses will only be used inside your WireGuard for NAT purposes, using them will still break your connectivity to this subnet.

💡 The wg-easy IPv6 CIDR can be changed:

- initially (before setup), as part of the initial unattended setup via the `wg_easy_environment_variables_additional_variable_init_ipv6_cidr` variable
- subsequently, from the Admin Panel -> Interface page of the web UI, via the Change CIDR button.

We propose 2 alternatives for your IPv6 CIDR:

- (recommended) a CIDR derived from a GUA one that you own. For example, if you get `2001:555:5555:5555:/64` from your ISP for your network, you could assign something like `2001:555:5555:5555::0:cafe:0/112` for your 1st (`0`-th) wg-easy instance. If you run more wg-easy instances in your network, you could use `2001:555:5555:5555::1:cafe:0/112`, `2001:555:5555:5555::2:cafe:0/112`, etc. for them, so that they all have unique subnets.

- (not so recommended, but the default for the wg-easy Ansible role) [a GUA-like CIDR](https://en.wikipedia.org/wiki/IPv6_address#Special-purpose_addresses). We've had success using the documentation-reserved CIDR (`2001:db8::/32`) as per [RFC 3849](https://datatracker.ietf.org/doc/html/rfc3849). You can pick a random CIDR value from this range, like `2001:db8:100:5000::0:cafe:0/112` and use it for your 1st (`0`-th) wg-easy instance. If you run more wg-easy instances in your network, you could use `2001:db8:100:5000::1:cafe:0/112`, `2001:db8:100:5000::2:cafe:0/112`, etc. for them, so that they all have unique subnets. Using documentation-reserved addresses for non-documentation-purposes is not great, but we've confirmed that it works well in practice. These addresses are only behind your NAT and never used for real addressing outside of it, so there shouldn't be a problem.

Regardless of what you choose, your WireGuard clients will get a network interface which uses a GUA or GUA-like IPv6 address instead of a ULA IPv6 address. With that, IPv6 connectivity will be preferred over IPv4 even without custom changes to `/etc/gai.conf`.

To change the IPv6 CIDR, refer to the [Adjusting the IPv4/IPv6 CIDR](#adjusting-the-ipv4ipv6-cidr) section above.


## Recommended other services

- [AdGuard Home](adguard-home.md) — A network-wide DNS software for blocking ads & tracking
