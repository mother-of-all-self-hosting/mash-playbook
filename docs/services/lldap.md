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

# LLDAP

The playbook can install and configure [LLDAP](https://lldap.it) for you.

LLDAP is a modern URL shortener with support for custom domains with functions like statistics and user management.

See the project's [documentation](https://github.com/thedevs-network/lldap/blob/main/README.md) to learn what LLDAP does and why it might be useful to you.

For details about configuring the [Ansible role for LLDAP](https://github.com/mother-of-all-self-hosting/ansible-role-lldap), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-lldap/blob/main/docs/configuring-lldap.md) online
- 📁 `roles/galaxy/lldap/docs/configuring-lldap.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server
- (optional) [Postgres](postgres.md) / MySQL / [MariaDB](mariadb.md) database — LLDAP will default to [SQLite](https://www.sqlite.org/) if Postgres is not enabled
- (optional) [Valkey](valkey.md) data-store; see [below](#configuring-valkey-optional) for details about installation

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file:

```yaml
########################################################################
#                                                                      #
# lldap                                                                #
#                                                                      #
########################################################################

lldap_enabled: true

lldap_hostname: lldap.example.com

########################################################################
#                                                                      #
# /lldap                                                               #
#                                                                      #
########################################################################
```

**Note**: hosting LLDAP under a subpath (by configuring the `lldap_path_prefix` variable) does not seem to be possible due to LLDAP's technical limitations.

### Select database to use (optional)

By default LLDAP is configured to use Postgres, but you can choose other databases such as MySQL (MariaDB) and SQLite. See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-lldap/blob/main/docs/configuring-lldap.md#specify-database-optional) on the role's documentation for details.

### Configure the mailer (optional)

On LLDAP you can set up a mailer for functions such as sending a password reset mail. **You can use Exim-relay as the mailer, which is enabled on this playbook by default.** See [this page about Exim-relay configuration](exim-relay.md) for details about how to set it up.

>[!NOTE]
> Without setting an authentication method such as DKIM, SPF, and DMARC for your hostname, emails are most likely to be quarantined as spam at recipient's mail servers. If you have set up a mail server with the [exim-relay Ansible role](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay), you can enable DKIM signing with it. Refer [its documentation](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay/blob/main/docs/configuring-exim-relay.md#enable-dkim-support-optional) for details.

### Configuring Valkey (optional)

Valkey can optionally be enabled for caching data. This playbook supports it, and you can set up a Valkey instance by enabling it on `vars.yml`.

If LLDAP is the sole service which requires Valkey on your server, it is fine to set up just a single Valkey instance. However, **it is not recommended if there are other services which require it, because sharing the Valkey instance has security concerns and possibly causes data conflicts**, as described on the [documentation for configuring Valkey](valkey.md). In this case, you should install a dedicated Valkey instance for each of them.

If you are unsure whether you will install other services along with LLDAP or you have already set up services which need Valkey (such as [PeerTube](peertube.md), [Funkwhale](funkwhale.md), and [Docmost](docmost.md)), it is recommended to install a Valkey instance dedicated to LLDAP.

*See [below](#setting-up-a-shared-valkey-instance) for an instruction to install a shared instance.*

#### Setting up a dedicated Valkey instance

To create a dedicated instance for LLDAP, you can follow the steps below:

1. Adjust the `hosts` file
2. Create a new `vars.yml` file for the dedicated instance
3. Edit the existing `vars.yml` file for the main host

*See [this page](../running-multiple-instances.md) for details about configuring multiple instances of Valkey on the same server.*

##### Adjust `hosts`

At first, you need to adjust `inventory/hosts` file to add a supplementary host for LLDAP.

The content should be something like below. Make sure to replace `mash.example.com` with your hostname and `YOUR_SERVER_IP_ADDRESS_HERE` with the IP address of the host, respectively. The same IP address should be set to both, unless the Valkey instance will be served from a different machine.

```ini
[mash_servers]
[mash_servers:children]
mash_example_com

[mash_example_com]
mash.example.com ansible_host=YOUR_SERVER_IP_ADDRESS_HERE
mash.example.com-lldap-deps ansible_host=YOUR_SERVER_IP_ADDRESS_HERE
…
```

`mash_example_com` can be any string and does not have to match with the hostname.

You can just add an entry for the supplementary host to `[mash_example_com]` if there are other entries there already.

##### Create `vars.yml` for the dedicated instance

Then, create a new directory where `vars.yml` for the supplementary host is stored. If `mash.example.com` is your main host, name the directory as `mash.example.com-lldap-deps`. Its path therefore will be `inventory/host_vars/mash.example.com-lldap-deps`.

After creating the directory, add a new `vars.yml` file inside it with a content below. It will have running the playbook create a `mash-lldap-valkey` instance on the new host, setting `/mash/lldap-valkey` to the base directory of the dedicated Valkey instance.

```yaml
# This is vars.yml for the supplementary host of LLDAP.

---

########################################################################
#                                                                      #
# Playbook                                                             #
#                                                                      #
########################################################################

# Put a strong secret below, generated with `pwgen -s 64 1` or in another way
mash_playbook_generic_secret_key: ''

# Override service names and directory path prefixes
mash_playbook_service_identifier_prefix: 'mash-lldap-'
mash_playbook_service_base_directory_name_prefix: 'lldap-'

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
# lldap                                                                 #
#                                                                      #
########################################################################

# Add the base configuration as specified above

# Point LLDAP to its dedicated Valkey instance
lldap_redis_hostname: mash-lldap-valkey

# Make sure the LLDAP service (mash-lldap.service) starts after its dedicated Valkey service (mash-lldap-valkey.service)
lldap_systemd_required_services_list_custom:
  - "mash-lldap-valkey.service"

# Make sure the LLDAP container is connected to the container network of its dedicated Valkey service (mash-lldap-valkey)
lldap_container_additional_networks_custom:
  - "mash-lldap-valkey"

########################################################################
#                                                                      #
# /lldap                                                                #
#                                                                      #
########################################################################
```

Running the installation command will create the dedicated Valkey instance named `mash-lldap-valkey`.

#### Setting up a shared Valkey instance

If you host only LLDAP on this server, it is fine to set up a single shared Valkey instance.

To install the single instance and hook LLDAP to it, add the following configuration to `inventory/host_vars/mash.example.com/vars.yml`:

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
# lldap                                                                 #
#                                                                      #
########################################################################

# Add the base configuration as specified above

# Point LLDAP to the shared Valkey instance
lldap_redis_hostname: "{{ valkey_identifier }}"

# Make sure the LLDAP service (mash-lldap.service) starts after the shared Valkey service (mash-valkey.service)
lldap_systemd_required_services_list_custom:
  - "{{ valkey_identifier }}.service"

# Make sure the LLDAP container is connected to the container network of the shared Valkey service (mash-valkey)
lldap_container_additional_networks_custom:
  - "{{ valkey_identifier }}"

########################################################################
#                                                                      #
# /lldap                                                                #
#                                                                      #
########################################################################
```

Running the installation command will create the shared Valkey instance named `mash-valkey`.

## Installation

If you have decided to install the dedicated Valkey instance for LLDAP, make sure to run the [installing](../installing.md) command for the supplementary host (`mash.example.com-lldap-deps`) first, before running it for the main host (`mash.example.com`).

Note that running the `just` commands for installation (`just install-all` or `just setup-all`) automatically takes care of the order. See [here](../running-multiple-instances.md#1-adjust-hosts) for more details about it.

## Usage

After running the command for installation, the LLDAP instance becomes available at the URL specified with `lldap_hostname`. With the configuration above, the service is hosted at `https://lldap.example.com`.

To get started, open the URL with a web browser, and register the administrator account. You can create additional users (admin-privileged or not) after that.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-lldap/blob/main/docs/configuring-lldap.md#troubleshooting) on the role's documentation for details.

## Related services

- [YOURLS](yourls.md) — Your Own URL Shortener, on your server
