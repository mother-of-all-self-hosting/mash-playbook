<!--
SPDX-FileCopyrightText: 2020 - 2024 MDAD project contributors
SPDX-FileCopyrightText: 2020 - 2025 Slavi Pantaleev
SPDX-FileCopyrightText: 2020 Aaron Raimist
SPDX-FileCopyrightText: 2020 Chris van Dijk
SPDX-FileCopyrightText: 2020 Dominik Zajac
SPDX-FileCopyrightText: 2020 Mickaël Cornière
SPDX-FileCopyrightText: 2022 François Darveau
SPDX-FileCopyrightText: 2022 Julian Foad
SPDX-FileCopyrightText: 2022 Warren Bailey
SPDX-FileCopyrightText: 2023 Antonis Christofides
SPDX-FileCopyrightText: 2023 Felix Stupp
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# BIND

The playbook can install and configure the [BIND](https://www.isc.org/bind/) DNS server for you.

See the project's [documentation](https://www.isc.org/bind/) to learn what BIND does and why it might be useful to you.

## Dependencies

This service requires no other services.

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file:

```yaml
########################################################################
#                                                                      #
# bind                                                                 #
#                                                                      #
########################################################################

bind_enabled: true

########################################################################
#                                                                      #
# /bind                                                                #
#                                                                      #
########################################################################
```

### Configuring ACLs

Various BIND features (like [Configuring recursion](#configuring-recursion) and others) can be configured to allow or deny requests depending on which networks they come from. This is done using Access Control Lists (ACLs).

You can define some ACLs by setting the `bind_config_acl_custom` variable in your `vars.yml` file like this:

```yaml
bind_config_acl_custom:
  private:
    # IPv4 private ranges (RFC 1918)
    - 10.0.0.0/8
    - 172.16.0.0/12
    - 192.168.0.0/16
    # IPv4 link-local
    - 169.254.0.0/16
    # IPv6 loopback
    - ::1/128
    # IPv6 link-local
    - fe80::/10
    # IPv6 Unique Local Addresses (RFC 4193)
    - fc00::/7
  home_1:
    - 1.2.3.4/32
  home_2:
    - 5.6.7.8/24
  # trusted is an ACL that's composed of other ACLs
  trusted:
    - home_1
    - home_2
    # localnets is a built-in ACL
    - localnets
    - private
```

💡 These are merely ACL definitions and don't do anything on their own. They need to be referenced in other configuration blocks - see an example in [Configuring recursion](#configuring-recursion).

### Configuring recursion

By default, BIND is configured to recursively resolve queries, but the default Access Control List that can do this is `none`, so it's effectively disabled.

We recommend **either** disabling recursion explicitly (`bind_config_options_recursion: false`) **or** allowing recursion for clients on specific networks.

To do the latter, you'll need to define some ACLs (see [Configuring ACLs](#configuring-acls)) and then adjust the `allow-recursion` option in the `options` block by adding the following configuration your `vars.yml` file:

```yaml
bind_config_options_allow_recursion: [trusted]
```

💡 If you're running a large server, you may also be interested in tweaking `bind_config_options_recursive_clients`, so you can serve more clients (though the default of `1000` is not too bad). If you're [enabling DNS-over-TLS (DoT) and/or DNS-over-HTTPS (DoH)](#configuring-dns-over-tls-dot-and-dns-over-https-doh), you may similarly wish to increase `bind_config_options_tcp_clients` (defaults to `150`).

### Configuring IPv6 connectivity

If your server has no IPv6 connectivity, trying to talk to other DNS servers via IPv6 may lead to slow responses (due to having to fall back to IPv4). This slowness propagates to clients querying your DNS server and may result in timeouts.

If your server does not have IPv6 connectivity, it's recommended to disable trying to connect over IPv6 by adding the following configuration to your `vars.yml` file:

```yaml
bind_ipv6_connectivity_enabled: false
```

💡 This only affects whether BIND will try to connect to other DNS servers over IPv6. It does not affect whether clients will be receive `AAAA` records from your DNS server (they still will, even if this is disabled).

### Configuring network exposure

By default, the BIND server only runs inside its container network and is not exposed to the internet.

To expose it, you'll have to adjust various `_bind_port` variables. Here are some examples for configuration you may wish to add to your `vars.yml` file:

```yaml
# Expose DNS on all interfaces
bind_container_dns_udp_bind_port: "53"
bind_container_dns_tcp_bind_port: "53"

# Expose DNS-over-TLS (DoT) on all interfaces
# Only makes sense if you actually configure (enable) DoT
bind_container_dot_tcp_bind_port: "853"

# Expose DNS-over-HTTPS (DoH) on all interfaces
# Only makes sense if you actually configure (enable) DoH
bind_container_doh_tcp_bind_port: "443"
```

### Configuring DNS-over-TLS (DoT) and DNS-over-HTTPS (DoH)

Configuring [DNS-over-TLS (DoT)](https://en.wikipedia.org/wiki/DNS_over_TLS) and [DNS-over-HTTPS (DoH)](https://en.wikipedia.org/wiki/DNS_over_HTTPS) **requires an SSL certificate**.

If you're terminating SSL outside of BIND (e.g. using a reverse proxy), you may enable the plain-HTTP listener for BIND. See the `bind_config_options_http_*` variables and `bind_container_http_tcp_bind_port`.

To make BIND terminate SSL, the SSL certificate must be obtained separately, then mounted into the container, referenced in a `tls` configuration block and then you can enable the DoT and/or DoH listeners.

You can both obtain an SSL certificate for a given domain (e.g. `ns.example.com`) from [Let's Encrypt](https://letsencrypt.org/) and renew it using [certbot](https://certbot.eff.org/). Setting up scripts to renew the certificate automatically is recommended. You can use the [Auxiliary](../auxiliary.md) service to configure scripts, systemd services, timers, etc. Unfortunately, we have no pre-configured configuration for you.

Once you have an SSL certificate and the directory tree is readable by `bind_uid`/`bind_gid` (`uid=53`/`gid=53`), you can configure DoT and DoH by adding the following configuration to your `vars.yml` file:

```yaml
# Mount the SSL data directory into the container
bind_container_additional_volumes_custom:
  - type: bind
    src: /path/to/your/ssl-data
    dst: /ssl-data
    options: readonly

# Create a TLS configuration block
bind_config_additional_configuration: |
  tls ns-tls {
      cert-file "/ssl-data/live/ns.example.com/fullchain.pem";
      key-file "/ssl-data/live/ns.example.com/privkey.pem";
  };

# Enable DoT
bind_config_options_dot_listen_on_enabled: true
bind_config_options_dot_listen_on_tls_name: "ns-tls"

# Expose DoT on all interfaces
bind_container_dot_tcp_bind_port: "853"

# Enable DoH
bind_config_options_doh_listen_on_enabled: true
bind_config_options_doh_listen_on_tls_name: "ns-tls"

# Expose DoH on all interfaces
bind_container_doh_tcp_bind_port: "443"

# Increase the number of clients that can connect to the server, if necessary.
# bind_config_options_tcp_clients: 2000
```

💡 To verify that DNS-over-TLS (DoT) is working, you can use `dig` like this: `dig @1.2.3.4 example.com +tls`.

💡 To verify that DNS-over-HTTPS (DoH) is working, you can use `dig` like this: `dig @1.2.3.4 example.com +https`.

### Configuring Discovery of Designated Resolvers (DDR)

If you have [configured DNS-over-TLS (DoT) or DNS-over-HTTPS (DoH)](#configuring-dns-over-tls-dot-and-dns-over-https-doh), you can make it possible for clients to discover support for these encrypted endpoints by advertising it via [Discovery of Designated Resolvers (DDR) - RFC 9462](https://www.rfc-editor.org/rfc/rfc9462.html). This way, certain clients can auto-upgrade to using an encrypted connection to your DNS server.

To do so, you'll need to make your server authoritative for a special `resolver.arpa` zone and add some `SVCB` records to it.

You can create the zone definition either as described in [Managing zones](#managing-zones), like this:

```yaml
bind_config_zones_custom:
  resolver.arpa:
    type: primary
    file: "/var/lib/bind/resolver.arpa.zone"
    _additional_configuration: |
      allow-update { none; };
      allow-query { trusted; };
      notify no;
```

The zone file (`/mash/bind/data/resolver.arpa.zone` on the host; `/var/lib/bind/resolver.arpa.zone` inside the container) could be created using the [Auxiliary](../auxiliary.md) service or another way. It needs to look something like this:

```
$TTL 86400
@       IN      SOA     ns.example.com. hostmaster.example.com. (
                        2025111101 ; Serial (YYYYMMDDNN)
                        28800      ; Refresh (8 hours)
                        14400      ; Retry (4 hours)
                        3600000    ; Expire (1000 hours)
                        86400 )    ; Minimum (1 day)

        IN      NS      ns.example.com.

; DDR (Discovery of Designated Resolvers) - RFC 9462
; SVCB records for DoH and DoT discovery

; Priority 1: DNS-over-HTTPS (DoH)
_dns    IN      SVCB    1 ns.example.com. alpn="h2" port="443" ipv4hint="1.2.3.4" dohpath="/dns-query{?dns}"

; Priority 2: DNS-over-TLS (DoT)
_dns    IN      SVCB    2 ns.example.com. alpn="dot" port="853" ipv4hint="1.2.3.4"
```

💡 If you have an IPv6 address for your DNS server, feel free to also publish an `ipv6hint`.

💡 To verify that DDR is working, you can use `dig` like this: `dig @1.2.3.4 _dns.resolver.arpa SVCB +short`. Expect output like this:

```
1 ns.example.com. alpn="h2" port=443 ipv4hint=1.2.3.4 key7="/dns-query{?dns}"
2 ns.example.com. alpn="dot" port=853 ipv4hint=1.2.3.4
```

### Injecting additional BIND `options`

The Ansible role supports some variables (`bind_config_options_*`) for configuring settings in the BIND [`options` block](https://bind9.readthedocs.io/en/stable/reference.html#options-block-grammar).

If you need to configure something else in the `options` block for which there's no dedicated variable, you can use the `bind_config_options_additional_configuration` variable. Example:

```yaml
bind_config_options_additional_configuration: |
  dnstap {
    auth;
    client response;
    resolver query;
  };
```

### Injecting additional BIND configuration

The Ansible role supports some variables (`bind_config_*`) for configuring various settings in the BIND configuration file like:

- [`options` block](https://bind9.readthedocs.io/en/stable/reference.html#options-block-grammar) variables - see [Injecting additional BIND `options`](#injecting-additional-bind-options)
- [`acl` block](https://bind9.readthedocs.io/en/stable/reference.html#acl-block-grammar) variables - see [Configuring ACLs](#configuring-acls)
- [`zone` block](https://bind9.readthedocs.io/en/stable/reference.html#zone-block-grammar) variables - see [Managing zones](#managing-zones)
- etc.

If you need to configure something else in the configuration file for which there's no dedicated variable, you can use the `bind_config_additional_configuration` variable. Example:

```yaml
bind_config_additional_configuration: |
  include "/var/lib/bind/custom.conf";

  tls ns-tls {
      cert-file "/ssl-data/live/ns.example.com/fullchain.pem";
      key-file "/ssl-data/live/ns.example.com/privkey.pem";
  };
```

### Managing zones

You can manage zone definitions using the `bind_config_zone_*` variables.

Here's an example configuration you may add to your `vars.yml` file:

```yaml
bind_config_zone_custom:
  example.com:
    type: primary
    file: "/var/lib/bind/example.com.zone"
    _additional_configuration: |
      allow-update { none; };
      allow-query { trusted; };
      notify no;
  another-example.com:
    type: secondary
    file: "/var/lib/bind/another-example.com.zone"
    _additional_configuration: |
      primaries { 1.2.3.4; }
```

💡 BIND's data directory on the host (`/mash/bind/data`) is mounted into the container at `/var/lib/bind`.

💡 You can manage your zone files using Ansible, by making use of the [Auxiliary](../auxiliary.md) service.

**Alternatively**, if you prefer to manage your zone files manually (without Ansible), you may also drop them into the data directory (`/mash/bind/data/`) and then tell the BIND server to load them from there (by using an [`include` directive](https://bind9.readthedocs.io/en/stable/reference.html#include-grammar)) like this:

```yaml
bind_config_zones_additional_configuration: |
  include "/var/lib/bind/zones.conf";
```

## Installation

Once you've configured the service, run the [installing](../installing.md) command for the host.

## Usage

After running the command for installation, if you have [configured network exposure](#configuring-network-exposure), you should be able to reach your DNS server.

You can test using `nslookup` or `dig`. At the bare minimum, you likely would have exposed port `53` for DNS queries, so these commands should work:

- `dig @1.2.3.4 example.com +udp`
- `dig @1.2.3.4 example.com +tcp`

## Managing via rndc

The Ansible playbook auto-configures the BIND Ansible role's secrets, so that an `rndc` tool wrapper is installed in `/mash/bind/bin/rndc`. With that, you can easily invoke `rndc` commands like:

- `/mash/bind/bin/rndc reload`
- `/mash/bind/bin/rndc status`
- etc.
