<!--
SPDX-FileCopyrightText: 2026 Robin Miller

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# LiteLLM

The playbook can install and configure [LiteLLM](https://github.com/BerriAI/litellm) for you.

LiteLLM is a simple service for aggregating and managing LLM inference providers.

See the project's [documentation](https://github.com/BerriAI/litellm/blob/master/README.md) to learn what LiteLLM does and why it might be useful to you.

For details about configuring the [Ansible role for LiteLLM](https://forgejo.littlecedar.net/grenewode/ansible-role-mash-litellm), you can check them via:

- 🌐 [the role's documentation](https://forgejo.littlecedar.net/grenewode/ansible-role-mash-litellm/src/branch/main/docs/configuring-litellm.md) online
- 📁 `roles/galaxy/litellm/docs/configuring-litellm.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server
- (optional) [Postgres](postgres.md) database — LiteLLM connects to it automatically if it is enabled
- (optional) [Valkey](valkey.md) data-store; see [below](#configuring-valkey-optional) for details about installation

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# litellm                                                              #
#                                                                      #
########################################################################

litellm_enabled: true

litellm_hostname: litellm.example.com

# Put a strong secret below, generated with `pwgen -s 64 1` or in another way.
# litellm_master_key must start with 'sk-'.
litellm_master_key: ''
litellm_salt_key: ''

########################################################################
#                                                                      #
# /litellm                                                             #
#                                                                      #
########################################################################
```

**Note**: hosting LiteLLM under a subpath (by configuring the `litellm_path_prefix` variable) is not possible due to LiteLLM's limitations.

### Configuring Valkey (optional)

LiteLLM uses caching to avoid repeating expensive operations. It can also store models in a [Postgres](postgres.md) database. This playbook supports enabling caching with a Valkey data-store, and you can set up a Valkey instance by enabling it on `vars.yml`.

If LiteLLM is the sole service which requires Valkey on your server, it is fine to set up just a single Valkey instance. However, **it is not recommended if there are other services which require it, because sharing the Valkey instance has security concerns and possibly causes data conflicts**, as described on the [documentation for configuring Valkey](valkey.md). In this case, you should install a dedicated Valkey instance for each of them.

If you are unsure whether you will install other services along with LiteLLM or you have already set up services which need Valkey (such as [Nextcloud](nextcloud.md), [PeerTube](peertube.md), and [Funkwhale](funkwhale.md)), it is recommended to install a Valkey instance dedicated to LiteLLM.

*See [below](#setting-up-a-shared-valkey-instance) for an instruction to install a shared instance.*

#### Setting up a dedicated Valkey instance

To create a dedicated instance for LiteLLM, you can follow the steps below:

1. Adjust the `hosts` file
2. Create a new `vars.yml` file for the dedicated instance
3. Edit the existing `vars.yml` file for the main host

*See [this page](../running-multiple-instances.md) for details about configuring multiple instances of Valkey on the same server.*

##### Adjust `hosts`

At first, you need to adjust `inventory/hosts` file to add a supplementary host for LiteLLM.

The content should be something like below. Make sure to replace `mash.example.com` with your hostname and `YOUR_SERVER_IP_ADDRESS_HERE` with the IP address of the host, respectively. The same IP address should be set to both, unless the Valkey instance will be served from a different machine.

```ini
[mash_servers]
[mash_servers:children]
mash_example_com

[mash_example_com]
mash.example.com ansible_host=YOUR_SERVER_IP_ADDRESS_HERE
mash.example.com-litellm-deps ansible_host=YOUR_SERVER_IP_ADDRESS_HERE
…
```

`mash_example_com` can be any string and does not have to match with the hostname.

You can just add an entry for the supplementary host to `[mash_example_com]` if there are other entries there already.

##### Create `vars.yml` for the dedicated instance

Then, create a new directory where `vars.yml` for the supplementary host is stored. If `mash.example.com` is your main host, name the directory as `mash.example.com-litellm-deps`. Its path therefore will be `inventory/host_vars/mash.example.com-litellm-deps`.

After creating the directory, add a new `vars.yml` file inside it with a content below. It will have running the playbook create a `mash-litellm-valkey` instance on the new host, setting `/mash/litellm-valkey` to the base directory of the dedicated Valkey instance.

```yaml
# This is vars.yml for the supplementary host of LiteLLM.

---

########################################################################
#                                                                      #
# Playbook                                                             #
#                                                                      #
########################################################################

# Put a strong secret below, generated with `pwgen -s 64 1` or in another way
mash_playbook_generic_secret_key: ''

# Override service names and directory path prefixes
mash_playbook_service_identifier_prefix: 'mash-litellm-'
mash_playbook_service_base_directory_name_prefix: 'litellm-'

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
# litellm                                                              #
#                                                                      #
########################################################################

# Add the base configuration as specified above

# Enable the cache
litellm_cache_type: redis

# Point LiteLLM to its dedicated Valkey instance
litellm_cache_hostname: mash-litellm-valkey

# Make sure the LiteLLM container is connected to the container network of its dedicated Valkey service (mash-litellm-valkey)
litellm_container_additional_networks_custom:
  - "mash-litellm-valkey"

# Make sure the LiteLLM service (mash-litellm.service) starts after its dedicated Valkey service (mash-litellm-valkey.service)
litellm_systemd_required_services_list_custom:
  - "mash-litellm-valkey.service"

########################################################################
#                                                                      #
# /litellm                                                             #
#                                                                      #
########################################################################
```

Running the installation command will create the dedicated Valkey instance named `mash-litellm-valkey`.

#### Setting up a shared Valkey instance

If you host only LiteLLM on this server, it is fine to set up a single shared Valkey instance.

To install the single instance and hook LiteLLM to it, add the following configuration to `inventory/host_vars/mash.example.com/vars.yml`:

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
# litellm                                                              #
#                                                                      #
########################################################################

# Add the base configuration as specified above

# Enable the cache
litellm_cache_type: redis

# Point LiteLLM to the shared Valkey instance
litellm_cache_hostname: "{{ valkey_identifier }}"

# Make sure the LiteLLM container is connected to the container network of the shared Valkey service (mash-valkey)
litellm_container_additional_networks_custom:
  - "{{ valkey_identifier }}"

# Make sure the LiteLLM service (mash-litellm.service) starts after the shared Valkey service (mash-valkey.service)
litellm_systemd_required_services_list_custom:
  - "{{ valkey_identifier }}.service"

########################################################################
#                                                                      #
# /litellm                                                             #
#                                                                      #
########################################################################
```

Running the installation command will create the shared Valkey instance named `mash-valkey`.

## Installation

If you have decided to install the dedicated Valkey instance for LiteLLM, make sure to run the [installing](../installing.md) command for the supplementary host (`mash.example.com-litellm-deps`) first, before running it for the main host (`mash.example.com`).

Note that running the `just` commands for installation (`just install-all` or `just setup-all`) automatically takes care of the order. See [here](../running-multiple-instances.md#1-adjust-hosts) for more details about it.

## Usage

After running the command for installation, the LiteLLM instance becomes available at the URL specified with `litellm_hostname`. With the configuration above, the service is hosted at `https://litellm.example.com`.

You can use the LiteLLM instance by running a command as below:

```sh
curl https://litellm.example.com
```

## Troubleshooting

See [this section](https://forgejo.littlecedar.net/grenewode/ansible-role-mash-litellm/src/branch/main/docs/configuring-litellm.md#troubleshooting) on the role's documentation for details.
