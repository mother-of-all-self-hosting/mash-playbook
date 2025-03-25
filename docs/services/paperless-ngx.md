<!--
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Paperless-ngx

[Paperless-ngx](https://paperless-ngx.com) is a community-supported open-source document management system that transforms your physical documents into a searchable online archive to organize them paperless.

> [!WARNING]
> Paperless-ngx currently [does not support](https://github.com/paperless-ngx/paperless-ngx/issues/6352) running the container rootless, therefore the role has not the usual security features of other services provided by this playbook. This put your system more at higher risk as vulnerabilities can have a higher impact.

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
# paperless                                                            #
#                                                                      #
########################################################################

paperless_enabled: true

paperless_hostname: paperless.example.com

# Set the following variables to create an initial admin user
# It will not re-create an admin user, it will not change a password if the user is already created
# paperless_admin_user: USERNAME
# paperless_admin_password: SECURE_PASSWORD

# Valkey configuration, as described below

########################################################################
#                                                                      #
# /paperless                                                           #
#                                                                      #
########################################################################
```

### Configure Valkey

Paperless-ngx requires a Valkey data-store to work. This playbook supports it, and you can set up a Valkey instance by enabling it on `vars.yml`.

If Paperless-ngx is the sole service which requires Valkey on your server, it is fine to set up just a single Valkey instance. However, **it is not recommended if there are other services which require it, because sharing the Valkey instance has security concerns and possibly causes data conflicts**, as described on the [documentation for configuring Valkey](valkey.md). In this case, you should install a dedicated Valkey instance for each of them.

If you are unsure whether you will install other services along with Paperless-ngx or you have already set up services which need Valkey (such as [Nextcloud](nextcloud.md), [PeerTube](peertube.md), and [Funkwhale](funkwhale.md)), it is recommended to install a Valkey instance dedicated to Paperless-ngx.

*See [below](#setting-up-a-shared-valkey-instance) for an instruction to install a shared instance.*

#### Setting up a dedicated Valkey instance

To create a dedicated instance for Paperless-ngx, you can follow the steps below:

1. Adjust the `hosts` file
2. Create a new `vars.yml` file for the dedicated instance
3. Edit the existing `vars.yml` file for the main host

*See [this page](../running-multiple-instances.md) for details about configuring multiple instances of Valkey on the same server.*

##### Adjust `hosts`

At first, you need to adjust `inventory/hosts` file to add a supplementary host for Paperless-ngx.

The content should be something like below. Make sure to replace `mash.example.com` with your hostname and `YOUR_SERVER_IP_ADDRESS_HERE` with the IP address of the host, respectively. The same IP address should be set to both, unless the Valkey instance will be served from a different machine.

```ini
[mash_servers]
[mash_servers:children]
mash_example_com

[mash_example_com]
mash.example.com ansible_host=YOUR_SERVER_IP_ADDRESS_HERE
mash.example.com-paperless-deps ansible_host=YOUR_SERVER_IP_ADDRESS_HERE
…
```

`mash_example_com` can be any string and does not have to match with the hostname.

You can just add an entry for the supplementary host to `[mash_example_com]` if there are other entries there already.

##### Create `vars.yml` for the dedicated instance

Then, create a new directory where `vars.yml` for the supplementary host is stored. If `mash.example.com` is your main host, name the directory as `mash.example.com-paperless-deps`. Its path therefore will be `inventory/host_vars/mash.example.com-paperless-deps`.

After creating the directory, add a new `vars.yml` file inside it with a content below. It will have running the playbook create a `mash-paperless-valkey` instance on the new host, setting `/mash/paperless-valkey` to the base directory of the dedicated Valkey instance.

```yaml
# This is vars.yml for the supplementary host of Paperless-ngx.

---

########################################################################
#                                                                      #
# Playbook                                                             #
#                                                                      #
########################################################################

# Put a strong secret below, generated with `pwgen -s 64 1` or in another way
mash_playbook_generic_secret_key: ''

# Override service names and directory path prefixes
mash_playbook_service_identifier_prefix: 'mash-paperless-'
mash_playbook_service_base_directory_name_prefix: 'paperless-'

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
# paperless                                                            #
#                                                                      #
########################################################################

# Add the base configuration as specified above

# Point Paperless-ngx to its dedicated Valkey instance
paperless_redis_hostname: mash-paperless-valkey

# Make sure the Paperless-ngx service (mash-paperless.service) starts after its dedicated Valkey service (mash-paperless-valkey.service)
paperless_systemd_required_services_list_custom:
  - "mash-paperless-valkey.service"

# Make sure the Paperless-ngx container is connected to the container network of its dedicated Valkey service (mash-paperless-valkey)
paperless_container_additional_networks_custom:
  - "mash-paperless-valkey"

########################################################################
#                                                                      #
# /paperless                                                           #
#                                                                      #
########################################################################
```

Running the installation command will create the dedicated Valkey instance named `mash-paperless-valkey`.

#### Setting up a shared Valkey instance

If you host only Paperless-ngx on this server, it is fine to set up a single shared Valkey instance.

To install the single instance and hook Paperless-ngx to it, add the following configuration to `inventory/host_vars/mash.example.com/vars.yml`:

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
# paperless                                                            #
#                                                                      #
########################################################################

# Add the base configuration as specified above

# Point Paperless-ngx to the shared Valkey instance
paperless_redis_hostname: "{{ valkey_identifier }}"

# Make sure the Paperless-ngx service (mash-paperless.service) starts after the shared Valkey service (mash-valkey.service)
paperless_systemd_required_services_list_custom:
  - "{{ valkey_identifier }}.service"

# Make sure the Paperless-ngx container is connected to the container network of the shared Valkey service (mash-valkey)
paperless_container_additional_networks_custom:
  - "{{ valkey_identifier }}"

########################################################################
#                                                                      #
# /paperless                                                           #
#                                                                      #
########################################################################
```

Running the installation command will create the shared Valkey instance named `mash-valkey`.

### Extending the configuration

There are some additional things you may wish to configure about the service.

Take a look at:

- [Paperless-ngx](https://github.com/mother-of-all-self-hosting/ansible-role-paperless)'s [`defaults/main.yml`](https://github.com/mother-of-all-self-hosting/ansible-role-paperless/blob/main/defaults/main.yml) for some variables that you can customize via your `vars.yml` file.

## Installation

If you have decided to install the dedicated Valkey instance for Paperless-ngx, make sure to run the [installing](../installing.md) command for the supplementary host (`mash.example.com-paperless-deps`) first, before running it for the main host (`mash.example.com`).

Note that running the `just` commands for installation (`just install-all` or `just setup-all`) automatically takes care of the order. See [here](../running-multiple-instances.md#1-adjust-hosts) for more details about it.

## Usage

After installation, your Paperless-ngx instance becomes available at the URL specified with `paperless_hostname`.

Refer to the [official documentation](https://docs.paperless-ngx.com/) to learn how to use Paperless-ngx.
