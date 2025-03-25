<!--
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Running multiple instances of the same service on the same host

On this playbook, each Ansible role can only be invoked once and made to install one instance of the service it is responsible for. So, if you need multiple instances (of whichever service), you'll need some workarounds.

Let's say you are setting up [PeerTube](services/peertube.md) and [NetBox](services/netbox.md), both of which require a [Valkey](services/valkey.md) instance, on the same host called `mash.example.com`.

If you just add `valkey_enabled: true` to `vars.yml` for `mash.example.com`, a single shared Valkey instance (`mash-valkey`) would be set up. However, it is not recommended because sharing the Valkey instance has security concerns and possibly causes data conflicts. In this case, you should not add `valkey_enabled: true` to `vars.yml` but install dedicated Valkey instances for each of them.

To install those instances, you can follow the steps below:

1. Adjust the `hosts` file
2. Adjust the configuration of the supplementary hosts to use a new "namespace"
3. Edit the `vars.yml` file for the main host

ℹ️ This document takes Valkey as an example, but the same steps can be applied to host multiple instances or whole stacks of any kind.

## 1. Adjust `hosts`

At first, you need to set up your `hosts` file in `inventory` directory as follows, so that hosts for multiple instances of the same service target the same server.

**Notes**:
- Make sure to replace `mash.example.com` with your hostname and `YOUR_SERVER_IP_ADDRESS_HERE` with the IP address of the host, respectively.
- `mash_example_com` can be any string and does not have to match with the hostname of the server.

```ini
[mash_servers]
[mash_servers:children]
mash_example_com

[mash_example_com]
mash.example.com ansible_host=YOUR_SERVER_IP_ADDRESS_HERE
mash.example.com-netbox-deps ansible_host=YOUR_SERVER_IP_ADDRESS_HERE
mash.example.com-peertube-deps ansible_host=YOUR_SERVER_IP_ADDRESS_HERE
```

This creates a new group (called `mash_example_com`) which contains all 3 hosts:

- (**new**) `mash.example.com-netbox-deps` — a new host, for your [NetBox](services/netbox.md) dependencies
- (**new**) `mash.example.com-peertube-deps` — a new host, for your [PeerTube](services/peertube.md) dependencies
- (old) `mash.example.com` — your main inventory host

You can just add a new entry to `[mash_example_com]` in order to have another supplementary host contained in the group.

### Note: use `-l` flag to select a host to run Ansible commands

When running Ansible commands later on, you can use the `-l` flag to limit which host to run them against. Here are a few examples:

- `just install-all` — runs the [installation](installing.md) process on all hosts (3 hosts in this case)
- `just install-all -l mash_example_com` — runs the installation process on all hosts in the `mash_example_com` group (same 3 hosts as `just install-all` in this case)
- `just install-all -l mash.example.com-netbox-deps` — runs the installation process on the `mash.example.com-netbox-deps` host

## 2. Adjust the configuration of the supplementary hosts to use a new "namespace"

Simply targeting the same server with multiple hosts causes conflicts, because services will use the same paths (e.g. `/mash/valkey`) and service/container names (`mash-valkey`) everywhere.

To avoid conflicts, it is necessary to adjust the `vars.yml` file for the new hosts (`mash.example.com-netbox-deps` and `mash.example.com-peertube-deps` in this example) and set non-default and unique values to variables, which are to override service names and directory path prefixes.

First, create new directories where `vars.yml` for the supplementary hosts are stored. Their paths should be `inventory/host_vars/mash.example.com-netbox-deps` and `inventory/host_vars/mash.example.com-peertube-deps`.

Then, create a new `vars.yml` file inside each of them with a content below.

**Notes**:
- As this `vars.yml` file will be used for the new host, make sure to set `mash_playbook_generic_secret_key`. It does not need to be same as the one on `vars.yml` for the main host.
- These variables are not related to the hostname of the server. For example, even if it is `www.example.com`, you do not need to include `www` in either of them. If you are not sure which string you should set, you might as well use the values as they are.

For the supplementary host for NetBox, create `inventory/host_vars/mash.example.com-netbox-deps/vars.yml` with this content.

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

For the supplementary host for PeerTube, create `inventory/host_vars/mash.example.com-peertube-deps/vars.yml` with this content.

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

With these `vars.yml` files, **two** individual Valkey instances will be created:

- `mash-netbox-valkey` with its base data path in `/mash/netbox-valkey`
- `mash-peertube-valkey` with its base data path in `/mash/peertube-valkey`

These instances reuse the `mash` user and group and the `/mash` data path, but are not in conflict with each other.

## 3. Edit `vars.yml` for the main host

Having configured `vars.yml` for Valkey instances for PeerTube and NetBox, add the following configuration to `vars.yml` for the main host (`inventory/host_vars/mash.example.com/vars.yml`):

```yaml
########################################################################
#                                                                      #
# netbox                                                               #
#                                                                      #
########################################################################

# Other NetBox configuration here

# Point NetBox to its dedicated Valkey instance
netbox_environment_variable_redis_host: mash-netbox-valkey
netbox_environment_variable_redis_cache_host: mash-netbox-valkey

# Make sure the NetBox service (mash-netbox.service) starts after its dedicated Valkey service (mash-netbox-valkey.service)
netbox_systemd_required_services_list_custom:
  - mash-netbox-valkey.service

# Make sure the NetBox container is connected to the container network of its dedicated Valkey service (mash-netbox-valkey)
netbox_container_additional_networks_custom:
  - mash-netbox-valkey

########################################################################
#                                                                      #
# /netbox                                                              #
#                                                                      #
########################################################################



########################################################################
#                                                                      #
# peertube                                                             #
#                                                                      #
########################################################################

# Other PeerTube configuration here

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

## Installation

Finally, run the [installation](installing.md) command to create supplementary hosts and wire them to the main host.

> [!WARNING]
> Make sure to run the command for the supplementary hosts first, before running it for the main host. Note that running the `just` command for installation (`just install-all` or `just setup-all`) automatically takes care of starting services in the correct order (thanks to the explicit dependencies defined between them).

## Questions & Answers

**Can't I just use the same Valkey instance for multiple services?**

> You may or you may not. See the [Valkey](services/valkey.md) documentation for why you shouldn't do this.

**Can't I just create one host and a separate stack for each service** (e.g. Nextcloud + all dependencies on one inventory host; PeerTube + all dependencies on another inventory host; with both inventory hosts targetting the same server)?

> That's a possibility which is somewhat clean. The downside is that each "full stack" comes with its own Postgres database which needs to be maintained and upgraded separately.
