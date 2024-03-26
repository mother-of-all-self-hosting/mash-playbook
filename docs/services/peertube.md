# PeerTube

[PeerTube](https://joinpeertube.org/) is a tool for sharing online videos developed by [Framasoft](https://framasoft.org/), a french non-profit.


## Dependencies

This service requires the following other services:

- a [Postgres](postgres.md) database
- a [KeyDB](keydb.md) data-store, installation details [below](#keydb)
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

# KeyDB configuration, as described below

########################################################################
#                                                                      #
# /peertube                                                            #
#                                                                      #
########################################################################
```

In the example configuration above, we configure the service to be hosted at `https://peertube.example.com`.

Hosting PeerTube under a subpath (by configuring the `peertube_path_prefix` variable) does not seem to be possible right now, due to PeerTube limitations.

### KeyDB

As described on the [KeyDB](keydb.md) documentation page, if you're hosting additional services which require KeyDB on the same server, you'd better go for installing a separate KeyDB instance for each service. See [Creating a KeyDB instance dedicated to PeerTube](#creating-a-keydb-instance-dedicated-to-peertube).

If you're only running PeerTube on this server and don't need to use KeyDB for anything else, you can [use a single KeyDB instance](#using-the-shared-keydb-instance-for-peertube).

#### Using the shared KeyDB instance for PeerTube

To install a single (non-dedicated) KeyDB instance (`mash-keydb`) and hook PeerTube to it, add the following **additional** configuration:

```yaml
########################################################################
#                                                                      #
# keydb                                                                #
#                                                                      #
########################################################################

keydb_enabled: true

########################################################################
#                                                                      #
# /keydb                                                               #
#                                                                      #
########################################################################


########################################################################
#                                                                      #
# peertube                                                             #
#                                                                      #
########################################################################

# Base configuration as shown above

# Point PeerTube to the shared KeyDB instance
peertube_config_redis_hostname: "{{ keydb_identifier }}"

# Make sure the PeerTube service (mash-peertube.service) starts after the shared KeyDB service (mash-keydb.service)
peertube_systemd_required_services_list_custom:
  - "{{ keydb_identifier }}.service"

# Make sure the PeerTube container is connected to the container network of the shared KeyDB service (mash-keydb)
peertube_container_additional_networks_custom:
  - "{{ keydb_identifier }}"

########################################################################
#                                                                      #
# /peertube                                                            #
#                                                                      #
########################################################################
```

This will create a `mash-keydb` KeyDB instance on this host.

This is only recommended if you won't be installing other services which require KeyDB. Alternatively, go for [Creating a KeyDB instance dedicated to PeerTube](#creating-a-keydb-instance-dedicated-to-peertube).


#### Creating a KeyDB instance dedicated to PeerTube

The following instructions are based on the [Running multiple instances of the same service on the same host](../running-multiple-instances.md) documentation.

Adjust your `inventory/hosts` file as described in [Re-do your inventory to add supplementary hosts](../running-multiple-instances.md#re-do-your-inventory-to-add-supplementary-hosts), adding a new supplementary host (e.g. if `peertube.example.com` is your main one, create `peertube.example.com-deps`).

Then, create a new `vars.yml` file for the

`inventory/host_vars/peertube.example.com-deps/vars.yml`:

```yaml
---

########################################################################
#                                                                      #
# Playbook                                                             #
#                                                                      #
########################################################################

# Put a strong secret below, generated with `pwgen -s 64 1` or in another way
# Various other secrets will be derived from this secret automatically.
mash_playbook_generic_secret_key: ''

# Override service names and directory path prefixes
mash_playbook_service_identifier_prefix: 'mash-peertube-'
mash_playbook_service_base_directory_name_prefix: 'peertube-'

########################################################################
#                                                                      #
# /Playbook                                                            #
#                                                                      #
########################################################################


########################################################################
#                                                                      #
# keydb                                                                #
#                                                                      #
########################################################################

keydb_enabled: true

########################################################################
#                                                                      #
# /keydb                                                               #
#                                                                      #
########################################################################
```

This will create a `mash-peertube-keydb` instance on this host with its data in `/mash/peertube-keydb`.

Then, adjust your main inventory host's variables file (`inventory/host_vars/peertube.example.com/vars.yml`) like this:

```yaml
########################################################################
#                                                                      #
# peertube                                                             #
#                                                                      #
########################################################################

# Base configuration as shown above

# Point PeerTube to its dedicated KeyDB instance
peertube_config_redis_hostname: mash-peertube-keydb

# Make sure the PeerTube service (mash-peertube.service) starts after its dedicated KeyDB service (mash-peertube-keydb.service)
peertube_systemd_required_services_list_custom:
  - "mash-peertube-keydb.service"

# Make sure the PeerTube container is connected to the container network of its dedicated KeyDB service (mash-peertube-keydb)
peertube_container_additional_networks_custom:
  - "mash-peertube-keydb"

########################################################################
#                                                                      #
# /peertube                                                            #
#                                                                      #
########################################################################
```


## Installation

If you've decided to install a dedicated KeyDB instance for PeerTube, make sure to first do [installation](../installing.md) for the supplementary inventory host (e.g. `peertube.example.com-deps`), before running installation for the main one (e.g. `peertube.example.com`).


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
