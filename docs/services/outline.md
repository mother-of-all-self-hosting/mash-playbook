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

# Outline

The playbook can install and configure [Outline](https://www.getoutline.com/) for you.

Outline is an open-source knowledge base for growing teams.

See the project's [documentation](https://docs.getoutline.com/s/guide) to learn what Outline does and why it might be useful to you.

For details about configuring the [Ansible role for Outline](https://github.com/mother-of-all-self-hosting/ansible-role-outline), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-outline/blob/main/docs/configuring-outline.md) online
- 📁 `roles/galaxy/outline/docs/configuring-outline.md` locally, if you have [fetched the Ansible roles](../installing.md)

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
# outline                                                              #
#                                                                      #
########################################################################

outline_enabled: true

outline_hostname: outline.example.com

########################################################################
#                                                                      #
# /outline                                                             #
#                                                                      #
########################################################################
```

**Note**: hosting Outline under a subpath (by configuring the `outline_path_prefix` variable) does not seem to be possible due to Outline's technical limitations.

### Set random 32-byte hex digits for secret key

You also need to set random **32-byte hex digits** for the secret key. To do so, add the following configuration to your `vars.yml` file. The value can be generated with `openssl rand -hex 32` or in another way.

```yaml
outline_environment_variable_secret_key: YOUR_SECRET_KEY_HERE
```

### Configure authentication methods

For Outline to work, at least one [authentication method](https://docs.getoutline.com/s/hosting/doc/authentication-7ViKRmRY5o) must be enabled. Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-outline/blob/main/docs/configuring-outline.md#configure-authentication-methods) on the role's documentation for details.

### Configure Valkey

Outline requires a Valkey data-store to work. This playbook supports it, and you can set up a Valkey instance by enabling it on `vars.yml`.

If Outline is the sole service which requires Valkey on your server, it is fine to set up just a single Valkey instance. However, **it is not recommended if there are other services which require it, because sharing the Valkey instance has security concerns and possibly causes data conflicts**, as described on the [documentation for configuring Valkey](valkey.md). In this case, you should install a dedicated Valkey instance for each of them.

If you are unsure whether you will install other services along with Outline or you have already set up services which need Valkey (such as [Nextcloud](nextcloud.md), [PeerTube](peertube.md), and [Funkwhale](funkwhale.md)), it is recommended to install a Valkey instance dedicated to Outline.

*See [below](#setting-up-a-shared-valkey-instance) for an instruction to install a shared instance.*

#### Setting up a dedicated Valkey instance

To create a dedicated instance for Outline, you can follow the steps below:

1. Adjust the `hosts` file
2. Create a new `vars.yml` file for the dedicated instance
3. Edit the existing `vars.yml` file for the main host

*Refer to [this page](../running-multiple-instances.md) for details about configuring multiple instances of Valkey on the same server.*

##### Adjust `hosts`

At first, you need to adjust `inventory/hosts` file to add a supplementary host for Outline.

The content should be something like below. Make sure to replace `mash.example.com` with your hostname and `YOUR_SERVER_IP_ADDRESS_HERE` with the IP address of the host, respectively. The same IP address should be set to both, unless the Valkey instance will be served from a different machine.

```ini
[mash_servers]
[mash_servers:children]
mash_example_com

[mash_example_com]
mash.example.com ansible_host=YOUR_SERVER_IP_ADDRESS_HERE
mash.example.com-outline-deps ansible_host=YOUR_SERVER_IP_ADDRESS_HERE
…
```

`mash_example_com` can be any string and does not have to match with the hostname.

You can just add an entry for the supplementary host to `[mash_example_com]` if there are other entries there already.

##### Create `vars.yml` for the dedicated instance

Then, create a new directory where `vars.yml` for the supplementary host is stored. If `mash.example.com` is your main host, name the directory as `mash.example.com-outline-deps`. Its path therefore will be `inventory/host_vars/mash.example.com-outline-deps`.

After creating the directory, add a new `vars.yml` file inside it with a content below. It will have running the playbook create a `mash-outline-valkey` instance on the new host, setting `/mash/outline-valkey` to the base directory of the dedicated Valkey instance.

```yaml
# This is vars.yml for the supplementary host of Outline.

---

########################################################################
#                                                                      #
# Playbook                                                             #
#                                                                      #
########################################################################

# Put a strong secret below, generated with `pwgen -s 64 1` or in another way
mash_playbook_generic_secret_key: ''

# Override service names and directory path prefixes
mash_playbook_service_identifier_prefix: 'mash-outline-'
mash_playbook_service_base_directory_name_prefix: 'outline-'

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
# outline                                                              #
#                                                                      #
########################################################################

# Add the base configuration as specified above

# Make sure the connection via Unix domain socket is enabled
# Set to `false` to enable TCP connection instead
outline_redis_socket_enabled: true

# Connect Outline to its dedicated Valkey instance via the Unix domain socket
#
# Alternatively, if you set `outline_redis_socket_enabled` to `false`,
# - Add the dedicated Valkey instance (mash-outline-valkey) to `outline_redis_hostname`
# - Add its network (mash-outline-valkey) to `outline_container_additional_networks_custom`
outline_redis_socket_path_host: /mash/outline-valkey/run

# Make sure the outline service (mash-outline.service) starts after its dedicated Valkey service (mash-outline-valkey.service)
outline_systemd_required_services_list_custom:
  - "mash-outline-valkey.service"

########################################################################
#                                                                      #
# /outline                                                             #
#                                                                      #
########################################################################
```

Running the installation command will create the dedicated Valkey instance named `mash-outline-valkey`.

#### Setting up a shared Valkey instance

If you host only Outline on this server, it is fine to set up a single shared Valkey instance.

To install the single instance and hook Outline to it, add the following configuration to `inventory/host_vars/mash.example.com/vars.yml`:

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
# outline                                                              #
#                                                                      #
########################################################################

# Add the base configuration as specified above

# Make sure the connection via Unix domain socket is enabled
# Set to `false` to enable TCP connection instead
outline_redis_socket_enabled: true

# Connect Outline to the shared Valkey instance via the Unix domain socket
#
# Alternatively, if you set `outline_redis_socket_enabled` to `false`,
# - Add the shared Valkey instance (mash-valkey) to `outline_redis_hostname`
# - Add its network (mash-valkey) to `outline_container_additional_networks_custom`
outline_redis_socket_path_host: "{{ valkey_run_path }}"

# Make sure the outline API service (mash-outline.service) starts after the shared Valkey service (mash-valkey.service)
outline_systemd_required_services_list_custom:
  - "{{ valkey_identifier }}.service"

########################################################################
#                                                                      #
# /outline                                                             #
#                                                                      #
########################################################################
```

Running the installation command will create the shared Valkey instance named `mash-valkey`.

## Installation

If you have decided to install the dedicated Valkey instance for Outline, make sure to run the [installing](../installing.md) command for the supplementary host (`mash.example.com-outline-deps`) first, before running it for the main host (`mash.example.com`).

Note that running the `just` commands for installation (`just install-all` or `just setup-all`) automatically takes care of the order. See [here](../running-multiple-instances.md#1-adjust-hosts) for more details about it.

## Usage

After running the command for installation, the Outline instance becomes available at the URL specified with `outline_hostname`. With the configuration above, the service is hosted at `https://outline.example.com`.

## Related services

- [BookStack](bookstack.md) — Information organizer and storage
- [Docmost](docmost.md) — Collaborative wiki and documentation software
