# NetBox

[NetBox](https://docs.netbox.dev/en/stable/) is an open-source web application that provides [IP address management (IPAM)](https://en.wikipedia.org/wiki/IP_address_management) and [data center infrastructure management (DCIM)](https://en.wikipedia.org/wiki/Data_center_management#Data_center_infrastructure_management) functionality.


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

# KeyDB configuration, as described below

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

[Single-Sign-On](#single-sign-on-sso-integration) is also supported.

### KeyDB

As described on the [KeyDB](keydb.md) documentation page, if you're hosting additional services which require KeyDB on the same server, you'd better go for installing a separate KeyDB instance for each service. See [Creating a KeyDB instance dedicated to NetBox](#creating-a-keydb-instance-dedicated-to-netbox).

If you're only running NetBox on this server and don't need to use KeyDB for anything else, you can [use a single KeyDB instance](#using-the-shared-keydb-instance-for-netbox).

#### Using the shared KeyDB instance for NetBox

To install a single (non-dedicated) KeyDB instance (`mash-keydb`) and hook NetBox to it, add the following **additional** configuration:

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
# netbox                                                               #
#                                                                      #
########################################################################

# Base configuration as shown above

# Point NetBox to the shared KeyDB instance
netbox_environment_variable_redis_host: "{{ keydb_identifier }}"
netbox_environment_variable_redis_cache_host: "{{ keydb_identifier }}"

# Make sure the NetBox service (mash-netbox.service) starts after the shared KeyDB service (mash-keydb.service)
netbox_systemd_required_services_list_custom:
  - "{{ keydb_identifier }}.service"

# Make sure the NetBox container is connected to the container network of the shared KeyDB service (mash-keydb)
netbox_container_additional_networks_custom:
  - "{{ keydb_identifier }}"

########################################################################
#                                                                      #
# /netbox                                                              #
#                                                                      #
########################################################################
```

This will create a `mash-keydb` KeyDB instance on this host.

This is only recommended if you won't be installing other services which require KeyDB. Alternatively, go for [Creating a KeyDB instance dedicated to NetBox](#creating-a-keydb-instance-dedicated-to-netbox).


#### Creating a KeyDB instance dedicated to NetBox

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

This will create a `mash-netbox-keydb` instance on this host with its data in `/mash/netbox-keydb`.

Then, adjust your main inventory host's variables file (`inventory/host_vars/netbox.example.com/vars.yml`) like this:

```yaml
########################################################################
#                                                                      #
# netbox                                                               #
#                                                                      #
########################################################################

# Base configuration as shown above


# Point NetBox to its dedicated KeyDB instance
netbox_environment_variable_redis_host: mash-netbox-keydb
netbox_environment_variable_redis_cache_host: mash-netbox-keydb

# Make sure the NetBox service (mash-netbox.service) starts after its dedicated KeyDB service (mash-netbox-keydb.service)
netbox_systemd_required_services_list_custom:
  - "mash-netbox-keydb.service"

# Make sure the NetBox container is connected to the container network of its dedicated KeyDB service (mash-netbox-keydb)
netbox_container_additional_networks_custom:
  - "mash-netbox-keydb"

########################################################################
#                                                                      #
# /netbox                                                              #
#                                                                      #
########################################################################
```

### Single-Sign-On (SSO) integration

NetBox supports different [Remote Authentication](https://docs.netbox.dev/en/stable/configuration/remote-authentication/) backends, including those provided by the [Python Social Auth](https://python-social-auth.readthedocs.io/) library. This library is included in the NetBox container image by default, so you can invoke any [backend](https://github.com/python-social-auth/social-core/tree/master/social_core/backends) provided by it.

Each module's Python file contains detailed information about how to configure it. It should be noted that module-specific configuration is passed as Python configuration (via `netbox_configuration_extra_python`), and **not as environment variables**.

We have detailed information about integrating with [Keycloak](keycloak.md) below.
You can use the configuration in the [Keycloak section](#keycloak) as a template for configuring other backends.

#### Keycloak

To integrate with [Keycloak](keycloak.md) use the following **additional** configuration:

```yaml
netbox_environment_variables_additional_variables: |
  REMOTE_AUTH_ENABLED=True
  REMOTE_AUTH_BACKEND=social_core.backends.keycloak.KeycloakOAuth2

  # Space-separated names of groups that new users will be assigned to.
  # These groups must be created manually (from the Admin panel's Groups section) before use.
  REMOTE_AUTH_DEFAULT_GROUPS=

netbox_configuration_extra_python: |
  # These need to match your Client app information in Keycloak. See below
  SOCIAL_AUTH_KEYCLOAK_KEY = ''
  SOCIAL_AUTH_KEYCLOAK_SECRET = ''

  # The value for this is retrieved from Keycloak -> Realm Settings -> Keys tab -> Public key button for RS256
  SOCIAL_AUTH_KEYCLOAK_PUBLIC_KEY = ''

  # The value for these are retrieved from Keycloak -> Realm Settings -> General tab -> OpenID Endpoint Configuration button
  SOCIAL_AUTH_KEYCLOAK_AUTHORIZATION_URL = 'https://KEYCLOAK_URL/realms/REALM_IDENTIFIER/protocol/openid-connect/auth'
  SOCIAL_AUTH_KEYCLOAK_ACCESS_TOKEN_URL = 'https://KEYCLOAK_URL/realms/REALM_IDENTIFIER/protocol/openid-connect/token'

# If Keycloak is running on the same server, uncomment the lines below
# and replace HOSTNAME with the hostname of the Keycloak server (e.g. mash.example.com or keycloak.example.com).
# netbox_container_extra_arguments:
#  - --add-host=HOSTNAME:{{ ansible_host }}
```

The Client app needs to be created and configured in a special way on the Keycloak side by:

- activating **Client authentication**
- **Valid redirect URIs**: `https://NETBOX_URL/oauth/complete/keycloak/`
- **Web origins**: `https://NETBOX_URL/`
- in **Advanced**, changing the following settings:
  - **Request object signature algorithm** = `RS256`
  - **User info signed response algorithm** = `RS256`
- in **Client scopes** (for this Client app via the **Client scopes** tab, not for all apps via the left-most menu), configure the `*-dedicated` scope (e.g. `netbox-dedicated` if you named your Client app `netbox`) and in the **Mappers** tab, click **Configure a new mapper** add a new **Audience** mapper with the following settings:
  - **Name** = anything you like (e.g. `netbox-audience`)
  - **Included Client Audience** = the key of this Client app (e.g. `netbox`)
  - **Add to access token** = On

For additional environment variables controlling groups and permissions for new users (like `REMOTE_AUTH_DEFAULT_GROUPS`), see the NetBox documentation for [Remote Authentication](https://docs.netbox.dev/en/stable/configuration/remote-authentication/).

## Installation

If you've decided to install a dedicated KeyDB instance for NetBox, make sure to first do [installation](../installing.md) for the supplementary inventory host (e.g. `netbox.example.com-deps`), before running installation for the main one (e.g. `netbox.example.com`).


## Usage

After installation, you can go to the NetBox URL, as defined in `netbox_hostname` and `netbox_path_prefix`.

You can log in with the **username** (**not** email) and password specified in the `netbox_environment_variable_superuser*` variables.
