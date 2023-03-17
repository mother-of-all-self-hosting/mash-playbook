# PeerTube

[PeerTube](https://joinpeertube.org/) is a tool for sharing online videos developed by [Framasoft](https://framasoft.org/), a french non-profit.


## Dependencies

This service requires the following other services:

- a [Postgres](postgres.md) database
- a [Redis](redis.md) data-store
- a [Traefik](traefik.md) reverse-proxy server


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# peertube                                                             #
#                                                                      #
########################################################################

peertube_enabled: true

peertube_hostname: peertube.example.com

# PeerTube does not support being hosted at a subpath right now,
# so using the peertube_path_prefix variable is not possible.

# A PeerTube secret.
# You can put any string here, but generating a strong one is preferred (e.g. `pwgen -s 64 1`).
peertube_config_secret: ''

# An email address to be associated with the `root` PeerTube administrator account.
peertube_config_admin_email: ''

# The initial password that the `root` PeerTube administrator account will be created with.
# You can put any string here, but generating a strong one is preferred (e.g. `pwgen -s 64 1`).
peertube_config_root_user_initial_password: ''

# Uncomment and adjust this after completing the initial installation.
# Find the `traefik` network's IP address range by running the following command on the server:
# `docker network inspect traefik -f "{{ (index .IPAM.Config 0).Subnet }}"`
# Then, replace the example IP range below, and re-run the playbook.
# peertube_trusted_proxies_values_custom: ["172.21.0.0/16"]

########################################################################
#                                                                      #
# /peertube                                                            #
#                                                                      #
########################################################################
```

In the example configuration above, we configure the service to be hosted at `https://peertube.example.com`.

Hosting PeerTube under a subpath (by configuring the `peertube_path_prefix` variable) does not seem to be possible right now, due to PeerTube limitations.


## Usage

After [installation](../installing.md), you should be able to access your new PeerTube instance at the URL you've chosen (depending on `peertube_hostname` and `peertube_path_prefix` values set in `vars.yml`).

You should then be able to log in with:

- username: `root`
- password: the password you've set in `peertube_config_root_user_initial_password` in `vars.yml`

## Adjusting the trusted reverse-proxy networks

If you go to **Administration** -> **System** -> **Debug** (`/admin/system/debug`), you'll notice that PeerTube reports some local IP instead of your own IP address.

To fix this, you need to adjust the "trusted proxies" configuration setting.

The default installation uses a Traefik reverse-proxy, so we suggest that you make PeerTube trust the whole `traefik` container network.

To do this:

- SSH into the machine
- run this command to find the network range: `docker network inspect traefik -f "{{ (index .IPAM.Config 0).Subnet }}"` (e.g. `172.19.0.0/16`)
- adjust your `vars.yml` configuration to contain a variable like this: `peertube_trusted_proxies_values_custom: ["172.19.0.0/16"]`

Then, re-install the PeerTube component via the playbook by running: `just install-service peertube`

You should then see the **Debug** page report your actual IP address.
