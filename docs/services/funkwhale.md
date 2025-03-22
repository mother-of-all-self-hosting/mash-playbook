<!--
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023-2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Funkwhale

[Funkwhale](https://funkwhale.audio/) is a community-driven project that lets you listen and share music and audio within a decentralized, open network.


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
# funkwhale                                                            #
#                                                                      #
########################################################################

funkwhale_enabled: true

funkwhale_hostname: mash.example.com

# Put a strong secret below, generated with `pwgen -s 64 1` or in another way
funkwhale_django_secret_key: ''

########################################################################
#                                                                      #
# /funkwhale                                                           #
#                                                                      #
########################################################################
```

### Configure Valkey

Funkwhale requires a Valkey data-store to work. This playbook supports it, and you can set up a Valkey instance by enabling it on `vars.yml`.

If Funkwhale is the sole service which requires Valkey on your server, it is fine to set up just a single Valkey instance. However, **it is not recommended if there are other services which require it, because sharing the Valkey instance has security concerns and possibly causes data conflicts**, as described on the [documentation for configuring Valkey](valkey.md). In this case, you should install a dedicated Valkey instance for each of them.

If you are unsure whether you will install other services along with Funkwhale or you have already set up services which need Valkey, it is recommended to install a Valkey instance dedicated to Funkwhale. See [below](#setting-up-a-shared-valkey-instance) for an instruction to install a shared instance.

#### Setting up a dedicated Valkey instance

To create a dedicated instance for Funkwhale, you can follow the steps below:

1. Adjust the `hosts` file
2. Create a new `vars.yml` file for the dedicated instance
3. Edit the existing `vars.yml` file for the main host

##### Adjust `hosts`

At first, you need to adjust `inventory/hosts` file to add a supplementary host for Funkwhale. See [here](../running-multiple-instances.md#re-do-your-inventory-to-add-supplementary-hosts) for details.

The content should be something like below. Make sure to replace `mash.example.com` with your hostname and `YOUR_SERVER_IP_ADDRESS_HERE` with the IP address of the host, respectively. The same IP address should be set to both, unless the Valkey instance will be served from a different machine.

```ini
[mash_servers]
[mash_servers:children]
mash_example_com

[mash_example_com]
mash.example.com ansible_host=YOUR_SERVER_IP_ADDRESS_HERE
mash.example.com-funkwhale-deps ansible_host=YOUR_SERVER_IP_ADDRESS_HERE
…
```

`mash_example_com` can be any string and does not have to match with the hostname.

You can just add an entry for the supplementary host to `[mash_example_com]` if there are other entries there already.

##### Create `vars.yml` for the dedicated instance

Then, create a new directory where `vars.yml` for the supplementary host is stored. If `mash.example.com` is your main host, name the directory as `mash.example.com-funkwhale-deps`. Its path therefore will be `inventory/host_vars/mash.example.com-funkwhale-deps`.

After creating the directory, add a new `vars.yml` file inside it with a content below. It will have running the playbook create a `mash-funkwhale-valkey` instance on the new host, setting `/mash/funkwhale-valkey` to the base directory of the dedicated Valkey instance.

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
mash_playbook_service_identifier_prefix: 'mash-funkwhale-'
mash_playbook_service_base_directory_name_prefix: 'funkwhale-'

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
# funkwhale                                                            #
#                                                                      #
########################################################################

# Add the base configuration as specified above

# Point Funkwhale to its dedicated Valkey instance
funkwhale_config_redis_hostname: mash-funkwhale-valkey

# Make sure the Funkwhale API service (mash-funkwhale-api.service) starts after its dedicated Valkey service
funkwhale_api_systemd_required_services_list_custom:
  - "mash-funkwhale-valkey.service"

# Make sure the Funkwhale API service (mash-funkwhale-api.service) is connected to the container network of its dedicated Valkey service
funkwhale_api_container_additional_networks_custom:
  - "mash-funkwhale-valkey"

########################################################################
#                                                                      #
# /funkwhale                                                           #
#                                                                      #
########################################################################
```

Running the installation command will create the dedicated Valkey instance named `mash-funkwhale-valkey`.

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
# funkwhale                                                            #
#                                                                      #
########################################################################

# Add the base configuration as specified above

# Point Funkwhale to the shared Valkey instance
funkwhale_config_redis_hostname: "{{ valkey_identifier }}"

# Make sure the Funkwhale API service (mash-funkwhale-api.service) starts after the shared Valkey service
funkwhale_api_systemd_required_services_list_custom:
  - "{{ valkey_identifier }}.service"

# Make sure the Funkwhale API service (mash-funkwhale-api.service) is connected to the container network of the shared Valkey service
funkwhale_api_container_additional_networks_custom:
  - "{{ valkey_container_network }}"

########################################################################
#                                                                      #
# /funkwhale                                                           #
#                                                                      #
########################################################################
```

Running the installation command will create the shared Valkey instance named `mash-valkey`.

## Installation

If you have decided to install the dedicated Valkey instance for Funkwhale, make sure to run the [installing](../installing.md) command for the supplementary host (`mash.example.com-funkwhale-deps`) first, before running it for the main host (`mash.example.com`).

Note that running the `just` commands for installation (`just install-all` or `just setup-all`) automatically takes care of the order. See [here](../running-multiple-instances.md#re-do-your-inventory-to-add-supplementary-hosts) for more details about it.

## Usage

After installation, your Funkwhale instance becomes available at the URL specified with `funkwhale_hostname`.

To log in to the service and get started, you have to create a user ("superuser") at first. To do so, run the command below after replacing `USERNAME`, `PASSWORD`, and `EMAIL_ADDRESS`:

```bash
just run-tags funkwhale-add-superuser --extra-vars=username=USERNAME --extra-vars=password=PASSWORD --extra-vars=email=EMAIL_ADDRESS
```

Log in to the web UI with the superuser to create other users.
