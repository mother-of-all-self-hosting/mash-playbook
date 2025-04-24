<!--
SPDX-FileCopyrightText: 2020 - 2024 MDAD project contributors
SPDX-FileCopyrightText: 2020 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2020 Aaron Raimist
SPDX-FileCopyrightText: 2020 Chris van Dijk
SPDX-FileCopyrightText: 2020 Dominik Zajac
SPDX-FileCopyrightText: 2020 Mickaël Cornière
SPDX-FileCopyrightText: 2022 François Darveau
SPDX-FileCopyrightText: 2022 Julian Foad
SPDX-FileCopyrightText: 2022 Warren Bailey
SPDX-FileCopyrightText: 2023 Antonis Christofides
SPDX-FileCopyrightText: 2023 Felix Stupp
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Ghostfolio

The playbook can install and configure [Ghostfolio](https://ghostfol.io/) for you.

Ghostfolio is a free software for wealth management to keep track of assets such as stocks, bonds, ETFs, etc.

See the project's [documentation](https://ghostfol.io/en/features) to learn what Ghostfolio does and why it might be useful to you.

For details about configuring the [Ansible role for Ghostfolio](https://github.com/mother-of-all-self-hosting/ansible-role-ghostfolio), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-ghostfolio/blob/main/docs/configuring-ghostfolio.md) online
- 📁 `roles/galaxy/ghostfolio/docs/configuring-ghostfolio.md` locally, if you have [fetched the Ansible roles](../installing.md)

>[!NOTE]
> The role is based on Node.js docker image, and is expected to run with uid 1000.

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server
- [Postgres](postgres.md) database
- [Valkey](valkey.md) data-store; see [below](#configure-valkey) for details about installation

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file:

```yaml
########################################################################
#                                                                      #
# ghostfolio                                                           #
#                                                                      #
########################################################################

ghostfolio_enabled: true

ghostfolio_hostname: ghostfolio.example.com

########################################################################
#                                                                      #
# /ghostfolio                                                          #
#                                                                      #
########################################################################
```

**Note**: hosting Ghostfolio under a subpath (by configuring the `ghostfolio_path_prefix` variable) does not seem to be possible due to Ghostfolio's technical limitations.

### Configure Valkey

Ghostfolio requires a Valkey data-store to work. This playbook supports it, and you can set up a Valkey instance by enabling it on `vars.yml`.

If Ghostfolio is the sole service which requires Valkey on your server, it is fine to set up just a single Valkey instance. However, **it is not recommended if there are other services which require it, because sharing the Valkey instance has security concerns and possibly causes data conflicts**, as described on the [documentation for configuring Valkey](valkey.md). In this case, you should install a dedicated Valkey instance for each of them.

If you are unsure whether you will install other services along with Ghostfolio or you have already set up services which need Valkey (such as [Nextcloud](nextcloud.md), [PeerTube](peertube.md), and [Funkwhale](funkwhale.md)), it is recommended to install a Valkey instance dedicated to Ghostfolio.

*See [below](#setting-up-a-shared-valkey-instance) for an instruction to install a shared instance.*

#### Setting up a dedicated Valkey instance

To create a dedicated instance for Ghostfolio, you can follow the steps below:

1. Adjust the `hosts` file
2. Create a new `vars.yml` file for the dedicated instance
3. Edit the existing `vars.yml` file for the main host

*See [this page](../running-multiple-instances.md) for details about configuring multiple instances of Valkey on the same server.*

##### Adjust `hosts`

At first, you need to adjust `inventory/hosts` file to add a supplementary host for Ghostfolio.

The content should be something like below. Make sure to replace `mash.example.com` with your hostname and `YOUR_SERVER_IP_ADDRESS_HERE` with the IP address of the host, respectively. The same IP address should be set to both, unless the Valkey instance will be served from a different machine.

```ini
[mash_servers]
[mash_servers:children]
mash_example_com

[mash_example_com]
mash.example.com ansible_host=YOUR_SERVER_IP_ADDRESS_HERE
mash.example.com-ghostfolio-deps ansible_host=YOUR_SERVER_IP_ADDRESS_HERE
…
```

`mash_example_com` can be any string and does not have to match with the hostname.

You can just add an entry for the supplementary host to `[mash_example_com]` if there are other entries there already.

##### Create `vars.yml` for the dedicated instance

Then, create a new directory where `vars.yml` for the supplementary host is stored. If `mash.example.com` is your main host, name the directory as `mash.example.com-ghostfolio-deps`. Its path therefore will be `inventory/host_vars/mash.example.com-ghostfolio-deps`.

After creating the directory, add a new `vars.yml` file inside it with a content below. It will have running the playbook create a `mash-ghostfolio-valkey` instance on the new host, setting `/mash/ghostfolio-valkey` to the base directory of the dedicated Valkey instance.

```yaml
# This is vars.yml for the supplementary host of Ghostfolio.

---

########################################################################
#                                                                      #
# Playbook                                                             #
#                                                                      #
########################################################################

# Put a strong secret below, generated with `pwgen -s 64 1` or in another way
mash_playbook_generic_secret_key: ''

# Override service names and directory path prefixes
mash_playbook_service_identifier_prefix: 'mash-ghostfolio-'
mash_playbook_service_base_directory_name_prefix: 'ghostfolio-'

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
# ghostfolio                                                           #
#                                                                      #
########################################################################

# Add the base configuration as specified above

# Point Ghostfolio to its dedicated Valkey instance
ghostfolio_config_redis_hostname: mash-ghostfolio-valkey

# Make sure the Ghostfolio service (mash-ghostfolio.service) starts after its dedicated Valkey service (mash-ghostfolio-valkey.service)
ghostfolio_systemd_required_services_list_custom:
  - "mash-ghostfolio-valkey.service"

# Make sure the Ghostfolio service (mash-ghostfolio.service) is connected to the container network of its dedicated Valkey service (mash-ghostfolio-valkey)
ghostfolio_container_additional_networks_custom:
  - "mash-ghostfolio-valkey"

########################################################################
#                                                                      #
# /ghostfolio                                                          #
#                                                                      #
########################################################################
```

Running the installation command will create the dedicated Valkey instance named `mash-ghostfolio-valkey`.

#### Setting up a shared Valkey instance

If you host only Ghostfolio on this server, it is fine to set up a single shared Valkey instance.

To install the single instance and hook Ghostfolio to it, add the following configuration to `inventory/host_vars/mash.example.com/vars.yml`:

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
# ghostfolio                                                           #
#                                                                      #
########################################################################

# Add the base configuration as specified above

# Point Ghostfolio to the shared Valkey instance
ghostfolio_config_redis_hostname: "{{ valkey_identifier }}"

# Make sure the Ghostfolio service (mash-ghostfolio.service) starts after its dedicated Valkey service (mash-ghostfolio-valkey.service)
ghostfolio_systemd_required_services_list_custom:
  - "{{ valkey_identifier }}.service"

# Make sure the Ghostfolio container is connected to the container network of its dedicated Valkey service (mash-ghostfolio-valkey)
ghostfolio_container_additional_networks_custom:
  - "{{ valkey_container_network }}"

########################################################################
#                                                                      #
# /ghostfolio                                                          #
#                                                                      #
########################################################################
```

Running the installation command will create the shared Valkey instance named `mash-valkey`.

### Set Coingecko API keys (optional)

If you have either or both of *CoinGecko* Demo API key and *CoinGecko* Pro API key, you can specify them by adding the following configuration to your `vars.yml` file:

```yaml
ghostfolio_environment_variable_api_key_coingecko_demo: YOUR_DEMO_KEY_HERE
ghostfolio_environment_variable_api_key_coingecko_pro: YOUR_PRO_KEY_HERE
```

## Installation

If you have decided to install the dedicated Valkey instance for Ghostfolio, make sure to run the [installing](../installing.md) command for the supplementary host (`mash.example.com-ghostfolio-deps`) first, before running it for the main host (`mash.example.com`).

Note that running the `just` commands for installation (`just install-all` or `just setup-all`) automatically takes care of the order. See [here](../running-multiple-instances.md#1-adjust-hosts) for more details about it.

## Usage

After installation, your Ghostfolio instance becomes available at the URL specified with `ghostfolio_hostname` like `https://ghostfolio.example.com`. As **registration is open to anyone by default**, you also would probably want to disable the signup form on "Admin Control" page after creating the account.

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-ghostfolio/blob/main/docs/configuring-ghostfolio.md#usage) on the role's documentation for details.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-ghostfolio/blob/main/docs/configuring-ghostfolio.md#troubleshooting) on the role's documentation for details.
