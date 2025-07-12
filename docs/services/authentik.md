<!--
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# authentik

[authentik](https://goauthentik.io/) is an open-source Identity Provider focused on flexibility and versatility.

> [!WARNING]
> SSO is pretty complex and while this role will install authentik for you we only tested OIDC and OAUTH integration. There is a high probability that using outposts/LDAP would need further configuration efforts. Make sure you test before using this in production and feel free to provide feedback!

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
# authentik                                                            #
#                                                                      #
########################################################################

authentik_enabled: true

authentik_hostname: authentik.example.com

# Put a strong secret below, generated with `pwgen -s 64 1` or in another way
authentik_secret_key: ''

# Valkey configuration, as described below

########################################################################
#                                                                      #
# /authentik                                                           #
#                                                                      #
########################################################################
```

### Configure Valkey

authentik requires a Valkey data-store to work. This playbook supports it, and you can set up a Valkey instance by enabling it on `vars.yml`.

If authentik is the sole service which requires Valkey on your server, it is fine to set up just a single Valkey instance. However, **it is not recommended if there are other services which require it, because sharing the Valkey instance has security concerns and possibly causes data conflicts**, as described on the [documentation for configuring Valkey](valkey.md). In this case, you should install a dedicated Valkey instance for each of them.

If you are unsure whether you will install other services along with authentik or you have already set up services which need Valkey (such as [Nextcloud](nextcloud.md), [Docmost](docmost.md), and [PeerTube](peertube.md)), it is recommended to install a Valkey instance dedicated to authentik.

*See [below](#setting-up-a-shared-valkey-instance) for an instruction to install a shared instance.*

#### Setting up a dedicated Valkey instance

To create a dedicated instance for authentik, you can follow the steps below:

1. Adjust the `hosts` file
2. Create a new `vars.yml` file for the dedicated instance
3. Edit the existing `vars.yml` file for the main host

*See [this page](../running-multiple-instances.md) for details about configuring multiple instances of Valkey on the same server.*

##### Adjust `hosts`

At first, you need to adjust `inventory/hosts` file to add a supplementary host for authentik.

The content should be something like below. Make sure to replace `mash.example.com` with your hostname and `YOUR_SERVER_IP_ADDRESS_HERE` with the IP address of the host, respectively. The same IP address should be set to both, unless the Valkey instance will be served from a different machine.

```ini
[mash_servers]
[mash_servers:children]
mash_example_com

[mash_example_com]
mash.example.com ansible_host=YOUR_SERVER_IP_ADDRESS_HERE
mash.example.com-authentik-deps ansible_host=YOUR_SERVER_IP_ADDRESS_HERE
…
```

`mash_example_com` can be any string and does not have to match with the hostname.

You can just add an entry for the supplementary host to `[mash_example_com]` if there are other entries there already.

##### Create `vars.yml` for the dedicated instance

Then, create a new directory where `vars.yml` for the supplementary host is stored. If `mash.example.com` is your main host, name the directory as `mash.example.com-authentik-deps`. Its path therefore will be `inventory/host_vars/mash.example.com-authentik-deps`.

After creating the directory, add a new `vars.yml` file inside it with a content below. It will have running the playbook create a `mash-authentik-valkey` instance on the new host, setting `/mash/authentik-valkey` to the base directory of the dedicated Valkey instance.

```yaml
# This is vars.yml for the supplementary host of authentik.

---

########################################################################
#                                                                      #
# Playbook                                                             #
#                                                                      #
########################################################################

# Put a strong secret below, generated with `pwgen -s 64 1` or in another way
mash_playbook_generic_secret_key: ''

# Override service names and directory path prefixes
mash_playbook_service_identifier_prefix: 'mash-authentik-'
mash_playbook_service_base_directory_name_prefix: 'authentik-'

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
# authentik                                                            #
#                                                                      #
########################################################################

# Add the base configuration as specified above

# Point authentik to its dedicated Valkey instance
authentik_config_redis_hostname: mash-authentik-valkey

# Make sure the authentik service (mash-authentik.service) starts after its dedicated Valkey service (mash-authentik-valkey.service)
authentik_systemd_required_services_list_custom:
  - "mash-authentik-valkey.service"

# Make sure the authentik container is connected to the container network of its dedicated Valkey service (mash-authentik-valkey)
authentik_container_additional_networks_custom:
  - "mash-authentik-valkey"

########################################################################
#                                                                      #
# /authentik                                                           #
#                                                                      #
########################################################################
```

Running the installation command will create the dedicated Valkey instance named `mash-authentik-valkey`.

#### Setting up a shared Valkey instance

If you host only authentik on this server, it is fine to set up a single shared Valkey instance.

To install the single instance and hook authentik to it, add the following configuration to `inventory/host_vars/mash.example.com/vars.yml`:

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
# authentik                                                            #
#                                                                      #
########################################################################

# Add the base configuration as specified above

# Point authentik to the shared Valkey instance
authentik_config_redis_hostname: "{{ valkey_identifier }}"

# Make sure the authentik service (mash-authentik.service) starts after the shared Valkey service (mash-valkey.service)
authentik_systemd_required_services_list_custom:
  - "{{ valkey_identifier }}.service"

# Make sure the authentik container is connected to the container network of the shared Valkey service (mash-valkey)
authentik_container_additional_networks_custom:
  - "{{ valkey_identifier }}"

########################################################################
#                                                                      #
# /authentik                                                           #
#                                                                      #
########################################################################
```

Running the installation command will create the shared Valkey instance named `mash-valkey`.

### Extending the configuration

There are some additional things you may wish to configure about the service.

Take a look at:

- [authentik](https://github.com/mother-of-all-self-hosting/ansible-role-authentik)'s [`defaults/main.yml`](https://github.com/mother-of-all-self-hosting/ansible-role-authentik/blob/main/defaults/main.yml) for some variables that you can customize via your `vars.yml` file.

## Installation

If you have decided to install the dedicated Valkey instance for authentik, make sure to run the [installing](../installing.md) command for the supplementary host (`mash.example.com-authentik-deps`) first, before running it for the main host (`mash.example.com`).

Note that running the `just` commands for installation (`just install-all` or `just setup-all`) automatically takes care of the order. See [here](../running-multiple-instances.md#1-adjust-hosts) for more details about it.

## Usage

After installation, you can set the admin password at `https://<authentik_hostname>/if/flow/initial-setup/`. Set the admin password there and start adding applications and users! Refer to the [official documentation](https://goauthentik.io/docs/) to learn how to integrate services. For this playbook tested examples are described in the respective service documentation. See

* [Grafana](./grafana.md#single-sign-on-authentik)
* [Nextcloud](./nextcloud.md#single-sign-on-authentik)
