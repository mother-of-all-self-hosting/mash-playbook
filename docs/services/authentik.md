# Authentik

[authentik](https://goauthentik.io/) is an open-source Identity Provider focused on flexibility and versatility. MASH can install authentik with the [`mother-of-all-self-hosting/ansible-role-authentik`](https://github.com/mother-of-all-self-hosting/ansible-role-authentik) ansible role.


> [!WARNING]
> SSO is pretty complex and while this role will install authentik for you we only tested OIDC and OAUTH integration. There is a high probability that using outposts/LDAP would need further configuration efforts. Make sure you test before using this in production and feel free to provide feedback!

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
# authentik                                                            #
#                                                                      #
########################################################################

authentik_enabled: true

authentik_hostname: authentik.example.com

# Put a strong secret below, generated with `pwgen -s 64 1` or in another way
authentik_secret_key: ''

# Valkey configuration, as described below

########################################################################
#                                                                      #
# /authentik                                                           #
#                                                                      #
########################################################################
```

### Valkey

As described on the [Valkey](valkey.md) documentation page, if you're hosting additional services which require KeyDB on the same server, you'd better go for installing a separate Valkey instance for each service. See [Creating a Valkey instance dedicated to authentik](#creating-a-valkey-instance-dedicated-to-authentik).

If you're only running authentik on this server and don't need to use KeyDB for anything else, you can [use a single Valkey instance](#using-the-shared-valkey-instance-for-authentik).

#### Using the shared Valkey instance for authentik

To install a single (non-dedicated) Valkey instance (`mash-valkey`) and hook authentik to it, add the following **additional** configuration:

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
# authentik                                                            #
#                                                                      #
########################################################################

# Base configuration as shown above

# Point authentik to the shared Valkey instance
authentik_config_redis_hostname: "{{ valkey_identifier }}"

# Make sure the authentik service (mash-authentik.service) starts after the shared KeyDB service (mash-valkey.service)
authentik_systemd_required_services_list_custom:
  - "{{ valkey_identifier }}.service"

# Make sure the authentik container is connected to the container network of the shared KeyDB service (mash-valkey)
authentik_container_additional_networks_custom:
  - "{{ valkey_identifier }}"

########################################################################
#                                                                      #
# /authentik                                                           #
#                                                                      #
########################################################################
```

This will create a `mash-valkey` Valkey instance on this host.

This is only recommended if you won't be installing other services which require KeyDB. Alternatively, go for [Creating a Valkey instance dedicated to authentik](#creating-a-valkey-instance-dedicated-to-authentik).


#### Creating a Valkey instance dedicated to authentik

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

This will create a `mash-authentik-valkey` instance on this host with its data in `/mash/authentik-valkey`.

Then, adjust your main inventory host's variables file (`inventory/host_vars/authentik.example.com/vars.yml`) like this:

```yaml
########################################################################
#                                                                      #
# authentik                                                            #
#                                                                      #
########################################################################

# Base configuration as shown above

# Point authentik to its dedicated Valkey instance
authentik_config_redis_hostname: mash-authentik-valkey

# Make sure the authentik service (mash-authentik.service) starts after its dedicated KeyDB service (mash-authentik-valkey.service)
authentik_systemd_required_services_list_custom:
  - "mash-authentik-valkey.service"

# Make sure the authentik container is connected to the container network of its dedicated KeyDB service (mash-authentik-valkey)
authentik_container_additional_networks_custom:
  - "mash-authentik-valkey"

########################################################################
#                                                                      #
# /authentik                                                           #
#                                                                      #
########################################################################
```


## Installation

If you've decided to install a dedicated Valkey instance for authentik, make sure to first do [installation](../installing.md) for the supplementary inventory host (e.g. `authentik.example.com-deps`), before running installation for the main one (e.g. `authentik.example.com`).


## Usage

After installation, you can set the admin password at `https://<authentik_hostname>/if/flow/initial-setup/`. Set the admin password there and start adding applications and users! Refer to the [official documentation](https://goauthentik.io/docs/) to learn how to integrate services. For this playbook tested examples are described in the respective service documentation. See

* [Grafana](./grafana.md#single-sign-on-authentik)
* [Nextcloud](./nextcloud.md#single-sign-on-authentik)


