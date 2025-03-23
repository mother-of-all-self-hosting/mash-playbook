<!--
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Authentik

[authentik](https://goauthentik.io/) is an open-source Identity Provider focused on flexibility and versatility. MASH can install authentik with the [`mother-of-all-self-hosting/ansible-role-authentik`](https://github.com/mother-of-all-self-hosting/ansible-role-authentik) ansible role.


> [!WARNING]
> SSO is pretty complex and while this role will install authentik for you we only tested OIDC and OAUTH integration. There is a high probability that using outposts/LDAP would need further configuration efforts. Make sure you test before using this in production and feel free to provide feedback!

## Dependencies

This service requires the following other services:

- a [Postgres](postgres.md) database
- a [Valkey](valkey.md) data-store; see [below](#configure-valkey) for details about installation
- a [Traefik](traefik.md) reverse-proxy server


## Configuration

To enable this service, add the following configuration to your `vars.yml` file:

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

### Configure Valkey

Funkwhale requires a Valkey data-store to work. This playbook supports it, and you can set up a Valkey instance by enabling it on `vars.yml`.

If Funkwhale is the sole service which requires Valkey on your server, it is fine to set up just a single Valkey instance. However, **it is not recommended if there are other services which require it, because sharing the Valkey instance has security concerns and possibly causes data conflicts**, as described on the [documentation for configuring Valkey](valkey.md). In this case, you should install a dedicated Valkey instance for each of them.

If you are unsure whether you will install other services along with Funkwhale or you have already set up services which need Valkey, it is recommended to install a Valkey instance dedicated to Funkwhale. See [below](#setting-up-a-shared-valkey-instance) for an instruction to install a shared instance.

#### Setting up a shared Valkey instance

If you host only Funkwhale on this server, it is fine to set up a single shared Valkey instance.

To install the single instance and hook Funkwhale to it, add the following configuration to `inventory/host_vars/mash.example.com/vars.yml`:

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

# Add the base configuration as specified above

# Point authentik to the shared Valkey instance
authentik_config_redis_hostname: "{{ valkey_identifier }}"

# Make sure the authentik service (mash-authentik.service) starts after the shared Valkey service (mash-valkey.service)
authentik_systemd_required_services_list_custom:
  - "{{ valkey_identifier }}.service"

# Make sure the authentik container is connected to the container network of the shared Valkey service (mash-valkey)
authentik_container_additional_networks_custom:
  - "{{ valkey_identifier }}"

########################################################################
#                                                                      #
# /authentik                                                           #
#                                                                      #
########################################################################
```

Running the installation command will create the shared Valkey instance named `mash-valkey`.

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
