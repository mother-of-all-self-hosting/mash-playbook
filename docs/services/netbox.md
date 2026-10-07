<!--
SPDX-FileCopyrightText: 2023, 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2025, 2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# NetBox

The playbook can install and configure [NetBox](https://docs.netbox.dev/en/stable/) for you.

NetBox is an open-source web application that provides [IP address management (IPAM)](https://en.wikipedia.org/wiki/IP_address_management) and [data center infrastructure management (DCIM)](https://en.wikipedia.org/wiki/Data_center_management#Data_center_infrastructure_management) functionality.

See the project's [documentation](https://docs.netbox.dev/en/stable/) to learn what NetBox does and why it might be useful to you.

For details about configuring the [Ansible role for NetBox](https://github.com/mother-of-all-self-hosting/ansible-role-netbox), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-netbox/blob/main/docs/configuring-netbox.md) online
- 📁 `roles/galaxy/netbox/docs/configuring-netbox.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Postgres](postgres.md) database
- [Traefik](traefik.md) reverse-proxy server
- [Valkey](valkey.md) data-store; see [below](#configure-valkey) for details about installation

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

########################################################################
#                                                                      #
# /netbox                                                              #
#                                                                      #
########################################################################
```

### Configure Valkey

Netbox requires a Valkey data-store to work. This playbook supports it, and you can set up a Valkey instance by enabling it on `vars.yml`.

If Netbox is the sole service which requires Valkey on your server, it is fine to set up just a single Valkey instance. However, **it is not recommended if there are other services which require it, because sharing the Valkey instance has security concerns and possibly causes data conflicts**, as described on the [documentation for configuring Valkey](valkey.md). In this case, you should install a dedicated Valkey instance for each of them.

If you are unsure whether you will install other services along with Netbox or you have already set up services which need Valkey (such as [Nextcloud](nextcloud.md), [PeerTube](peertube.md), and [Funkwhale](funkwhale.md)), it is recommended to install a Valkey instance dedicated to Netbox.

*See [below](#setting-up-a-shared-valkey-instance) for an instruction to install a shared instance.*

#### Setting up a dedicated Valkey instance

To create a dedicated instance for Netbox, you can follow the steps below:

1. Adjust the `hosts` file
2. Create a new `vars.yml` file for the dedicated instance
3. Edit the existing `vars.yml` file for the main host

*Refer to [this page](../running-multiple-instances.md) for details about configuring multiple instances of Valkey on the same server.*

##### Adjust `hosts`

At first, you need to adjust `inventory/hosts` file to add a supplementary host for Netbox.

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

```yaml
# This is vars.yml for the supplementary host of NetBox.

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
netbox_redis_hostname: mash-netbox-valkey
netbox_environment_variable_redis_cache_hostname: mash-netbox-valkey

# Make sure the NetBox container is connected to the container network of its dedicated Valkey service (mash-netbox-valkey)
netbox_container_additional_networks_custom:
  - "mash-netbox-valkey"

# Make sure the NetBox service (mash-netbox.service) starts after its dedicated Valkey service (mash-netbox-valkey.service)
netbox_systemd_required_services_list_custom:
  - "mash-netbox-valkey.service"

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
netbox_redis_hostname: "{{ valkey_identifier }}"
netbox_environment_variable_redis_cache_hostname: "{{ valkey_identifier }}"

# Make sure the NetBox container is connected to the container network of the shared Valkey service (mash-valkey)
netbox_container_additional_networks_custom:
  - "{{ valkey_identifier }}"

# Make sure the NetBox service (mash-netbox.service) starts after the shared Valkey service (mash-valkey.service)
netbox_systemd_required_services_list_custom:
  - "{{ valkey_identifier }}.service"

########################################################################
#                                                                      #
# /netbox                                                              #
#                                                                      #
########################################################################
```

Running the installation command will create the shared Valkey instance named `mash-valkey`.

## Installation

If you have decided to install the dedicated Valkey instance for Netbox, make sure to run the [installing](../installing.md) command for the supplementary host (`mash.example.com-netbox-deps`) first, before running it for the main host (`mash.example.com`).

Note that running the `just` commands for installation (`just install-all` or `just setup-all`) automatically takes care of the order. See [here](../running-multiple-instances.md#1-adjust-hosts) for more details about it.

## Usage

After running the command for installation, the Netbox instance becomes available at the URL specified with `netbox_hostname` and `netbox_path_prefix`. With the configuration above, the service is hosted at `https://mash.example.com/netbox`.
