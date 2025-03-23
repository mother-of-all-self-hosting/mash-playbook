<!--
SPDX-FileCopyrightText: 2023 - 2024 Slavi Pantaleev

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Lago

[Lago](https://www.getlago.com/) is an open-source metering and usage-based billing solution.


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

# Valkey configuration, as described below

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


### Valkey

As described on the [Valkey](valkey.md) documentation page, if you're hosting additional services which require KeyDB on the same server, you'd better go for installing a separate Valkey instance for each service. See [Creating a Valkey instance dedicated to Lago](#creating-a-valkey-instance-dedicated-to-lago).

If you're only running Lago on this server and don't need to use KeyDB for anything else, you can [use a single Valkey instance](#using-the-shared-valkey-instance-for-lago).

#### Using the shared Valkey instance for Lago

To install a single (non-dedicated) Valkey instance (`mash-valkey`) and hook Lago to it, add the following **additional** configuration:

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
# lago                                                                 #
#                                                                      #
########################################################################

# Base configuration as shown above

# Point Lago to the shared Valkey instance
lago_redis_hostname: "{{ valkey_identifier }}"

# Make sure the Lago service (mash-lago.service) starts after the shared KeyDB service (mash-valkey.service)
lago_api_systemd_required_services_list_custom:
  - "{{ valkey_identifier }}.service"

# Make sure the Lago container is connected to the container network of the shared KeyDB service (mash-valkey)
lago_api_container_additional_networks_custom:
  - "{{ valkey_identifier }}"

########################################################################
#                                                                      #
# /lago                                                                #
#                                                                      #
########################################################################
```

This will create a `mash-valkey` Valkey instance on this host.

This is only recommended if you won't be installing other services which require KeyDB. Alternatively, go for [Creating a Valkey instance dedicated to Lago](#creating-a-valkey-instance-dedicated-to-lago).

#### Creating a Valkey instance dedicated to Lago

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

This will create a `mash-lago-valkey` instance on this host with its data in `/mash/lago-valkey`.

Then, adjust your main inventory host's variables file (`inventory/host_vars/lago.example.com/vars.yml`) like this:

```yaml
########################################################################
#                                                                      #
# lago                                                             #
#                                                                      #
########################################################################

# Base configuration as shown above

# Point Lago to its dedicated Valkey instance
lago_redis_hostname: mash-lago-valkey

# Make sure the Lago service (mash-lago.service) starts after its dedicated KeyDB service (mash-lago-valkey.service)
lago_api_systemd_required_services_list_custom:
  - "mash-lago-valkey.service"

# Make sure the Lago container is connected to the container network of its dedicated KeyDB service (mash-lago-valkey)
lago_api_container_additional_networks_custom:
  - "mash-lago-valkey"

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
