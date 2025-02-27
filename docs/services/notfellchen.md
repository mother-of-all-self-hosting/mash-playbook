# Notfellchen

[Notfellchen](https://codeberg.org/moanos/notfellchen) is a self-hosted tool to list animals available for adoption to increase their chance of finding a forever-home.


> [!WARNING]
> This service is a custom solution. Feel free to use it but don't expect a solution that works for every use case. Issues with this should be filed in the [project itself](https://codeberg.org/moanos/notfellchen).

## Dependencies

This service requires the following other services:

- a [Postgres](postgres.md) database
- a [Traefik](traefik.md) reverse-proxy server


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# notfellchen                                                          #
#                                                                      #
########################################################################

notfellchen_enabled: true
notfellchen_hostname: notfellchen.example.com

########################################################################
#                                                                      #
# /notfellchen                                                         #
#                                                                      #
########################################################################
```

### Valkey

As described on the [Valkey](valkey.md) documentation page, if you're hosting additional services which require KeyDB on the same server, you'd better go for installing a separate Valkey instance for each service. See [Creating a Valkey instance dedicated to notfellchen](#creating-a-valkey-instance-dedicated-to-notfellchen).

If you're only running notfellchen on this server and don't need to use KeyDB for anything else, you can [use a single Valkey instance](#using-the-shared-valkey-instance-for-notfellchen).

#### Using the shared Valkey instance for notfellchen

To install a single (non-dedicated) Valkey instance (`mash-valkey`) and hook notfellchen to it, add the following **additional** configuration:

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
# notfellchen                                                          #
#                                                                      #
########################################################################

# Base configuration as shown above

# Point notfellchen to the shared Valkey instance
notfellchen_config_redis_hostname: "{{ valkey_identifier }}"

# Make sure the notfellchen API service (mash-notfellchen.service) starts after the shared KeyDB service
notfellchen_api_systemd_required_services_list_custom:
  - "{{ valkey_identifier }}.service"

# Make sure the notfellchen API service (mash-notfellchen.service) is connected to the container network of the shared KeyDB service
notfellchen_container_additional_networks_custom:
  - "{{ valkey_container_network }}"

########################################################################
#                                                                      #
# /notfellchen                                                           #
#                                                                      #
########################################################################
```

This will create a `mash-valkey` Valkey instance on this host.

This is only recommended if you won't be installing other services which require KeyDB. Alternatively, go for [Creating a Valkey instance dedicated to notfellchen](#creating-a-valkey-instance-dedicated-to-notfellchen).


#### Creating a Valkey instance dedicated to notfellchen

The following instructions are based on the [Running multiple instances of the same service on the same host](../running-multiple-instances.md) documentation.

Adjust your `inventory/hosts` file as described in [Re-do your inventory to add supplementary hosts](../running-multiple-instances.md#re-do-your-inventory-to-add-supplementary-hosts), adding a new supplementary host (e.g. if `notfellchen.example.com` is your main one, create `notfellchen.example.com-deps`).

Then, create a new `vars.yml` file for the

`inventory/host_vars/notfellchen.example.com-deps/vars.yml`:

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
mash_playbook_service_identifier_prefix: 'mash-notfellchen-'
mash_playbook_service_base_directory_name_prefix: 'notfellchen-'

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

This will create a `mash-notfellchen-valkey` instance on this host with its data in `/mash/notfellchen-valkey`.

Then, adjust your main inventory host's variables file (`inventory/host_vars/notfellchen.example.com/vars.yml`) like this:

```yaml
########################################################################
#                                                                      #
# notfellchen                                                            #
#                                                                      #
########################################################################

# Base configuration as shown above

# Point notfellchen to its dedicated Valkey instance
notfellchen_config_redis_hostname: mash-notfellchen-valkey

# Make sure the notfellchen ervice (mash-notfellchen.service) starts after its dedicated KeyDB service
notfellchen_systemd_required_services_list_custom:
  - "mash-notfellchen-valkey.service"

# Make sure the notfellchen service (mash-notfellchen.service) is connected to the container network of its dedicated KeyDB service
notfellchen_api_container_additional_networks_custom:
  - "mash-notfellchen-valkey"

########################################################################
#                                                                      #
# /notfellchen                                                         #
#                                                                      #
########################################################################
```



## Setting up the first user

You need to create a first user (unless you import an existing database).
You can do this conveniently by running

```bash
just run-tags notfellchen-add-superuser --extra-vars=username=USERNAME --extra-vars=password=PASSWORD --extra-vars=email=EMAIL
```

## Usage

After installation, you can go to the URL, as defined in `notfellchen_hostname`. Log in with the user credentials from above.
