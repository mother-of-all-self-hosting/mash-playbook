<!--
SPDX-FileCopyrightText: 2020 Aaron Raimist
SPDX-FileCopyrightText: 2020 Chris van Dijk
SPDX-FileCopyrightText: 2020 Dominik Zajac
SPDX-FileCopyrightText: 2020 Mickaël Cornière
SPDX-FileCopyrightText: 2020-2024 MDAD project contributors
SPDX-FileCopyrightText: 2020-2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2022 François Darveau
SPDX-FileCopyrightText: 2022 Julian Foad
SPDX-FileCopyrightText: 2022 Warren Bailey
SPDX-FileCopyrightText: 2023 Antonis Christofides
SPDX-FileCopyrightText: 2023 Felix Stupp
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 Thomas Miceli
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Svix

The playbook can install and configure [Svix](https://github.com/svix/svix-webhooks) for you.

Svix is a webhook service.

See the project's [documentation](https://docs.svix.com/) to learn what Svix does and why it might be useful to you.

For details about configuring the [Ansible role for Svix](https://radicle.network/nodes/iris.radicle.network/rad%3Az23UDsbsiGGq9B8M8TSNWB4MLk3vX), you can check them via:

- 🌐 [the role's documentation](https://radicle.network/nodes/iris.radicle.network/rad%3Az23UDsbsiGGq9B8M8TSNWB4MLk3vX/tree/docs/configuring-svix-server.md) online
- 📁 `roles/galaxy/svix/docs/configuring-svix-server.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server
- [Postgres](postgres.md) database
- (optional) [Valkey](valkey.md) data-store; see [below](#configuring-valkey-optional) for details about installation

## Configuration

To enable this service, add the following configuration to your `vars.yml` file:

```yaml
########################################################################
#                                                                      #
# svix_server                                                          #
#                                                                      #
########################################################################

svix_server_enabled: true

svix_server_hostname: svix.example.com

########################################################################
#                                                                      #
# /svix_server                                                         #
#                                                                      #
########################################################################
```

### Configuring Valkey (optional)

Valkey can optionally be enabled for caching data. This playbook supports it, and you can set up a Valkey instance by enabling it on `vars.yml`.

If Svix is the sole service which requires Valkey on your server, it is fine to set up just a single Valkey instance. However, **it is not recommended if there are other services which require it, because sharing the Valkey instance has security concerns and possibly causes data conflicts**, as described on the [documentation for configuring Valkey](valkey.md). In this case, you should install a dedicated Valkey instance for each of them.

If you are unsure whether you will install other services along with Svix or you have already set up services which need Valkey (such as [PeerTube](peertube.md), [Funkwhale](funkwhale.md), and [Docmost](docmost.md)), it is recommended to install a Valkey instance dedicated to Svix.

*See [below](#setting-up-a-shared-valkey-instance) for an instruction to install a shared instance.*

#### Setting up a dedicated Valkey instance

To create a dedicated instance for Svix, you can follow the steps below:

1. Adjust the `hosts` file
2. Create a new `vars.yml` file for the dedicated instance
3. Edit the existing `vars.yml` file for the main host

*See [this page](../running-multiple-instances.md) for details about configuring multiple instances of Valkey on the same server.*

##### Adjust `hosts`

At first, you need to adjust `inventory/hosts` file to add a supplementary host for Svix.

The content should be something like below. Make sure to replace `mash.example.com` with your hostname and `YOUR_SERVER_IP_ADDRESS_HERE` with the IP address of the host, respectively. The same IP address should be set to both, unless the Valkey instance will be served from a different machine.

```ini
[mash_servers]
[mash_servers:children]
mash_example_com

[mash_example_com]
mash.example.com ansible_host=YOUR_SERVER_IP_ADDRESS_HERE
mash.example.com-svix-deps ansible_host=YOUR_SERVER_IP_ADDRESS_HERE
…
```

`mash_example_com` can be any string and does not have to match with the hostname.

You can just add an entry for the supplementary host to `[mash_example_com]` if there are other entries there already.

##### Create `vars.yml` for the dedicated instance

Then, create a new directory where `vars.yml` for the supplementary host is stored. If `mash.example.com` is your main host, name the directory as `mash.example.com-svix-deps`. Its path therefore will be `inventory/host_vars/mash.example.com-svix-deps`.

After creating the directory, add a new `vars.yml` file inside it with a content below. It will have running the playbook create a `mash-svix-valkey` instance on the new host, setting `/mash/svix-valkey` to the base directory of the dedicated Valkey instance.

```yaml
# This is vars.yml for the supplementary host of Svix.

---

########################################################################
#                                                                      #
# Playbook                                                             #
#                                                                      #
########################################################################

# Put a strong secret below, generated with `pwgen -s 64 1` or in another way
mash_playbook_generic_secret_key: ''

# Override service names and directory path prefixes
mash_playbook_service_identifier_prefix: 'mash-svix-'
mash_playbook_service_base_directory_name_prefix: 'svix-'

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
# svix_server                                                          #
#                                                                      #
########################################################################

# Add the base configuration as specified above

# Point Svix to its dedicated Valkey instance
svix_server_redis_hostname: mash-svix-valkey

# Make sure the Svix container is connected to the container network of its dedicated Valkey service (mash-svix-valkey)
svix_server_container_additional_networks_custom:
  - "mash-svix-valkey"

# Make sure the Svix service (mash-svix.service) starts after its dedicated Valkey service (mash-svix-valkey.service)
svix_server_systemd_required_services_list_custom:
  - "mash-svix-valkey.service"

########################################################################
#                                                                      #
# /svix_server                                                         #
#                                                                      #
########################################################################
```

Running the installation command will create the dedicated Valkey instance named `mash-svix-valkey`.

#### Setting up a shared Valkey instance

If you host only Svix on this server, it is fine to set up a single shared Valkey instance.

To install the single instance and hook Svix to it, add the following configuration to `inventory/host_vars/mash.example.com/vars.yml`:

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
# svix_server                                                          #
#                                                                      #
########################################################################

# Add the base configuration as specified above

# Point Svix to the shared Valkey instance
svix_server_redis_hostname: "{{ valkey_identifier }}"

# Make sure the Svix container is connected to the container network of the shared Valkey service (mash-valkey)
svix_server_container_additional_networks_custom:
  - "{{ valkey_identifier }}"

# Make sure the Svix service (mash-svix.service) starts after the shared Valkey service (mash-valkey.service)
svix_server_systemd_required_services_list_custom:
  - "{{ valkey_identifier }}.service"

########################################################################
#                                                                      #
# /svix_server                                                         #
#                                                                      #
########################################################################
```

Running the installation command will create the shared Valkey instance named `mash-valkey`.

## Installation

If you have decided to install the dedicated Valkey instance for Svix, make sure to run the [installing](../installing.md) command for the supplementary host (`mash.example.com-svix-deps`) first, before running it for the main host (`mash.example.com`).

Note that running the `just` commands for installation (`just install-all` or `just setup-all`) automatically takes care of the order. See [here](../running-multiple-instances.md#1-adjust-hosts) for more details about it.

## Usage

After running the command for installation, the Svix instance becomes available at the URL specified with `svix_server_hostname`. With the configuration above, the service is hosted at `https://svix.example.com`.

## Troubleshooting

See [this section](https://radicle.network/nodes/iris.radicle.network/rad%3Az23UDsbsiGGq9B8M8TSNWB4MLk3vX/tree/docs/configuring-svix-server.md#troubleshooting) on the role's documentation for details.
