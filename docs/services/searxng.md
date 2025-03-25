<!--
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2024 Sergio Durigan Junior
SPDX-FileCopyrightText: 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# SearXNG

[SearXNG](https://github.com/searxng/searxng/) is a privacy-respecting, hackable [metasearch engine](https://en.wikipedia.org/wiki/Metasearch_engine).

## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server

If rate-limiting is enabled, then it also requires:

- a [Valkey](valkey.md) data-store; see [below](#configuring-rate-limiting) for details about installation

## Configuration

To enable this service, add the following configuration to your `vars.yml` file:

```yaml
########################################################################
#                                                                      #
# searxng                                                              #
#                                                                      #
########################################################################

searxng_enabled: true

searxng_instance_name: My Example Instance Name'

searxng_hostname: mash.example.com
searxng_path_prefix: /searxng

# Generate the secret key with "openssl rand -hex 32".
searxng_secret_key: 'MY_SECRET_KEY'

########################################################################
#                                                                      #
# /searxng                                                             #
#                                                                      #
########################################################################
```

### Configuring rate-limiting

If you want to enable rate-limiting, add the following configuration to `vars.yml`:

```yaml
searxng_enable_rate_limiter: true
```

Rate-limiting also requires a Valkey data-store to work. This playbook supports it, and you can set up a Valkey instance by enabling it on `vars.yml`.

If SearXNG is the sole service which requires Valkey on your server, it is fine to set up just a single Valkey instance. However, **it is not recommended if there are other services which require it, because sharing the Valkey instance has security concerns and possibly causes data conflicts**, as described on the [documentation for configuring Valkey](valkey.md). In this case, you should install a dedicated Valkey instance for each of them.

If you are unsure whether you will install other services along with SearXNG or you have already set up services which need Valkey (such as [Nextcloud](nextcloud.md), [PeerTube](peertube.md), and [Funkwhale](funkwhale.md)), it is recommended to install a Valkey instance dedicated to SearXNG.

*See [below](#setting-up-a-shared-valkey-instance) for an instruction to install a shared instance.*

#### Setting up a dedicated Valkey instance

To create a dedicated instance for SearXNG, you can follow the steps below:

1. Adjust the `hosts` file
2. Create a new `vars.yml` file for the dedicated instance
3. Edit the existing `vars.yml` file for the main host

*See [this page](../running-multiple-instances.md) for details about configuring multiple instances of Valkey on the same server.*

##### Adjust `hosts`

At first, you need to adjust `inventory/hosts` file to add a supplementary host for SearXNG.

The content should be something like below. Make sure to replace `mash.example.com` with your hostname and `YOUR_SERVER_IP_ADDRESS_HERE` with the IP address of the host, respectively. The same IP address should be set to both, unless the Valkey instance will be served from a different machine.

```ini
[mash_servers]
[mash_servers:children]
mash_example_com

[mash_example_com]
mash.example.com ansible_host=YOUR_SERVER_IP_ADDRESS_HERE
mash.example.com-searxng-deps ansible_host=YOUR_SERVER_IP_ADDRESS_HERE
…
```

`mash_example_com` can be any string and does not have to match with the hostname.

You can just add an entry for the supplementary host to `[mash_example_com]` if there are other entries there already.

##### Create `vars.yml` for the dedicated instance

Then, create a new directory where `vars.yml` for the supplementary host is stored. If `mash.example.com` is your main host, name the directory as `mash.example.com-searxng-deps`. Its path therefore will be `inventory/host_vars/mash.example.com-searxng-deps`.

After creating the directory, add a new `vars.yml` file inside it with a content below. It will have running the playbook create a `mash-searxng-valkey` instance on the new host, setting `/mash/searxng-valkey` to the base directory of the dedicated Valkey instance.

```yaml
# This is vars.yml for the supplementary host of SearXNG.

---

########################################################################
#                                                                      #
# Playbook                                                             #
#                                                                      #
########################################################################

# Put a strong secret below, generated with `pwgen -s 64 1` or in another way
mash_playbook_generic_secret_key: ''

# Override service names and directory path prefixes
mash_playbook_service_identifier_prefix: 'mash-searxng-'
mash_playbook_service_base_directory_name_prefix: 'searxng-'

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
# searxng                                                              #
#                                                                      #
########################################################################

# Add the base configuration as specified above

# Point SearXNG to its dedicated Valkey instance
searxng_rate_limiter_config_valkey_hostname: mash-searxng-valkey

# Make sure the SearXNG service (mash-searxng.service) starts after its dedicated Valkey service (mash-searxng-valkey.service)
searxng_systemd_required_services_list_custom:
  - "mash-searxng-valkey.service"

# Make sure the SearXNG container is connected to the container network of its dedicated Valkey service (mash-searxng-valkey)
searxng_container_additional_networks_custom:
  - "mash-searxng-valkey"

########################################################################
#                                                                      #
# /searxng                                                             #
#                                                                      #
########################################################################
```

Running the installation command will create the dedicated Valkey instance named `mash-searxng-valkey`.

#### Setting up a shared Valkey instance

If you host only SearXNG on this server, it is fine to set up a single shared Valkey instance.

To install the single instance and hook SearXNG to it, add the following configuration to `inventory/host_vars/mash.example.com/vars.yml`:

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
# searxng                                                              #
#                                                                      #
########################################################################

# Add the base configuration as specified above

# Point SearXNG to the shared Valkey instance
searxng_rate_limiter_config_valkey_hostname: "{{ valkey_identifier }}"

# Make sure the SearXNG service (mash-searxng.service) starts after the shared Valkey service (mash-valkey.service)
searxng_systemd_required_services_list_custom:
  - "{{ valkey_identifier }}.service"

# Make sure the SearXNG container is connected to the container network of the shared Valkey service (mash-valkey)
searxng_container_additional_networks_custom:
  - "{{ valkey_identifier }}"

########################################################################
#                                                                      #
# /searxng                                                             #
#                                                                      #
########################################################################
```

Running the installation command will create the shared Valkey instance named `mash-valkey`.

### Configuring basic authentication

If you are running a private instance, you might want to protect it with so that only authorized people can use it. An easy option is to choose a non-trivial subpath by modifying the `searxng_path_prefix`. Another, more complete option is to enable basic authentication for the instance.

To do the latter, add the following configuration to `vars.yml`:

```yaml
searxng_basic_auth_enabled: true
searxng_basic_auth_username: 'my_username'
searxng_basic_auth_password: 'my_password'
```

## Installation

If you have decided to install the dedicated Valkey instance for SearXNG, make sure to run the [installing](../installing.md) command for the supplementary host (`mash.example.com-searxng-deps`) first, before running it for the main host (`mash.example.com`).

Note that running the `just` commands for installation (`just install-all` or `just setup-all`) automatically takes care of the order. See [here](../running-multiple-instances.md#1-adjust-hosts) for more details about it.

## Usage

After installation, your SearXNG instance becomes available at the URL specified with `searxng_hostname` and `searxng_path_prefix`. With the configuration above, the service is hosted at `https://mash.example.com/searxng`.

If authentication is enabled, you can log in with the username and password specified with `searxng_basic_auth_username` and `searxng_basic_auth_password`.
