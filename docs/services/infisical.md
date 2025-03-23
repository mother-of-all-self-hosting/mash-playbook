<!--
SPDX-FileCopyrightText: 2023 Slavi Pantaleev

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Infisical

[Infisical](https://infisical.com/) is an open-source end-to-end encrypted platform for securely managing secrets and configs across your team, devices, and infrastructure.


## Dependencies

This service requires the following other services:

- a [MongoDB](mongodb.md) document-oriented database server
- a [Traefik](traefik.md) reverse-proxy server
- a [Valkey](valkey.md) data-store, installation details [below](#valkey)


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# infisical                                                            #
#                                                                      #
########################################################################

infisical_enabled: true

infisical_hostname: infisical.example.com

# Generate this with: `openssl rand -hex 16`
infisical_backend_environment_variable_encryption_key: ''

# WARNING: uncomment this after creating your first user account,
# unless you'd like to run a server with public registration enabled.
# infisical_backend_environment_variable_invite_only_signup: true

########################################################################
#                                                                      #
# /infisical                                                           #
#                                                                      #
########################################################################
```


### URL

In the example configuration above, we configure the service to be hosted at `https://infisical.example.com`.

Hosting Infisical under a subpath (by configuring the `infisical_path_prefix` variable) does not seem to be possible right now, due to Infisical limitations.


### Authentication

Public registration can be enabled/disabled using the `infisical_backend_environment_variable_invite_only_signup` variable.

We recommend installing with public registration enabled at first (which is the default value for this variable), creating your first user account, and then disabling public registration by explicitly setting `infisical_backend_environment_variable_invite_only_signup` to `true`. Enabling invite-only signup requires that you configure [Email configuration](#email-configuration)


### Valkey

As described on the Valkey documentation page, if you're hosting additional services which require Valkey on the same server, you'd better go for installing a separate Valkey instance for each service. See Creating a Valkey instance dedicated to Infisical.

If you're only running Infisical on this server and don't need to use Valkey for anything else, you can use a single Valkey instance.
Using the shared Valkey instance for Infisical

To install a single (non-dedicated) Valkey instance (mash-valkey) and hook Infisical to it, add the following additional configuration:

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
# infisical                                                            #
#                                                                      #
########################################################################

# Base configuration as shown above

# Point Infisical to the shared Valkey instance
infisical_environment_variable_redis_host: "{{ valkey_identifier }}"
infisical_environment_variable_redis_cache_host: "{{ valkey_identifier }}"

# Make sure the Infisical service (mash-infisical.service) starts after the shared Valkey service (mash-valkey.service)
infisical_systemd_required_services_list_custom:
  - "{{ valkey_identifier }}.service"

# Make sure the Infisical container is connected to the container network of the shared Valkey service (mash-valkey)
infisical_container_additional_networks_custom:
  - "{{ valkey_identifier }}"

########################################################################
#                                                                      #
# /infisical                                                           #
#                                                                      #
########################################################################
```

This will create a mash-valkey Valkey instance on this host.

This is only recommended if you won't be installing other services which require Valkey. Alternatively, go for Creating a Valkey instance dedicated to Infisical.
Creating a Valkey instance dedicated to Infisical

The following instructions are based on the Running multiple instances of the same service on the same host documentation.

Adjust your inventory/hosts file as described in Re-do your inventory to add supplementary hosts, adding a new supplementary host (e.g. if infisical.example.com is your main one, create infisical.example.com-deps).

Then, create a new vars.yml file for the

inventory/host_vars/infisical.example.com-deps/vars.yml:

```yaml

########################################################################
#                                                                      #
# Playbook                                                             #
#                                                                      #
########################################################################

# Put a strong secret below, generated with `pwgen -s 64 1` or in another way
# Various other secrets will be derived from this secret automatically.
mash_playbook_generic_secret_key: ''

# Override service names and directory path prefixes
mash_playbook_service_identifier_prefix: 'mash-infisical-'
mash_playbook_service_base_directory_name_prefix: 'infisical-'

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

This will create a mash-infisical-valkey instance on this host with its data in /mash/infisical-valkey.

Then, adjust your main inventory host's variables file (inventory/host_vars/infisical.example.com/vars.yml) like this:

########################################################################
#                                                                      #
# infisical                                                            #
#                                                                      #
########################################################################

# Base configuration as shown above


# Point Infisical to its dedicated Valkey instance
infisical_environment_variable_redis_host: mash-infisical-valkey
infisical_environment_variable_redis_cache_host: mash-infisical-valkey

# Make sure the Infisical service (mash-infisical.service) starts after its dedicated Valkey service (mash-infisical-valkey.service)
infisical_systemd_required_services_list_custom:
  - "mash-infisical-valkey.service"

# Make sure the Infisical container is connected to the container network of its dedicated Valkey service (mash-infisical-valkey)
infisical_container_additional_networks_custom:
  - "mash-infisical-valkey"

########################################################################
#                                                                      #
# /infisical                                                           #
#                                                                      #
########################################################################
```

### Email configuration

As described in the Infisical documentation about [Email](https://infisical.com/docs/self-hosting/configuration/email), some important functionality requires email-sending to be configured.

Here are some additional variables you can add to your `vars.yml` file:

```yaml
infisical_backend_environment_variable_smtp_host: smtp.example.com
infisical_backend_environment_variable_smtp_port: 587
infisical_backend_environment_variable_smtp_secure: false

infisical_backend_environment_variable_smtp_username: infisical@example.com
infisical_backend_environment_variable_smtp_password: ''

infisical_backend_environment_variable_smtp_address: infisical@example.com
infisical_backend_environment_variable_smtp_name: Infisical
```

For additional SMTP-related variables, consult the [`defaults/main.yml` file](https://github.com/mother-of-all-self-hosting/ansible-role-infisical/blob/main/defaults/main.yml) in the [ansible-role-infisical](https://github.com/mother-of-all-self-hosting/ansible-role-infisical) Ansible role.


## Usage

After installation, you can go to the Infisical URL, as defined in `infisical_hostname`.

As mentioned in [Authentication](#authentication) above, you can create the first user from the web interface.

If you'd like to prevent other users from registering, consider disabling public registration as described in the [Authentication](#authentication) section and re-running the playbook (`just install-service infisical`).
