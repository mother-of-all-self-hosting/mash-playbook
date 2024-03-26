# Lago

[Lago](https://www.getlago.com/) is an open-source metering and usage-based billing solution.


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
# lago                                                                 #
#                                                                      #
########################################################################

lago_enabled: true

lago_hostname: lago.example.com

# Generate this using `openssl genrsa 2048 | base64 --wrap=0`
lago_api_environment_variable_lago_rsa_private_key: ''

# WARNING: remove this after you create your user account,
# unless you'd like to run a server with public registration enabled.
lago_front_environment_variable_lago_disable_signup: false

# KeyDB configuration, as described below

########################################################################
#                                                                      #
# /lago                                                                #
#                                                                      #
########################################################################
```


### URL

In the example configuration above, we configure the service to be hosted at `https://lago.example.com`.

Hosting Lago under a subpath (by configuring the `lago_path_prefix` variable) does not seem to be possible right now, due to Lago limitations.

Our setup hosts the Lago frontend at the root path (`/`) and the Lago API at the `/api` prefix.
This seems to work well, except for [PDF invoices failing due to a Lago bug](https://github.com/getlago/lago/issues/221).


### Authentication

Public registration can be enabled/disabled using the `lago_front_environment_variable_lago_disable_signup` variable.

We recommend installing with public registration enabled at first, creating your first user account, and then disabling public registration (unless you need it).

It should be noted that disabling public signup with this variable merely disables the Sign-Up page in the web interface, but [does not actually disable signups due to a Lago bug](https://github.com/getlago/lago/issues/220).


### KeyDB

As described on the [KeyDB](keydb.md) documentation page, if you're hosting additional services which require KeyDB on the same server, you'd better go for installing a separate KeyDB instance for each service. See [Creating a KeyDB instance dedicated to Lago](#creating-a-keydb-instance-dedicated-to-lago).

If you're only running Lago on this server and don't need to use KeyDB for anything else, you can [use a single KeyDB instance](#using-the-shared-keydb-instance-for-lago).

#### Using the shared KeyDB instance for Lago

To install a single (non-dedicated) KeyDB instance (`mash-keydb`) and hook Lago to it, add the following **additional** configuration:

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
# lago                                                                 #
#                                                                      #
########################################################################

# Base configuration as shown above

# Point Lago to the shared KeyDB instance
lago_redis_hostname: "{{ keydb_identifier }}"

# Make sure the Lago service (mash-lago.service) starts after the shared KeyDB service (mash-keydb.service)
lago_api_systemd_required_services_list_custom:
  - "{{ keydb_identifier }}.service"

# Make sure the Lago container is connected to the container network of the shared KeyDB service (mash-keydb)
lago_api_container_additional_networks_custom:
  - "{{ keydb_identifier }}"

########################################################################
#                                                                      #
# /lago                                                                #
#                                                                      #
########################################################################
```

This will create a `mash-keydb` KeyDB instance on this host.

This is only recommended if you won't be installing other services which require KeyDB. Alternatively, go for [Creating a KeyDB instance dedicated to Lago](#creating-a-keydb-instance-dedicated-to-lago).

#### Creating a KeyDB instance dedicated to Lago

The following instructions are based on the [Running multiple instances of the same service on the same host](../running-multiple-instances.md) documentation.

Adjust your `inventory/hosts` file as described in [Re-do your inventory to add supplementary hosts](../running-multiple-instances.md#re-do-your-inventory-to-add-supplementary-hosts), adding a new supplementary host (e.g. if `lago.example.com` is your main one, create `lago.example.com-deps`).

Then, create a new `vars.yml` file for the

`inventory/host_vars/lago.example.com-deps/vars.yml`:

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
mash_playbook_service_identifier_prefix: 'mash-lago-'
mash_playbook_service_base_directory_name_prefix: 'lago-'

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

This will create a `mash-lago-keydb` instance on this host with its data in `/mash/lago-keydb`.

Then, adjust your main inventory host's variables file (`inventory/host_vars/lago.example.com/vars.yml`) like this:

```yaml
########################################################################
#                                                                      #
# lago                                                             #
#                                                                      #
########################################################################

# Base configuration as shown above

# Point Lago to its dedicated KeyDB instance
lago_redis_hostname: mash-lago-keydb

# Make sure the Lago service (mash-lago.service) starts after its dedicated KeyDB service (mash-lago-keydb.service)
lago_api_systemd_required_services_list_custom:
  - "mash-lago-keydb.service"

# Make sure the Lago container is connected to the container network of its dedicated KeyDB service (mash-lago-keydb)
lago_api_container_additional_networks_custom:
  - "mash-lago-keydb"

########################################################################
#                                                                      #
# /lago                                                            #
#                                                                      #
########################################################################
```


## Usage

After installation, you can go to the Lago URL, as defined in `lago_hostname`.

As mentioned in [Authentication](#authentication) above, you can create the first user from the web interface.

If you'd like to prevent other users from registering, consider disabling public registration by removing the `lago_front_environment_variable_lago_disable_signup` references from your configuration and re-running the playbook (`just install-service lago`).
