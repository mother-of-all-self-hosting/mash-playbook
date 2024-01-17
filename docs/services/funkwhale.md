# Funkwhale

[Funkwhale](funkwhale.audio/) is a community-driven project that lets you listen and share music and audio within a decentralized, open network.


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
# funkwhale                                                               #
#                                                                      #
########################################################################

funkwhale_enabled: true

funkwhale_hostname: mash.example.com

# Put a strong secret below, generated with `pwgen -s 64 1` or in another way
funkwhale_django_secret_key: ''

# Redis configuration, as described below

########################################################################
#                                                                      #
# /funkwhale                                                              #
#                                                                      #
########################################################################
```

### Redis

As described on the [Redis](redis.md) documentation page, if you're hosting additional services which require Redis on the same server, you'd better go for installing a separate Redis instance for each service. See [Creating a Redis instance dedicated to funkwhale](#creating-a-redis-instance-dedicated-to-funkwhale).

If you're only running funkwhale on this server and don't need to use Redis for anything else, you can [use a single Redis instance](#using-the-shared-redis-instance-for-funkwhale).

#### Using the shared Redis instance for funkwhale

To install a single (non-dedicated) Redis instance (`mash-redis`) and hook funkwhale to it, add the following **additional** configuration:

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
# funkwhale                                                            #
#                                                                      #
########################################################################

# Base configuration as shown above

# Point funkwhale to the shared Redis instance
funkwhale_config_redis_hostname: "{{ redis_identifier }}"

# Make sure the funkwhale API service (mash-funkwhale-api.service) starts after the shared Redis service
funkwhale_api_systemd_required_services_list_custom:
  - "{{ redis_identifier }}.service"

# Make sure the funkwhale API service (mash-funkwhale-api.service) is connected to the container network of the shared Redis service
funkwhale_api_container_additional_networks_custom:
  - "{{ redis_container_network }}"

########################################################################
#                                                                      #
# /funkwhale                                                           #
#                                                                      #
########################################################################
```

This will create a `mash-redis` Redis instance on this host.

This is only recommended if you won't be installing other services which require Redis. Alternatively, go for [Creating a Redis instance dedicated to funkwhale](#creating-a-redis-instance-dedicated-to-funkwhale).


#### Creating a Redis instance dedicated to funkwhale

The following instructions are based on the [Running multiple instances of the same service on the same host](../running-multiple-instances.md) documentation.

Adjust your `inventory/hosts` file as described in [Re-do your inventory to add supplementary hosts](../running-multiple-instances.md#re-do-your-inventory-to-add-supplementary-hosts), adding a new supplementary host (e.g. if `funkwhale.example.com` is your main one, create `funkwhale.example.com-deps`).

Then, create a new `vars.yml` file for the

`inventory/host_vars/funkwhale.example.com-deps/vars.yml`:

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
mash_playbook_service_identifier_prefix: 'mash-funkwhale-'
mash_playbook_service_base_directory_name_prefix: 'funkwhale-'

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

This will create a `mash-funkwhale-redis` instance on this host with its data in `/mash/funkwhale-redis`.

Then, adjust your main inventory host's variables file (`inventory/host_vars/funkwhale.example.com/vars.yml`) like this:

```yaml
########################################################################
#                                                                      #
# funkwhale                                                            #
#                                                                      #
########################################################################

# Base configuration as shown above

# Point funkwhale to its dedicated Redis instance
funkwhale_config_redis_hostname: mash-funkwhale-redis

# Make sure the funkwhale API service (mash-funkwhale-api.service) starts after its dedicated Redis service
funkwhale_api_systemd_required_services_list_custom:
  - "mash-funkwhale-redis.service"

# Make sure the funkwhale API service (mash-funkwhale-api.service) is connected to the container network of its dedicated Redis service
funkwhale_api_container_additional_networks_custom:
  - "mash-funkwhale-redis"

########################################################################
#                                                                      #
# /funkwhale                                                           #
#                                                                      #
########################################################################
```


## Installation

If you've decided to install a dedicated Redis instance for funkwhale, make sure to first do [installation](../installing.md) for the supplementary inventory host (e.g. `funkwhale.example.com-deps`), before running installation for the main one (e.g. `funkwhale.example.com`).


## Usage

After installation, you can go to the funkwhale URL, as defined in `funkwhale_hostname`. To login and get started you first have to create a user. you can do this with
```bash
just run-tags funkwhale-add-superuser --extra-vars=username=USERNAME --extra-vars=password=PASSWORD --extra-vars=email=EMAIL
```

All other users can be created in the Web GUI.
