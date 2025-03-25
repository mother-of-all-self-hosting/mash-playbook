<!--
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Lago

[Lago](https://www.getlago.com/) is an open-source metering and usage-based billing solution.


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

**Notes**:
- Hosting Lago under a subpath (by configuring the `lago_path_prefix` variable) does not seem to be possible right now, due to Lago limitations.
- Our setup hosts the Lago frontend at the root path (`/`) and the Lago API at the `/api` prefix. This seems to work well, except for [PDF invoices failing due to a Lago bug](https://github.com/getlago/lago/issues/221).

### Configure Valkey

Lago requires a Valkey data-store to work. This playbook supports it, and you can set up a Valkey instance by enabling it on `vars.yml`.

If Lago is the sole service which requires Valkey on your server, it is fine to set up just a single Valkey instance. However, **it is not recommended if there are other services which require it, because sharing the Valkey instance has security concerns and possibly causes data conflicts**, as described on the [documentation for configuring Valkey](valkey.md). In this case, you should install a dedicated Valkey instance for each of them.

If you are unsure whether you will install other services along with Lago or you have already set up services which need Valkey (such as [Nextcloud](nextcloud.md), [PeerTube](peertube.md), and [Funkwhale](funkwhale.md)), it is recommended to install a Valkey instance dedicated to Lago.

*See [below](#setting-up-a-shared-valkey-instance) for an instruction to install a shared instance.*

#### Setting up a dedicated Valkey instance

To create a dedicated instance for Lago, you can follow the steps below:

1. Adjust the `hosts` file
2. Create a new `vars.yml` file for the dedicated instance
3. Edit the existing `vars.yml` file for the main host

*See [this page](../running-multiple-instances.md) for details about configuring multiple instances of Valkey on the same server.*

##### Adjust `hosts`

At first, you need to adjust `inventory/hosts` file to add a supplementary host for Lago.

The content should be something like below. Make sure to replace `mash.example.com` with your hostname and `YOUR_SERVER_IP_ADDRESS_HERE` with the IP address of the host, respectively. The same IP address should be set to both, unless the Valkey instance will be served from a different machine.

```ini
[mash_servers]
[mash_servers:children]
mash_example_com

[mash_example_com]
mash.example.com ansible_host=YOUR_SERVER_IP_ADDRESS_HERE
mash.example.com-lago-deps ansible_host=YOUR_SERVER_IP_ADDRESS_HERE
…
```

`mash_example_com` can be any string and does not have to match with the hostname.

You can just add an entry for the supplementary host to `[mash_example_com]` if there are other entries there already.

##### Create `vars.yml` for the dedicated instance

Then, create a new directory where `vars.yml` for the supplementary host is stored. If `mash.example.com` is your main host, name the directory as `mash.example.com-lago-deps`. Its path therefore will be `inventory/host_vars/mash.example.com-lago-deps`.

After creating the directory, add a new `vars.yml` file inside it with a content below. It will have running the playbook create a `mash-lago-valkey` instance on the new host, setting `/mash/lago-valkey` to the base directory of the dedicated Valkey instance.

```yaml
# This is vars.yml for the supplementary host of Lago.

---

########################################################################
#                                                                      #
# Playbook                                                             #
#                                                                      #
########################################################################

# Put a strong secret below, generated with `pwgen -s 64 1` or in another way
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

##### Edit the main `vars.yml` file

Having configured `vars.yml` for the dedicated instance, add the following configuration to `vars.yml` for the main host, whose path should be `inventory/host_vars/mash.example.com/vars.yml` (replace `mash.example.com` with yours).

```yaml
########################################################################
#                                                                      #
# lago                                                                 #
#                                                                      #
########################################################################

# Add the base configuration as specified above

# Point Lago to its dedicated Valkey instance
lago_redis_hostname: mash-lago-valkey

# Make sure the Lago service (mash-lago.service) starts after its dedicated Valkey service (mash-lago-valkey.service)
lago_api_systemd_required_services_list_custom:
  - "mash-lago-valkey.service"

# Make sure the Lago container is connected to the container network of its dedicated Valkey service (mash-lago-valkey)
lago_api_container_additional_networks_custom:
  - "mash-lago-valkey"

########################################################################
#                                                                      #
# /lago                                                                #
#                                                                      #
########################################################################
```

Running the installation command will create the dedicated Valkey instance named `mash-lago-valkey`.

#### Setting up a shared Valkey instance

If you host only Lago on this server, it is fine to set up a single shared Valkey instance.

To install the single instance and hook Lago to it, add the following configuration to `inventory/host_vars/mash.example.com/vars.yml`:

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

# Add the base configuration as specified above

# Point Lago to the shared Valkey instance
lago_redis_hostname: "{{ valkey_identifier }}"

# Make sure the Lago service (mash-lago.service) starts after the shared Valkey service (mash-valkey.service)
lago_api_systemd_required_services_list_custom:
  - "{{ valkey_identifier }}.service"

# Make sure the Lago container is connected to the container network of the shared Valkey service (mash-valkey)
lago_api_container_additional_networks_custom:
  - "{{ valkey_identifier }}"

########################################################################
#                                                                      #
# /lago                                                                #
#                                                                      #
########################################################################
```

Running the installation command will create the shared Valkey instance named `mash-valkey`.

### Configure authentication

By default, the Lago instance allows anyone to sign up from the web interface.

We recommend installing with registration open to public at first to create your first user. After creating the user, you can disable public registration by adding the following configuration to `vars.yml`:

```yaml
lago_front_environment_variable_lago_disable_signup: true
```

## Installation

If you have decided to install the dedicated Valkey instance for Lago, make sure to run the [installing](../installing.md) command for the supplementary host (`mash.example.com-lago-deps`) first, before running it for the main host (`mash.example.com`).

Note that running the `just` commands for installation (`just install-all` or `just setup-all`) automatically takes care of the order. See [here](../running-multiple-instances.md#1-adjust-hosts) for more details about it.

## Usage

After installation, your Lago instance becomes available at the URL specified with `lago_hostname`.

To log in to the service and get started, you need to create a user from the web interface.

After creating the first user, you can prevent others from registering by making registration closed. To do so, configure [authentication](#configure-authentication) and re-run the playbook: `just install-service lago`
