# Funkwhale

[Funkwhale](https://funkwhale.audio/) is a community-driven project that lets you listen and share music and audio within a decentralized, open network.


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
# funkwhale                                                               #
#                                                                      #
########################################################################

funkwhale_enabled: true

funkwhale_hostname: mash.example.com

# Put a strong secret below, generated with `pwgen -s 64 1` or in another way
funkwhale_django_secret_key: ''

# Valkey configuration, as described below

########################################################################
#                                                                      #
# /funkwhale                                                              #
#                                                                      #
########################################################################
```

### Valkey

As described on the [Valkey](valkey.md) documentation page, if you're hosting additional services which require KeyDB on the same server, you'd better go for installing a separate Valkey instance for each service. See [Creating a Valkey instance dedicated to funkwhale](#creating-a-valkey-instance-dedicated-to-funkwhale).

If you're only running funkwhale on this server and don't need to use KeyDB for anything else, you can [use a single Valkey instance](#using-the-shared-valkey-instance-for-funkwhale).

#### Using the shared Valkey instance for funkwhale

To install a single (non-dedicated) Valkey instance (`mash-valkey`) and hook funkwhale to it, add the following **additional** configuration:

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
# funkwhale                                                            #
#                                                                      #
########################################################################

# Base configuration as shown above

# Point funkwhale to the shared Valkey instance
funkwhale_config_redis_hostname: "{{ valkey_identifier }}"

# Make sure the funkwhale API service (mash-funkwhale-api.service) starts after the shared KeyDB service
funkwhale_api_systemd_required_services_list_custom:
  - "{{ valkey_identifier }}.service"

# Make sure the funkwhale API service (mash-funkwhale-api.service) is connected to the container network of the shared KeyDB service
funkwhale_api_container_additional_networks_custom:
  - "{{ valkey_container_network }}"

########################################################################
#                                                                      #
# /funkwhale                                                           #
#                                                                      #
########################################################################
```

This will create a `mash-valkey` Valkey instance on this host.

This is only recommended if you won't be installing other services which require KeyDB. Alternatively, go for [Creating a Valkey instance dedicated to funkwhale](#creating-a-valkey-instance-dedicated-to-funkwhale).


#### Creating a Valkey instance dedicated to funkwhale

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

This will create a `mash-funkwhale-valkey` instance on this host with its data in `/mash/funkwhale-valkey`.

Then, adjust your main inventory host's variables file (`inventory/host_vars/funkwhale.example.com/vars.yml`) like this:

```yaml
########################################################################
#                                                                      #
# funkwhale                                                            #
#                                                                      #
########################################################################

# Base configuration as shown above

# Point funkwhale to its dedicated Valkey instance
funkwhale_config_redis_hostname: mash-funkwhale-valkey

# Make sure the funkwhale API service (mash-funkwhale-api.service) starts after its dedicated KeyDB service
funkwhale_api_systemd_required_services_list_custom:
  - "mash-funkwhale-valkey.service"

# Make sure the funkwhale API service (mash-funkwhale-api.service) is connected to the container network of its dedicated KeyDB service
funkwhale_api_container_additional_networks_custom:
  - "mash-funkwhale-valkey"

########################################################################
#                                                                      #
# /funkwhale                                                           #
#                                                                      #
########################################################################
```


## Installation

If you've decided to install a dedicated Valkey instance for funkwhale, make sure to first do [installation](../installing.md) for the supplementary inventory host (e.g. `funkwhale.example.com-deps`), before running installation for the main one (e.g. `funkwhale.example.com`).


## Usage

After installation, you can go to the funkwhale URL, as defined in `funkwhale_hostname`. To login and get started you first have to create a user. you can do this with
```bash
just run-tags funkwhale-add-superuser --extra-vars=username=USERNAME --extra-vars=password=PASSWORD --extra-vars=email=EMAIL
```

All other users can be created in the Web GUI.
