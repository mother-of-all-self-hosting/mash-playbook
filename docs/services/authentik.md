# Authentik

[authentik](https://goauthentik.io/) is an open-source Identity Provider focused on flexibility and versatility. MASH can install authentik with the [`mother-of-all-self-hosting/ansible-role-authentik`](https://github.com/mother-of-all-self-hosting/ansible-role-authentik) ansible role.


**Warning:** SSO is pretty complex and while this role will install authentik for you we only tested OIDC and OAUTH integration. There is a high probability that using outposts/LDAP would need further configuration efforts. Make sure you test before using this in production and feel free to provide feedback!

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
# authentik                                                            #
#                                                                      #
########################################################################

authentik_enabled: true
authentik_hostname: authentik.example.com
authentik_secret_key: 'verysecret'

########################################################################
#                                                                      #
# /authentik                                                           #
#                                                                      #
########################################################################
```

### Redis

As described on the [Redis](redis.md) documentation page, if you're hosting additional services which require Redis on the same server, you'd better go for installing a separate Redis instance for each service. See [Creating a Redis instance dedicated to authentik](#creating-a-redis-instance-dedicated-to-authentik).

If you're only running authentik on this server and don't need to use Redis for anything else, you can [use a single Redis instance](#using-the-shared-redis-instance-for-authentik).

#### Using the shared Redis instance for authentik

To install a single (non-dedicated) Redis instance (`mash-redis`) and hook authentik to it, add the following **additional** configuration:

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
# authentik                                                               #
#                                                                      #
########################################################################

# Base configuration as shown above

# Point authentik to the shared Redis instance
authentik_config_redis_hostname: "{{ redis_identifier }}"

# Make sure the authentik service (mash-authentik.service) starts after the shared Redis service (mash-redis.service)
authentik_systemd_required_services_list_custom:
  - "{{ redis_identifier }}.service"

# Make sure the authentik container is connected to the container network of the shared Redis service (mash-redis)
authentik_container_additional_networks_custom:
  - "{{ redis_identifier }}"

########################################################################
#                                                                      #
# /authentik                                                              #
#                                                                      #
########################################################################
```

This will create a `mash-redis` Redis instance on this host.

This is only recommended if you won't be installing other services which require Redis. Alternatively, go for [Creating a Redis instance dedicated to authentik](#creating-a-redis-instance-dedicated-to-authentik).


#### Creating a Redis instance dedicated to authentik

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

This will create a `mash-authentik-redis` instance on this host with its data in `/mash/authentik-redis`.

Then, adjust your main inventory host's variables file (`inventory/host_vars/authentik.example.com/vars.yml`) like this:

```yaml
########################################################################
#                                                                      #
# authentik                                                               #
#                                                                      #
########################################################################

# Base configuration as shown above


# Point authentik to its dedicated Redis instance
authentik_environment_variable_redis_host: mash-authentik-redis
authentik_environment_variable_redis_cache_host: mash-authentik-redis

# Make sure the authentik service (mash-authentik.service) starts after its dedicated Redis service (mash-authentik-redis.service)
authentik_systemd_required_services_list_custom:
  - "mash-authentik-redis.service"

# Make sure the authentik container is connected to the container network of its dedicated Redis service (mash-authentik-redis)
authentik_container_additional_networks_custom:
  - "mash-authentik-redis"

########################################################################
#                                                                      #
# /authentik                                                              #
#                                                                      #
########################################################################
```


## Installation

If you've decided to install a dedicated Redis instance for authentik, make sure to first do [installation](../installing.md) for the supplementary inventory host (e.g. `authentik.example.com-deps`), before running installation for the main one (e.g. `authentik.example.com`).


## Usage

After installation, you can set the admin password at `https://<authentik_hostname>/if/flow/initial-setup/`. Set the admin password there and start adding applications and users! Refer to the [official documentation](https://goauthentik.io/docs/) to learn how to integrate services. For this playbook tested examples are described in the respective service documentation. See

* [Grafana](./grafana.md)
* [Nextcloud](./nextcloud.md)


