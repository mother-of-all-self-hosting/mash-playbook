# NetBox

[NetBox](https://docs.netbox.dev/en/stable/) is an open-source web application that provides [IP address management (IPAM)](https://en.wikipedia.org/wiki/IP_address_management) and [data center infrastructure management (DCIM)](https://en.wikipedia.org/wiki/Data_center_management#Data_center_infrastructure_management) functionality.


## Dependencies

This service requires the following other services:

- a [Postgres](postgres.md) database
- a [Redis](redis.md) data-store, installation details [below](#redis)
- a [Traefik](traefik.md) reverse-proxy server


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# netbox                                                               #
#                                                                      #
########################################################################

netbox_enabled: true

netbox_hostname: mash.example.com
netbox_path_prefix: /netbox

# Put a strong secret below, generated with `pwgen -s 64 1` or in another way
netbox_environment_variable_secret_key: ''

# The following superuser will be created upon launch.
netbox_environment_variable_superuser_name: your_username_here
netbox_environment_variable_superuser_email: your.email@example.com
# Put a strong secret below, generated with `pwgen -s 64 1` or in another way.
# Changing the password subsequently will not affect the user's password.
netbox_environment_variable_superuser_password: ''

# Redis configuration, as described below

########################################################################
#                                                                      #
# /netbox                                                              #
#                                                                      #
########################################################################
```

### URL

In the example configuration above, we configure the service to be hosted at `https://mash.example.com/netbox`.

You can remove the `netbox_path_prefix` variable definition, to make it default to `/`, so that the service is served at `https://mash.example.com/`.


### Authentication

If `netbox_environment_variable_superuser_*` variables are specified, NetBox will try to create the user (if missing).


### Redis

As described on the [Redis](redis.md) documentation page, if you're hosting additional services which require Redis on the same server, you'd better go for installing a separate Redis instance for each service. See [Creating a Redis instance dedicated to NetBox](#creating-a-redis-instance-dedicated-to-netbox).

If you're only running NetBox on this server and don't need to use Redis for anything else, you can [use a single Redis instance](#using-the-shared-redis-instance-for-netbox).

#### Using the shared Redis instance for NetBox

To install a single (non-dedicated) Redis instance (`mash-redis`) and hook NetBox to it, add the following **additional** configuration:

```yaml
########################################################################
#                                                                      #
# redis                                                                #
#                                                                      #
########################################################################

redis_enabled: true

########################################################################
#                                                                      #
# /redis                                                               #
#                                                                      #
########################################################################


########################################################################
#                                                                      #
# netbox                                                               #
#                                                                      #
########################################################################

# Base configuration as shown above

# Point NetBox to the shared Redis instance
netbox_config_redis_hostname: "{{ redis_identifier }}"

# Make sure the NetBox service (mash-netbox.service) starts after the shared Redis service (mash-redis.service)
netbox_systemd_required_services_list_custom:
  - "{{ redis_identifier }}.service"

# Make sure the NetBox container is connected to the container network of the shared Redis service (mash-redis)
netbox_container_additional_networks_custom:
  - "{{ redis_identifier }}"

########################################################################
#                                                                      #
# /netbox                                                              #
#                                                                      #
########################################################################
```

This will create a `mash-redis` Redis instance on this host.

This is only recommended if you won't be installing other services which require Redis. Alternatively, go for [Creating a Redis instance dedicated to NetBox](#creating-a-redis-instance-dedicated-to-netbox).


#### Creating a Redis instance dedicated to NetBox

The following instructions are based on the [Running multiple instances of the same service on the same host](../running-multiple-instances.md) documentation.

Adjust your `inventory/hosts` file as described in [Re-do your inventory to add supplementary hosts](../running-multiple-instances.md#re-do-your-inventory-to-add-supplementary-hosts), adding a new supplementary host (e.g. if `netbox.example.com` is your main one, create `netbox.example.com-deps`).

Then, create a new `vars.yml` file for the

`inventory/host_vars/netbox.example.com-deps/vars.yml`:

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
mash_playbook_service_identifier_prefix: 'mash-netbox-'
mash_playbook_service_base_directory_name_prefix: 'netbox-'

########################################################################
#                                                                      #
# /Playbook                                                            #
#                                                                      #
########################################################################


########################################################################
#                                                                      #
# redis                                                                #
#                                                                      #
########################################################################

redis_enabled: true

########################################################################
#                                                                      #
# /redis                                                               #
#                                                                      #
########################################################################
```

This will create a `mash-netbox-redis` instance on this host with its data in `/mash/netbox-redis`.

Then, adjust your main inventory host's variables file (`inventory/host_vars/netbox.example.com/vars.yml`) like this:

```yaml
########################################################################
#                                                                      #
# netbox                                                               #
#                                                                      #
########################################################################

# Base configuration as shown above


# Point NetBox to its dedicated Redis instance
netbox_environment_variable_redis_host: mash-netbox-redis
netbox_environment_variable_redis_cache_host: mash-netbox-redis

# Make sure the NetBox service (mash-netbox.service) starts after its dedicated Redis service (mash-netbox-redis.service)
netbox_systemd_required_services_list_custom:
  - "mash-netbox-redis.service"

# Make sure the NetBox container is connected to the container network of its dedicated Redis service (mash-netbox-redis)
netbox_container_additional_networks_custom:
  - "mash-netbox-redis"

########################################################################
#                                                                      #
# /netbox                                                              #
#                                                                      #
########################################################################
```


## Installation

If you've decided to install a dedicated Redis instance for NetBox, make sure to first do [installation](../installing.md) for the supplementary inventory host (e.g. `netbox.example.com-deps`), before running installation for the main one (e.g. `netbox.example.com`).


## Usage

After installation, you can go to the NetBox URL, as defined in `netbox_hostname` and `netbox_path_prefix`.

You can log in with the **username** (**not** email) and password specified in the `netbox_environment_variable_superuser*` variables.
