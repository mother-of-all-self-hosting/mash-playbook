# AdGuard Home

[AdGuard Home](https://adguard.com/en/adguard-home/overview.html/) is a network-wide DNS software for blocking ads & tracking.

**Warning**: running a public DNS server is not advisable. You'd better install AdGuard Home in a trusted local network, or adjust its network interfaces and port exposure (via the variables in the [Networking](#networking) configuration section below) so that you don't expose your DNS server publicly to the whole world. If you're exposing your DNS server publicly, consider restricting who can use it by adjusting the **Allowed clients** setting in the **Access settings** section of **Settings** -> **DNS settings**.


## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# adguard-home                                                         #
#                                                                      #
########################################################################

adguard_home_enabled: true

adguard_home_hostname: mash.example.com

# Hosting under a subpath sort of works, but is not ideal
# (see the URL section below for details).
# Consider using a dedicated hostname and removing the line below.
adguard_home_path_prefix: /adguard-home

########################################################################
#                                                                      #
# /adguard-home                                                        #
#                                                                      #
########################################################################
```

### URL

In the example configuration above, we configure the service to be hosted at `https://mash.example.com/adguard-home`.

You can remove the `adguard_home_path_prefix` variable definition, to make it default to `/`, so that the service is served at `https://mash.example.com/`.

When **hosting under a subpath**, you may hit [this bug](https://github.com/AdguardTeam/AdGuardHome/issues/5478), which causes these **annoyances**:

- upon initial usage, you will be redirected to `/install.html` and would need to manually adjust this URL to something like `/adguard-home/install.html` (depending on your `adguard_home_path_prefix`). After the installation wizard completes, you'd be redirected to `/index.html` incorrectly as well.

- every time you hit the homepage and you're not logged in, you will be redirected to `/login.html` and would need to manually adjust this URL to something like `/adguard-home/login.html` (depending on your `adguard_home_path_prefix`)


### Networking

By default, the following ports will be exposed by the container on **all network interfaces**:

- `53` over **TCP**, controlled by `adguard_home_container_dns_tcp_bind_port` - used for DNS over TCP
- `53` over **UDP**, controlled by `adguard_home_container_dns_udp_bind_port` - used for DNS over UDP

Docker automatically opens these ports in the server's firewall, so you **likely don't need to do anything**. If you use another firewall in front of the server, you may need to adjust it.

To expose these ports only on **some** network interfaces, you can use additional configuration like this:

```yaml
# Expose only on 192.168.1.15
adguard_home_container_dns_tcp_bind_port: '192.168.1.15:53'
adguard_home_container_dns_udp_bind_port: '192.168.1.15:53'
```

## Usage

After installation, you can go to the AdGuard Home URL, as defined in `adguard_home_hostname` and `adguard_home_path_prefix`.

As mentioned in the [URL](#url) section above, you may hit some annoyances when hosting under a subpath.

The first time you visit the AdGuard Home pages, you'll go through a setup wizard **make sure to set the HTTP port to `3000`**. This is the in-container port that our Traefik setup expects and uses for serving the install wizard to begin with. If you go with the default (`80`), the web UI will stop working after the installation wizard completes.
