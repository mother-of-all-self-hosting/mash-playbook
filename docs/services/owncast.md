# Owncast

[Owncast](https://owncast.online/) is a free and open source live video and web chat server for use with existing popular broadcasting software.


## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# owncast                                                            #
#                                                                      #
########################################################################

owncast_enabled: true

owncast_hostname: live.example.com
owncast_path_prefix: /owncast
########################################################################
#                                                                      #
# /owncast                                                           #
#                                                                      #
########################################################################
```

### URL

In the example configuration above, we configure the service to be hosted at `https://mash.example.com/owncast`.

You can remove the `owncast_path_prefix` variable definition, to make it default to `/`, so that the service is served at `https://mash.example.com/`.

### Authentication

You can log in with **any** of the Basic Auth credentials defined in `owncast_basicauth_credentials`. owncast is **not a multi-user system**, so whichever user you authenticate with, you'd ultimately end up looking at the same shared system.

Authentication is **done at the reverse-proxy level** (Traefik), so upon logging in, owncast will show you scary warnings about **no GUI password being set**. You should ignore these warnings.

You can hide the warning permanently by going to **Actions** -> **Advanced** -> **GUI** section -> checking the **Insecure Admin Access** checkbox.

### Networking

By default, the following ports will be exposed by the container on **all network interfaces**:

- `22000` over **TCP**, controlled by `owncast_container_sync_tcp_bind_port` - used for TCP based sync protocol traffic
- `22000` over **UDP**, controlled by `owncast_container_sync_udp_bind_port` - used for QUIC based sync protocol traffic
- `21027` over **UDP**, controlled by `owncast_container_local_discovery_udp_bind_port` - used for discovery broadcasts on IPv4 and multicasts on IPv6

Docker automatically opens these ports in the server's firewall, so you **likely don't need to do anything**. If you use another firewall in front of the server, you may need to adjust it.

To learn more, see the upstream [Firewall documentation](https://docs.owncast.net/users/firewall.html).

### Configuration & Data

The owncast configuration (stored in `owncast_config_path` on the host) is mounted to the `/var/owncast` directory in the container.
By default, owncast will create a default `Sync` directory underneath. We advise that you **don't use this** `Sync` directory and use the data directory (discussed below).

As mentioned above, the **data directory** (stored in `owncast_data_path` on the host) is mounted to the `/data` directory in the container. We advise that you put data files underneath `/data` when you start using owncast.

If you'd like to **mount additional directories** into the container, look into the `owncast_container_additional_volumes` variable part of the [`ansible-role-owncast` role](https://github.com/mother-of-all-self-hosting/ansible-role-owncast)'s [`defaults/main.yml` file](https://github.com/mother-of-all-self-hosting/ansible-role-owncast/blob/main/defaults/main.yml).


## Usage

After installation, you can go to the owncast URL, as defined in `owncast_hostname` and `owncast_path_prefix`.

As mentioned in [Configuration & Data](#configuration--data) above, you should:

- get rid of the `Default Folder` directory that was automatically created in `/var/owncast/Sync`
- change the default data directory, by going to **Actions** -> **Settings** -> **General** tab -> **Edit Folder Defaults** and changing **Folder Path** to `/data`

As mentioned in [Authentication](#authentication) above, you'd probably wish to permanently disable the "no GUI password set" security warnings as described there.
