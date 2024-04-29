# Paperless-ngx

[Paperless-ngx](https://paperless-ngx.com) s a community-supported open-source document management system that transforms your physical documents into a searchable online archive so you can keep, well, less paper. MASH can install paperless-ngx with the [`mother-of-all-self-hosting/ansible-role-paperless`](https://github.com/mother-of-all-self-hosting/ansible-role-paperless) ansible role.


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
# authentik                                                            #
#                                                                      #
########################################################################

authentik_enabled: true

authentik_hostname: authentik.example.com

# Put a strong secret below, generated with `pwgen -s 64 1` or in another way
authentik_secret_key: ''

# KeyDB configuration, as described below

########################################################################
#                                                                      #
# /authentik                                                           #
#                                                                      #
########################################################################
```

### KeyDB

As described on the [KeyDB](keydb.md) documentation page, if you're hosting additional services which require KeyDB on the same server, you'd better go for installing a separate KeyDB instance for each service. See [Creating a KeyDB instance dedicated to paperless-ngx](#creating-a-keydb-instance-dedicated-to-paperless-ngx).

If you're only running authentik on this server and don't need to use KeyDB for anything else, you can [use a single KeyDB instance](#using-the-shared-keydb-instance-for-authentik).

#### Using the shared KeyDB instance for authentik

To install a single (non-dedicated) KeyDB instance (`mash-keydb`) and hook authentik to it, add the following **additional** configuration:

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
# authentik                                                            #
#                                                                      #
########################################################################

# Base configuration as shown above

# Point authentik to the shared KeyDB instance
authentik_config_redis_hostname: "{{ keydb_identifier }}"

# Make sure the authentik service (mash-authentik.service) starts after the shared KeyDB service (mash-keydb.service)
authentik_systemd_required_services_list_custom:
  - "{{ keydb_identifier }}.service"

# Make sure the authentik container is connected to the container network of the shared KeyDB service (mash-keydb)
authentik_container_additional_networks_custom:
  - "{{ keydb_identifier }}"

########################################################################
#                                                                      #
# /authentik                                                           #
#                                                                      #
########################################################################
```

This will create a `mash-keydb` KeyDB instance on this host.

This is only recommended if you won't be installing other services which require KeyDB. Alternatively, go for [Creating a KeyDB instance dedicated to authentik](#creating-a-keydb-instance-dedicated-to-authentik).


#### Creating a KeyDB instance dedicated to authentik

The following instructions are based on the [Running multiple instances of the same service on the same host](../running-multiple-instances.md) documentation.

Adjust your `inventory/hosts` file as described in [Re-do your inventory to add supplementary hosts](../running-multiple-instances.md#re-do-your-inventory-to-add-supplementary-hosts), adding a new supplementary host (e.g. if `authentik.example.com` is your main one, create `authentik.example.com-deps`).

Then, create a new `vars.yml` file for the

`inventory/host_vars/authentik.example.com-deps/vars.yml`:

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
mash_playbook_service_identifier_prefix: 'mash-authentik-'
mash_playbook_service_base_directory_name_prefix: 'authentik-'

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

This will create a `mash-authentik-keydb` instance on this host with its data in `/mash/authentik-keydb`.

Then, adjust your main inventory host's variables file (`inventory/host_vars/authentik.example.com/vars.yml`) like this:

```yaml
########################################################################
#                                                                      #
# authentik                                                            #
#                                                                      #
########################################################################

# Base configuration as shown above

# Point authentik to its dedicated KeyDB instance
authentik_config_redis_hostname: mash-authentik-keydb

# Make sure the authentik service (mash-authentik.service) starts after its dedicated KeyDB service (mash-authentik-keydb.service)
authentik_systemd_required_services_list_custom:
  - "mash-authentik-keydb.service"

# Make sure the authentik container is connected to the container network of its dedicated KeyDB service (mash-authentik-keydb)
authentik_container_additional_networks_custom:
  - "mash-authentik-keydb"

########################################################################
#                                                                      #
# /authentik                                                           #
#                                                                      #
########################################################################
```


## Installation

If you've decided to install a dedicated KeyDB instance for paperless, make sure to first do [installation](../installing.md) for the supplementary inventory host (e.g. `paperless.example.com-deps`), before running installation for the main one (e.g. `paperless.example.com`).


## Usage

Access your instance in your browser at `https://paperless.example.org`

Refer to the [official documentation](https://docs.paperless-ngx.com/) to learn how to use paperless.