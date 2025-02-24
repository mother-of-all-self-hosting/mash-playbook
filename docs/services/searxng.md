# SearXNG

[SearXNG](https://github.com/searxng/searxng/) is a privacy-respecting, hackable [metasearch engine](https://en.wikipedia.org/wiki/Metasearch_engine).

## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server

If rate-limiting is enabled, then it also requires:

- a [Valkey](valkey.md) database

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# searxng                                                              #
#                                                                      #
########################################################################

searxng_enabled: true

searxng_instance_name: My Example Instance Name'

searxng_hostname: searxng.example.com

# If you want to server SearXNG under a subpath, you can specify it here.
#searxng_path_prefix: '/'

# Generate the secret key with "openssl rand -hex 32".
searxng_secret_key: 'MY_SECRET_KEY'

########################################################################
#                                                                      #
# /searxng                                                             #
#                                                                      #
########################################################################
```

In the example configuration above, we configure the service to be hosted at `https://searxng.example.com`.

It is possible to host SearXNG under a subpath (by configuring the `searxng_path_prefix` variable).

### Configuring rate-limiting

If you want to enable rate-limiting, you will also need to enable Valkey. As described on the [Valkey](valkey.md) documentation page, if you're hosting additional services which require Valkey on the same server, you'd better go for installing a separate Valkey instance for each service. See [Creating a Valkey instance dedicated to SearXNG](...).

You will also need to enable rate-limiting for SearXNG by setting:

```yaml
searxng_enable_rate_limiter: true
```

#### Creating a Valkey instance dedicated to SearXNG

The following instructions are based on the [Running multiple instances of the same service on the same host](running-multiple-instances.md#re-do-your-inventory-to-add-supplementary-hosts) documentation.

Adjust your `inventory/hosts` file as described in [Re-do your inventory to add supplementary hosts](../running-multiple-instances.md#re-do-your-inventory-to-add-supplementary-hosts), adding a new supplementary host (e.g. if `searxng.example.com` is your main one, create `searxng.example.com-deps`).

Then, create a new `vars.yml` file for the `inventory/host_vars/searxng.example.com-deps/vars.yml`:

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
mash_playbook_service_identifier_prefix: 'mash-searxng-'
mash_playbook_service_base_directory_name_prefix: 'searxng-'

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

This will create a `mash-searxng-valkey` instance on this host with its data in `/mash/searxng-valkey`.

Then, adjust your main inventory host's variables file (`inventory/host_vars/searxng.example.com/vars.yml`) like this:

```yaml
########################################################################
#                                                                      #
# searxng                                                              #
#                                                                      #
########################################################################

# Base configuration as shown above

# Point Searxng to its dedicated Valkey instance
searxng_rate_limiter_config_valkey_hostname: mash-searxng-valkey

# Make sure the Searxng service (mash-searxng.service) starts after its dedicated KeyDB service (mash-searxng-valkey.service)
searxng_systemd_required_services_list_custom:
  - "mash-searxng-valkey.service"

# Make sure the Searxng container is connected to the container network of its dedicated KeyDB service (mash-searxng-valkey)
searxng_container_additional_networks_custom:
  - "mash-searxng-valkey"

########################################################################
#                                                                      #
# /searxng                                                             #
#                                                                      #
########################################################################
```

### Configuring basic authentication

If you are running a private instance, you might want to protect it with so that only authorized people can use it. An easy option is to choose a non-trivial subpath by modifying the `searxng_path_prefix`. Another, more complete option is to enable basic authentication for the instance.

To do the latter, you need to set the following variables:

```yaml
searxng_basic_auth_enabled: true
searxng_basic_auth_username: 'my_username'
searxng_basic_auth_password: 'my_password'
```
