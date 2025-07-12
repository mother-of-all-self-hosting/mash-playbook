<!--
SPDX-FileCopyrightText: 2023 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# PeerTube

[PeerTube](https://joinpeertube.org/) is a tool for sharing online videos developed by [Framasoft](https://framasoft.org/), a french non-profit.


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
# peertube                                                             #
#                                                                      #
########################################################################

peertube_enabled: true

peertube_hostname: peertube.example.com

# Put a strong secret below, generated with `pwgen -s 64 1` or in another way
peertube_config_secret: ''

# An email address to be associated with the `root` PeerTube administrator account.
peertube_config_admin_email: ''

# The initial password that the `root` PeerTube administrator account will be created with.
# You can put any string here, but generating a strong one is preferred (e.g. `pwgen -s 64 1`).
peertube_config_root_user_initial_password: ''

########################################################################
#                                                                      #
# /peertube                                                            #
#                                                                      #
########################################################################
```

**Note**: hosting PeerTube under a subpath (by configuring the `peertube_path_prefix` variable) does not seem to be possible right now, due to PeerTube limitations.

### Configure Valkey

PeerTube requires a Valkey data-store to work. This playbook supports it, and you can set up a Valkey instance by enabling it on `vars.yml`.

If PeerTube is the sole service which requires Valkey on your server, it is fine to set up just a single Valkey instance. However, **it is not recommended if there are other services which require it, because sharing the Valkey instance has security concerns and possibly causes data conflicts**, as described on the [documentation for configuring Valkey](valkey.md). In this case, you should install a dedicated Valkey instance for each of them.

If you are unsure whether you will install other services along with PeerTube or you have already set up services which need Valkey (such as [Nextcloud](nextcloud.md), [Funkwhale](funkwhale.md), and [SearXNG](searxng.md)), it is recommended to install a Valkey instance dedicated to PeerTube.

*See [below](#setting-up-a-shared-valkey-instance) for an instruction to install a shared instance.*

#### Setting up a dedicated Valkey instance

To create a dedicated instance for PeerTube, you can follow the steps below:

1. Adjust the `hosts` file
2. Create a new `vars.yml` file for the dedicated instance
3. Edit the existing `vars.yml` file for the main host

*See [this page](../running-multiple-instances.md) for details about configuring multiple instances of Valkey on the same server.*

##### Adjust `hosts`

At first, you need to adjust `inventory/hosts` file to add a supplementary host for PeerTube.

The content should be something like below. Make sure to replace `mash.example.com` with your hostname and `YOUR_SERVER_IP_ADDRESS_HERE` with the IP address of the host, respectively. The same IP address should be set to both, unless the Valkey instance will be served from a different machine.

```ini
[mash_servers]
[mash_servers:children]
mash_example_com

[mash_example_com]
mash.example.com ansible_host=YOUR_SERVER_IP_ADDRESS_HERE
mash.example.com-peertube-deps ansible_host=YOUR_SERVER_IP_ADDRESS_HERE
…
```

`mash_example_com` can be any string and does not have to match with the hostname.

You can just add an entry for the supplementary host to `[mash_example_com]` if there are other entries there already.

##### Create `vars.yml` for the dedicated instance

Then, create a new directory where `vars.yml` for the supplementary host is stored. If `mash.example.com` is your main host, name the directory as `mash.example.com-peertube-deps`. Its path therefore will be `inventory/host_vars/mash.example.com-peertube-deps`.

After creating the directory, add a new `vars.yml` file inside it with a content below. It will have running the playbook create a `mash-peertube-valkey` instance on the new host, setting `/mash/peertube-valkey` to the base directory of the dedicated Valkey instance.

```yaml
# This is vars.yml for the supplementary host of PeerTube.

---

########################################################################
#                                                                      #
# Playbook                                                             #
#                                                                      #
########################################################################

# Put a strong secret below, generated with `pwgen -s 64 1` or in another way
mash_playbook_generic_secret_key: ''

# Override service names and directory path prefixes
mash_playbook_service_identifier_prefix: 'mash-peertube-'
mash_playbook_service_base_directory_name_prefix: 'peertube-'

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
# peertube                                                             #
#                                                                      #
########################################################################

# Add the base configuration as specified above

# Point PeerTube to its dedicated Valkey instance
peertube_config_redis_hostname: mash-peertube-valkey

# Make sure the PeerTube service (mash-peertube.service) starts after its dedicated Valkey service (mash-peertube-valkey.service)
peertube_systemd_required_services_list_custom:
  - "mash-peertube-valkey.service"

# Make sure the PeerTube container is connected to the container network of its dedicated Valkey service (mash-peertube-valkey)
peertube_container_additional_networks_custom:
  - "mash-peertube-valkey"

########################################################################
#                                                                      #
# /peertube                                                            #
#                                                                      #
########################################################################
```

Running the installation command will create the dedicated Valkey instance named `mash-peertube-valkey`.

#### Setting up a shared Valkey instance

If you host only PeerTube on this server, it is fine to set up a single shared Valkey instance.

To install the single instance and hook PeerTube to it, add the following configuration to `inventory/host_vars/mash.example.com/vars.yml`:

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
# peertube                                                             #
#                                                                      #
########################################################################

# Add the base configuration as specified above

# Point PeerTube to the shared Valkey instance
peertube_config_redis_hostname: "{{ valkey_identifier }}"

# Make sure the PeerTube service (mash-peertube.service) starts after the shared Valkey service (mash-valkey.service)
peertube_systemd_required_services_list_custom:
  - "{{ valkey_identifier }}.service"

# Make sure the PeerTube container is connected to the container network of the shared Valkey service (mash-valkey)
peertube_container_additional_networks_custom:
  - "{{ valkey_identifier }}"

########################################################################
#                                                                      #
# /peertube                                                            #
#                                                                      #
########################################################################
```

Running the installation command will create the shared Valkey instance named `mash-valkey`.

## Installation

If you have decided to install the dedicated Valkey instance for PeerTube, make sure to run the [installing](../installing.md) command for the supplementary host (`mash.example.com-peertube-deps`) first, before running it for the main host (`mash.example.com`).

Note that running the `just` commands for installation (`just install-all` or `just setup-all`) automatically takes care of the order. See [here](../running-multiple-instances.md#1-adjust-hosts) for more details about it.

### Adjust Traefik network's IP address range

After completing the initial installation, it is necessary to adjust the Traefik network's IP address range.

First, find the `traefik` network's IP address range by running the following command on the server: `docker network inspect traefik -f "{{ (index .IPAM.Config 0).Subnet }}"`

Then, add the following configuration after replacing the example IP range below, and re-run the playbook.

```yaml
peertube_trusted_proxies_values_custom: ["172.21.0.0/16"]
```

## Usage

After installation, your PeerTube instance becomes available at the URL specified with `peertube_hostname` and `peertube_path_prefix`.

You should then be able to log in with:

- username: `root`
- password: the password you've set in `peertube_config_root_user_initial_password` in `vars.yml`
