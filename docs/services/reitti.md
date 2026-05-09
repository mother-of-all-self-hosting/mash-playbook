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
SPDX-FileCopyrightText: 2024 Tiz
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Reitti

The playbook can install and configure [Reitti](https://www.dedicatedcode.com/projects/reitti/) for you.

Reitti is a personal location tracking and analysis application.

See the project's [documentation](https://www.dedicatedcode.com/projects/reitti/) to learn what Reitti does and why it might be useful to you.

For details about configuring the [Ansible role for Reitti](https://radicle.network/nodes/seed.radicle.garden/rad%3Az3rhdtDR5EHHGk1SNBHwYtofxNyAf), you can check them via:

- 🌐 [the role's documentation](https://radicle.network/nodes/seed.radicle.garden/rad%3Az3rhdtDR5EHHGk1SNBHwYtofxNyAf/tree/docs/configuring-reitti.md) online
- 📁 `roles/galaxy/reitti/docs/configuring-reitti.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Postgres database with PostGIS extensions installed](postgis.md)
- [Traefik](traefik.md) reverse-proxy server
- [Valkey](valkey.md) data-store; see [below](#configure-valkey) for details about installation

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# reitti                                                               #
#                                                                      #
########################################################################

reitti_enabled: true

reitti_hostname: reitti.example.com

########################################################################
#                                                                      #
# /reitti                                                              #
#                                                                      #
########################################################################
```

### Configure Valkey

Reitti requires a Valkey data-store to work. This playbook supports it, and you can set up a Valkey instance by enabling it on `vars.yml`.

If Reitti is the sole service which requires Valkey on your server, it is fine to set up just a single Valkey instance. However, **it is not recommended if there are other services which require it, because sharing the Valkey instance has security concerns and possibly causes data conflicts**, as described on the [documentation for configuring Valkey](valkey.md). In this case, you should install a dedicated Valkey instance for each of them.

If you are unsure whether you will install other services along with Reitti or you have already set up services which need Valkey (such as [Nextcloud](nextcloud.md), [PeerTube](peertube.md), and [Funkwhale](funkwhale.md)), it is recommended to install a Valkey instance dedicated to Reitti.

*See [below](#setting-up-a-shared-valkey-instance) for an instruction to install a shared instance.*

#### Setting up a dedicated Valkey instance

To create a dedicated instance for Reitti, you can follow the steps below:

1. Adjust the `hosts` file
2. Create a new `vars.yml` file for the dedicated instance
3. Edit the existing `vars.yml` file for the main host

*See [this page](../running-multiple-instances.md) for details about configuring multiple instances of Valkey on the same server.*

##### Adjust `hosts`

At first, you need to adjust `inventory/hosts` file to add a supplementary host for Reitti.

The content should be something like below. Make sure to replace `mash.example.com` with your hostname and `YOUR_SERVER_IP_ADDRESS_HERE` with the IP address of the host, respectively. The same IP address should be set to both, unless the Valkey instance will be served from a different machine.

```ini
[mash_servers]
[mash_servers:children]
mash_example_com

[mash_example_com]
mash.example.com ansible_host=YOUR_SERVER_IP_ADDRESS_HERE
mash.example.com-reitti-deps ansible_host=YOUR_SERVER_IP_ADDRESS_HERE
…
```

`mash_example_com` can be any string and does not have to match with the hostname.

You can just add an entry for the supplementary host to `[mash_example_com]` if there are other entries there already.

##### Create `vars.yml` for the dedicated instance

Then, create a new directory where `vars.yml` for the supplementary host is stored. If `mash.example.com` is your main host, name the directory as `mash.example.com-reitti-deps`. Its path therefore will be `inventory/host_vars/mash.example.com-reitti-deps`.

After creating the directory, add a new `vars.yml` file inside it with a content below. It will have running the playbook create a `mash-reitti-valkey` instance on the new host, setting `/mash/reitti-valkey` to the base directory of the dedicated Valkey instance.

```yaml
# This is vars.yml for the supplementary host of Reitti.

---

########################################################################
#                                                                      #
# Playbook                                                             #
#                                                                      #
########################################################################

# Put a strong secret below, generated with `pwgen -s 64 1` or in another way
mash_playbook_generic_secret_key: ''

# Override service names and directory path prefixes
mash_playbook_service_identifier_prefix: 'mash-reitti-'
mash_playbook_service_base_directory_name_prefix: 'reitti-'

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
# reitti                                                               #
#                                                                      #
########################################################################

# Add the base configuration as specified above

# Point Reitti to its dedicated Valkey instance
reitti_redis_hostname: mash-reitti-valkey

# Make sure the Reitti service (mash-reitti.service) is connected to the container network of its dedicated Valkey service (mash-reitti-valkey)
reitti_container_additional_networks_custom:
  - "mash-reitti-valkey"

# Make sure the Reitti service (mash-reitti.service) starts after its dedicated Valkey service (mash-reitti-valkey.service)
reitti_systemd_required_services_list_custom:
  - "mash-reitti-valkey.service"

########################################################################
#                                                                      #
# /reitti                                                              #
#                                                                      #
########################################################################
```

Running the installation command will create the dedicated Valkey instance named `mash-reitti-valkey`.

#### Setting up a shared Valkey instance

If you host only Reitti on this server, it is fine to set up a single shared Valkey instance.

To install the single instance and hook Reitti to it, add the following configuration to `inventory/host_vars/mash.example.com/vars.yml`:

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
# reitti                                                               #
#                                                                      #
########################################################################

# Add the base configuration as specified above

# Point Reitti to the shared Valkey instance
reitti_redis_hostname: "{{ valkey_identifier }}"

# Make sure the Reitti container is connected to the container network of the shared Valkey service (mash-valkey)
reitti_container_additional_networks_custom:
  - "{{ valkey_container_network }}"

# Make sure the Reitti service (mash-reitti.service) starts after the shared Valkey service (mash-valkey.service)
reitti_systemd_required_services_list_custom:
  - "{{ valkey_identifier }}.service"

########################################################################
#                                                                      #
# /reitti                                                              #
#                                                                      #
########################################################################
```

Running the installation command will create the shared Valkey instance named `mash-valkey`.

### Usage

After running the command for installation, the Reitti instance becomes available at the URL specified with `reitti_hostname`. With the configuration above, the service is hosted at `https://reitti.example.com`.

To get started, open the URL with a web browser to create an account. **Note that the first registered user becomes an administrator automatically.**

## Troubleshooting

See [this section](https://radicle.network/nodes/seed.radicle.garden/rad%3Az3rhdtDR5EHHGk1SNBHwYtofxNyAf/tree/docs/configuring-reitti.md#troubleshooting) on the role's documentation for details.
