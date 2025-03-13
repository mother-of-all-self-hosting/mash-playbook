# Syncthing

[Syncthing](https://syncthing.net/) is a **continuous file synchronization** program which synchronizes files between two or more computers in real time, safely protected from prying eyes.


## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# syncthing                                                            #
#                                                                      #
########################################################################

syncthing_enabled: true

syncthing_hostname: mash.example.com
syncthing_path_prefix: /syncthing

# By default, the data directory is created at (`/mash/syncthing/data`), as defined below.
# If you'd like to put it elsewhere on the host, uncomment and edit the line below.
#
# Regardless of the location of the data directory on the host,
# it will be mounted into the Syncthing container at `/data`.
# syncthing_data_path: "{{ syncthing_base_path }}/data"

# To mount additional data directories, use `syncthing_container_additional_volumes`.

# Secure with HTTP Basic Auth (at the Traefik level)
syncthing_basicauth_enabled: true

# Syncthing is NOT a multi-user system.
# Whichever user you authenticate with later, you would get to the same shared system.
syncthing_basicauth_credentials:
  - username: someone
    password: secret-password
  - username: another
    password: more-secret-password

########################################################################
#                                                                      #
# /syncthing                                                           #
#                                                                      #
########################################################################
```

### URL

In the example configuration above, we configure the service to be hosted at `https://mash.example.com/syncthing`.

You can remove the `syncthing_path_prefix` variable definition, to make it default to `/`, so that the service is served at `https://mash.example.com/`.

### Authentication

You can log in with **any** of the Basic Auth credentials defined in `syncthing_basicauth_credentials`. Syncthing is **not a multi-user system**, so whichever user you authenticate with, you'd ultimately end up looking at the same shared system.

Authentication is **done at the reverse-proxy level** (Traefik), so upon logging in, Syncthing will show you scary warnings about **no GUI password being set**. You should ignore these warnings.

You can hide the warning permanently by going to **Actions** -> **Advanced** -> **GUI** section -> checking the **Insecure Admin Access** checkbox.

### Networking

By default, the following ports will be exposed by the container on **all network interfaces**:

- `22000` over **TCP**, controlled by `syncthing_container_sync_tcp_bind_port` and `syncthing_container_sync_tcp_port` — used for TCP based sync protocol traffic
- `22000` over **UDP**, controlled by `syncthing_container_sync_udp_bind_port` and `syncthing_container_sync_udp_port` — used for QUIC based sync protocol traffic
- `21027` over **UDP**, controlled by `syncthing_container_local_discovery_udp_bind_port` — used for discovery broadcasts on IPv4 and multicasts on IPv6

Docker automatically opens these ports in the server's firewall, so you **likely don't need to do anything**. If you use another firewall in front of the server, you may need to adjust it.

If you have multiple devices on the same LAN, you may wish to assign a unique port to each one as recommended in the [Local network setup section on ArchWiki](https://wiki.archlinux.org/title/Syncthing#Local_network_setup).

As the upstream [Firewall documentation](https://docs.syncthing.net/users/firewall.html) says:

> The external forwarded ports and the internal destination ports have to be the same (e.g. 22000/TCP).

Because of this, the Syncthing Ansible role makes the actually exposed ports (`syncthing_container_sync_*_bind_port` variables) the same as the ports that the Syncthing program in the container actually listens on (`syncthing_container_sync_tcp_port` or `syncthing_container_sync_udp_port`). That is to say, **the `_bind_port` variables are automatically adjusted** based on the values of `syncthing_container_sync_tcp_port` and `syncthing_container_sync_udp_port`.

However, changing `syncthing_container_sync_tcp_port` or `syncthing_container_sync_udp_port` in Ansible does not change the Syncthing configuration and the port Syncthing decides to listen, but merely tells the Ansible role which ports you'd like to use, so it can wire things correctly.

**To effectively change the Syncthing ports** being used:

1. Adjust `syncthing_container_sync_tcp_port` and `syncthing_container_sync_udp_port` in your `vars.yml`
2. Re-install the Syncthing service by re-running the Ansible playbook
3. Log in to the Syncthing Web UI (see [Usage](#usage))
4. Go to **Settings** -> **Connections** and put something like this in the **Sync Protocol Listen Addresses** configuration (inspired by the [Listen Addresses documentation](https://docs.syncthing.net/v1.27.0/users/config#listen-addresses)): `tcp://0.0.0.0:TCP_PORT_HERE, quic://0.0.0.0:UDP_PORT_HERE, dynamic+https://relays.syncthing.net/endpoint` (adjust `TCP_PORT_HERE` and `UDP_PORT_HERE` with the port numbers you've chosen for `syncthing_container_sync_tcp_port` and `syncthing_container_sync_udp_port`)


### Configuration & Data

The Syncthing configuration (stored in `syncthing_config_path` on the host) is mounted to the `/var/syncthing` directory in the container.
By default, Syncthing will create a default `Sync` directory underneath. We advise that you **don't use this** `Sync` directory and use the data directory (discussed below).

As mentioned above, the **data directory** (stored in `syncthing_data_path` on the host) is mounted to the `/data` directory in the container. We advise that you put data files underneath `/data` when you start using Syncthing.

If you'd like to **mount additional directories** into the container, look into the `syncthing_container_additional_volumes` variable part of the [`ansible-role-syncthing` role](https://github.com/mother-of-all-self-hosting/ansible-role-syncthing)'s [`defaults/main.yml` file](https://github.com/mother-of-all-self-hosting/ansible-role-syncthing/blob/main/defaults/main.yml).


## Usage

After installation, you can go to the Syncthing URL, as defined in `syncthing_hostname` and `syncthing_path_prefix`.

As mentioned in [Configuration & Data](#configuration--data) above, you should:

- get rid of the `Default Folder` directory that was automatically created in `/var/syncthing/Sync`
- change the default data directory, by going to **Actions** -> **Settings** -> **General** tab -> **Edit Folder Defaults** and changing **Folder Path** to `/data`

As mentioned in [Authentication](#authentication) above, you'd probably wish to permanently disable the "no GUI password set" security warnings as described there.
