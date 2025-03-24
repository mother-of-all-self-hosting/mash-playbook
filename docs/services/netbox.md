<!--
SPDX-FileCopyrightText: 2023 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# NetBox

[NetBox](https://docs.netbox.dev/en/stable/) is an open-source web application that provides [IP address management (IPAM)](https://en.wikipedia.org/wiki/IP_address_management) and [data center infrastructure management (DCIM)](https://en.wikipedia.org/wiki/Data_center_management#Data_center_infrastructure_management) functionality.


## Dependencies

This service requires the following other services:

- a [Postgres](postgres.md) database
- a [Traefik](traefik.md) reverse-proxy server
- a [Valkey](valkey.md) data-store; see [below](#configure-valkey) for details about installation


## Configuration

To enable this service, add the following configuration to your `vars.yml` file:

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

########################################################################
#                                                                      #
# /netbox                                                              #
#                                                                      #
########################################################################
```

### Configure Valkey

Netbox requires a Valkey data-store to work. This playbook supports it, and you can set up a Valkey instance by enabling it on `vars.yml`.

If Netbox is the sole service which requires Valkey on your server, it is fine to set up just a single Valkey instance. However, **it is not recommended if there are other services which require it, because sharing the Valkey instance has security concerns and possibly causes data conflicts**, as described on the [documentation for configuring Valkey](valkey.md). In this case, you should install a dedicated Valkey instance for each of them.

If you are unsure whether you will install other services along with Netbox or you have already set up services which need Valkey, it is recommended to install a Valkey instance dedicated to Netbox. See [below](#setting-up-a-shared-valkey-instance) for an instruction to install a shared instance.

#### Setting up a dedicated Valkey instance

To create a dedicated instance for Netbox, you can follow the steps below:

1. Adjust the `hosts` file
2. Create a new `vars.yml` file for the dedicated instance
3. Edit the existing `vars.yml` file for the main host

##### Adjust `hosts`

At first, you need to adjust `inventory/hosts` file to add a supplementary host for Netbox. See [here](../running-multiple-instances.md#re-do-your-inventory-to-add-supplementary-hosts) for details.

The content should be something like below. Make sure to replace `mash.example.com` with your hostname and `YOUR_SERVER_IP_ADDRESS_HERE` with the IP address of the host, respectively. The same IP address should be set to both, unless the Valkey instance will be served from a different machine.

```ini
[mash_servers]
[mash_servers:children]
mash_example_com

[mash_example_com]
mash.example.com ansible_host=YOUR_SERVER_IP_ADDRESS_HERE
mash.example.com-netbox-deps ansible_host=YOUR_SERVER_IP_ADDRESS_HERE
…
```

`mash_example_com` can be any string and does not have to match with the hostname.

You can just add an entry for the supplementary host to `[mash_example_com]` if there are other entries there already.

##### Create `vars.yml` for the dedicated instance

Then, create a new directory where `vars.yml` for the supplementary host is stored. If `mash.example.com` is your main host, name the directory as `mash.example.com-netbox-deps`. Its path therefore will be `inventory/host_vars/mash.example.com-netbox-deps`.

After creating the directory, add a new `vars.yml` file inside it with a content below. It will have running the playbook create a `mash-netbox-valkey` instance on the new host, setting `/mash/netbox-valkey` to the base directory of the dedicated Valkey instance.

**Notes**:
- As this `vars.yml` file will be used for the new host, make sure to set `mash_playbook_generic_secret_key`. It does not need to be same as the one on `vars.yml` for the main host. Without setting it, the Valkey instance will not be configured.
- Since these variables are used to configure the service name and directory path of the Valkey instance, you do not have to have them matched with the hostname of the server. For example, even if the hostname is `www.example.com`, you do **not** need to set `mash_playbook_service_base_directory_name_prefix` to `www-`. If you are not sure which string you should set, you might as well use the values as they are.

```yaml
---

########################################################################
#                                                                      #
# Playbook                                                             #
#                                                                      #
########################################################################

# Put a strong secret below, generated with `pwgen -s 64 1` or in another way
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

##### Edit the main `vars.yml` file

Having configured `vars.yml` for the dedicated instance, add the following configuration to `vars.yml` for the main host, whose path should be `inventory/host_vars/mash.example.com/vars.yml` (replace `mash.example.com` with yours).

```yaml
########################################################################
#                                                                      #
# netbox                                                               #
#                                                                      #
########################################################################

# Add the base configuration as specified above

# Point NetBox to its dedicated Valkey instance
netbox_environment_variable_redis_host: mash-netbox-valkey
netbox_environment_variable_redis_cache_host: mash-netbox-valkey

# Make sure the NetBox service (mash-netbox.service) starts after its dedicated Valkey service (mash-netbox-valkey.service)
netbox_systemd_required_services_list_custom:
  - "mash-netbox-valkey.service"

# Make sure the NetBox container is connected to the container network of its dedicated Valkey service (mash-netbox-valkey)
netbox_container_additional_networks_custom:
  - "mash-netbox-valkey"

########################################################################
#                                                                      #
# /netbox                                                              #
#                                                                      #
########################################################################
```

Running the installation command will create the dedicated Valkey instance named `mash-netbox-valkey`.

#### Setting up a shared Valkey instance

If you host only Netbox on this server, it is fine to set up a single shared Valkey instance.

To install the single instance and hook Netbox to it, add the following configuration to `inventory/host_vars/mash.example.com/vars.yml`:

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
# netbox                                                               #
#                                                                      #
########################################################################

# Add the base configuration as specified above

# Point NetBox to the shared Valkey instance
netbox_environment_variable_redis_host: "{{ valkey_identifier }}"
netbox_environment_variable_redis_cache_host: "{{ valkey_identifier }}"

# Make sure the NetBox service (mash-netbox.service) starts after the shared Valkey service (mash-valkey.service)
netbox_systemd_required_services_list_custom:
  - "{{ valkey_identifier }}.service"

# Make sure the NetBox container is connected to the container network of the shared Valkey service (mash-valkey)
netbox_container_additional_networks_custom:
  - "{{ valkey_identifier }}"

########################################################################
#                                                                      #
# /netbox                                                              #
#                                                                      #
########################################################################
```

Running the installation command will create the shared Valkey instance named `mash-valkey`.

### Authentication

You can create the "superuser" (if missing) for NetBox upon launch by adding the following configuration to `vars.yml`:

```yaml
netbox_environment_variable_superuser_name: your_username_here
netbox_environment_variable_superuser_email: your.email@example.com

# Put a strong secret below, generated with `pwgen -s 64 1` or in another way.
# Changing the password subsequently will not affect the user's password.
netbox_environment_variable_superuser_password: ''
```

Single-Sign-On is also supported. See below for details.

### Single-Sign-On (SSO) integration

NetBox supports different [Remote Authentication](https://docs.netbox.dev/en/stable/configuration/remote-authentication/) backends, including those provided by the [Python Social Auth](https://python-social-auth.readthedocs.io/) library. This library is included in the NetBox container image by default, so you can invoke any [backend](https://github.com/python-social-auth/social-core/tree/master/social_core/backends) provided by it.

Each module's Python file contains detailed information about how to configure it. It should be noted that module-specific configuration is passed as Python configuration (via `netbox_configuration_extra_python`), and **not as environment variables**.

We have detailed information about integrating with [Keycloak](keycloak.md) below. You can use the configuration in the [Keycloak section](#keycloak) as a template for configuring other backends.

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

If you have decided to install the dedicated Valkey instance for Netbox, make sure to run the [installing](../installing.md) command for the supplementary host (`mash.example.com-netbox-deps`) first, before running it for the main host (`mash.example.com`).

Note that running the `just` commands for installation (`just install-all` or `just setup-all`) automatically takes care of the order. See [here](../running-multiple-instances.md#re-do-your-inventory-to-add-supplementary-hosts) for more details about it.

## Usage

After installation, your Netbox instance becomes available at the URL specified with `netbox_hostname` and `netbox_path_prefix`. With the configuration above, the service is hosted at `https://mash.example.com/netbox`.

You can log in with the **username** (**not** email) and password specified in the `netbox_environment_variable_superuser*` variables.
