<!--
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Notfellchen

[Notfellchen](https://codeberg.org/moanos/notfellchen) is a self-hosted tool to list animals available for adoption to increase their chance of finding a forever-home.


> [!WARNING]
> This service is a custom solution. Feel free to use it but don't expect a solution that works for every use case. Issues with this should be filed in the [project itself](https://codeberg.org/moanos/notfellchen).

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
# notfellchen                                                          #
#                                                                      #
########################################################################

notfellchen_enabled: true
notfellchen_hostname: notfellchen.example.com

########################################################################
#                                                                      #
# /notfellchen                                                         #
#                                                                      #
########################################################################
```

### Configure Valkey

Notfellchen requires a Valkey data-store to work. This playbook supports it, and you can set up a Valkey instance by enabling it on `vars.yml`.

If Notfellchen is the sole service which requires Valkey on your server, it is fine to set up just a single Valkey instance. However, **it is not recommended if there are other services which require it, because sharing the Valkey instance has security concerns and possibly causes data conflicts**, as described on the [documentation for configuring Valkey](valkey.md). In this case, you should install a dedicated Valkey instance for each of them.

If you are unsure whether you will install other services along with Notfellchen or you have already set up services which need Valkey (such as [Nextcloud](nextcloud.md), [PeerTube](peertube.md), and [Funkwhale](funkwhale.md)), it is recommended to install a Valkey instance dedicated to Notfellchen.

*See [below](#setting-up-a-shared-valkey-instance) for an instruction to install a shared instance.*

#### Setting up a dedicated Valkey instance

To create a dedicated instance for Notfellchen, you can follow the steps below:

1. Adjust the `hosts` file
2. Create a new `vars.yml` file for the dedicated instance
3. Edit the existing `vars.yml` file for the main host

*See [this page](../running-multiple-instances.md) for details about configuring multiple instances of Valkey on the same server.*

##### Adjust `hosts`

At first, you need to adjust `inventory/hosts` file to add a supplementary host for Notfellchen.

The content should be something like below. Make sure to replace `mash.example.com` with your hostname and `YOUR_SERVER_IP_ADDRESS_HERE` with the IP address of the host, respectively. The same IP address should be set to both, unless the Valkey instance will be served from a different machine.

```ini
[mash_servers]
[mash_servers:children]
mash_example_com

[mash_example_com]
mash.example.com ansible_host=YOUR_SERVER_IP_ADDRESS_HERE
mash.example.com-notfellchen-deps ansible_host=YOUR_SERVER_IP_ADDRESS_HERE
…
```

`mash_example_com` can be any string and does not have to match with the hostname.

You can just add an entry for the supplementary host to `[mash_example_com]` if there are other entries there already.

##### Create `vars.yml` for the dedicated instance

Then, create a new directory where `vars.yml` for the supplementary host is stored. If `mash.example.com` is your main host, name the directory as `mash.example.com-notfellchen-deps`. Its path therefore will be `inventory/host_vars/mash.example.com-notfellchen-deps`.

After creating the directory, add a new `vars.yml` file inside it with a content below. It will have running the playbook create a `mash-notfellchen-valkey` instance on the new host, setting `/mash/notfellchen-valkey` to the base directory of the dedicated Valkey instance.

```yaml
# This is vars.yml for the supplementary host of Notfellchen.

---

########################################################################
#                                                                      #
# Playbook                                                             #
#                                                                      #
########################################################################

# Put a strong secret below, generated with `pwgen -s 64 1` or in another way
mash_playbook_generic_secret_key: ''

# Override service names and directory path prefixes
mash_playbook_service_identifier_prefix: 'mash-notfellchen-'
mash_playbook_service_base_directory_name_prefix: 'notfellchen-'

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
# notfellchen                                                          #
#                                                                      #
########################################################################

# Add the base configuration as specified above

# Point notfellchen to its dedicated Valkey instance
notfellchen_config_redis_hostname: mash-notfellchen-valkey

# Make sure the notfellchen ervice (mash-notfellchen.service) starts after its dedicated Valkey service
notfellchen_systemd_required_services_list_custom:
  - "mash-notfellchen-valkey.service"

# Make sure the notfellchen service (mash-notfellchen.service) is connected to the container network of its dedicated Valkey service
notfellchen_api_container_additional_networks_custom:
  - "mash-notfellchen-valkey"

########################################################################
#                                                                      #
# /notfellchen                                                         #
#                                                                      #
########################################################################
```

Running the installation command will create the dedicated Valkey instance named `mash-notfellchen-valkey`.

#### Setting up a shared Valkey instance

If you host only Notfellchen on this server, it is fine to set up a single shared Valkey instance.

To install the single instance and hook Notfellchen to it, add the following configuration to `inventory/host_vars/mash.example.com/vars.yml`:

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
# notfellchen                                                          #
#                                                                      #
########################################################################

# Add the base configuration as specified above

# Point notfellchen to the shared Valkey instance
notfellchen_config_redis_hostname: "{{ valkey_identifier }}"

# Make sure the notfellchen API service (mash-notfellchen.service) starts after the shared Valkey service
notfellchen_api_systemd_required_services_list_custom:
  - "{{ valkey_identifier }}.service"

# Make sure the notfellchen API service (mash-notfellchen.service) is connected to the container network of the shared Valkey service
notfellchen_container_additional_networks_custom:
  - "{{ valkey_container_network }}"

########################################################################
#                                                                      #
# /notfellchen                                                         #
#                                                                      #
########################################################################
```

Running the installation command will create the shared Valkey instance named `mash-valkey`.

## Installation

If you have decided to install the dedicated Valkey instance for Notfellchen, make sure to run the [installing](../installing.md) command for the supplementary host (`mash.example.com-notfellchen-deps`) first, before running it for the main host (`mash.example.com`).

Note that running the `just` commands for installation (`just install-all` or `just setup-all`) automatically takes care of the order. See [here](../running-multiple-instances.md#1-adjust-hosts) for more details about it.

## Usage

After installation, your Notfellchen instance becomes available at the URL specified with `notfellchen_hostname`.

To log in to the service and get started, you have to create a user ("superuser") at first. To do so, run the command below after replacing `USERNAME`, `PASSWORD`, and `EMAIL_ADDRESS`:

```bash
just run-tags notfellchen-add-superuser --extra-vars=username=USERNAME --extra-vars=password=PASSWORD --extra-vars=email=EMAIL_ADDRESS
```
