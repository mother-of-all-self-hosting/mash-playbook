# PeerTube

[PeerTube](https://joinpeertube.org/) is a tool for sharing online videos developed by [Framasoft](https://framasoft.org/), a french non-profit.


## Dependencies

This service requires the following other services:

- a [Postgres](postgres.md) database
- a [Valkey](valkey.md) data-store, installation details [below](#valkey)
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

# Valkey configuration, as described below

########################################################################
#                                                                      #
# /peertube                                                            #
#                                                                      #
########################################################################
```

In the example configuration above, we configure the service to be hosted at `https://peertube.example.com`.

Hosting PeerTube under a subpath (by configuring the `peertube_path_prefix` variable) does not seem to be possible right now, due to PeerTube limitations.

### Valkey

As described on the [Valkey](valkey.md) documentation page, if you're hosting additional services which require KeyDB on the same server, you'd better go for installing a separate Valkey instance for each service. See [Creating a Valkey instance dedicated to PeerTube](#creating-a-valkey-instance-dedicated-to-peertube).

If you're only running PeerTube on this server and don't need to use KeyDB for anything else, you can [use a single Valkey instance](#using-the-shared-valkey-instance-for-peertube).

#### Using the shared Valkey instance for PeerTube

To install a single (non-dedicated) Valkey instance (`mash-valkey`) and hook PeerTube to it, add the following **additional** configuration:

```yaml
########################################################################
#                                                                      #
# valkey                                                               #
#                                                                      #
########################################################################

valkey_enabled: true

########################################################################
#                                                                      #
# /valkey                                                              #
#                                                                      #
########################################################################


########################################################################
#                                                                      #
# peertube                                                             #
#                                                                      #
########################################################################

# Base configuration as shown above

# Point PeerTube to the shared Valkey instance
peertube_config_redis_hostname: "{{ valkey_identifier }}"

# Make sure the PeerTube service (mash-peertube.service) starts after the shared KeyDB service (mash-valkey.service)
peertube_systemd_required_services_list_custom:
  - "{{ valkey_identifier }}.service"

# Make sure the PeerTube container is connected to the container network of the shared KeyDB service (mash-valkey)
peertube_container_additional_networks_custom:
  - "{{ valkey_identifier }}"

########################################################################
#                                                                      #
# /peertube                                                            #
#                                                                      #
########################################################################
```

This will create a `mash-valkey` Valkey instance on this host.

This is only recommended if you won't be installing other services which require KeyDB. Alternatively, go for [Creating a Valkey instance dedicated to PeerTube](#creating-a-valkey-instance-dedicated-to-peertube).


#### Creating a Valkey instance dedicated to PeerTube

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
# valkey                                                               #
#                                                                      #
########################################################################

valkey_enabled: true

########################################################################
#                                                                      #
# /valkey                                                              #
#                                                                      #
########################################################################
```

This will create a `mash-peertube-valkey` instance on this host with its data in `/mash/peertube-valkey`.

Then, adjust your main inventory host's variables file (`inventory/host_vars/peertube.example.com/vars.yml`) like this:

```yaml
########################################################################
#                                                                      #
# peertube                                                             #
#                                                                      #
########################################################################

# Base configuration as shown above

# Point PeerTube to its dedicated Valkey instance
peertube_config_redis_hostname: mash-peertube-valkey

# Make sure the PeerTube service (mash-peertube.service) starts after its dedicated KeyDB service (mash-peertube-valkey.service)
peertube_systemd_required_services_list_custom:
  - "mash-peertube-valkey.service"

# Make sure the PeerTube container is connected to the container network of its dedicated KeyDB service (mash-peertube-valkey)
peertube_container_additional_networks_custom:
  - "mash-peertube-valkey"

########################################################################
#                                                                      #
# /peertube                                                            #
#                                                                      #
########################################################################
```


## Installation

If you've decided to install a dedicated Valkey instance for PeerTube, make sure to first do [installation](../installing.md) for the supplementary inventory host (e.g. `peertube.example.com-deps`), before running installation for the main one (e.g. `peertube.example.com`).


## Usage

After [installation](../installing.md), you should be able to access your new PeerTube instance at the URL you've chosen (depending on `peertube_hostname` and `peertube_path_prefix` values set in `vars.yml`).

You should then be able to log in with:

- username: `root`
- password: the password you've set in `peertube_config_root_user_initial_password` in `vars.yml`
