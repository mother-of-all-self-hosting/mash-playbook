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

# Open Archiver

The playbook can install and configure [Open Archiver](https://github.com/karlomikus/bar-assistant/) for you.

Open Archiver is a service for managing cocktail recipes at your home bar with a lot of cocktail-oriented features like ingredient substitutes. The playbook is configured to set up the Open Archiver's API server and its web client software [Salt Rim](https://github.com/karlomikus/vue-salt-rim).

See the project's [documentation](https://docs.openarchiver.app/) to learn what Open Archiver does and why it might be useful to you.

For details about configuring the [Ansible role for Open Archiver](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az3JDUHjeHMqbZ3YLxquSUbCmAJLi), you can check them via:
- 🌐 [the role's documentation](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az3JDUHjeHMqbZ3YLxquSUbCmAJLi/tree/docs/configuring-openarchiver.md) online
- 📁 `roles/galaxy/openarchiver/docs/configuring-openarchiver.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Meilisearch](meilisearch.md)
- [Postgres](postgres.md) database
- [Traefik](traefik.md) reverse-proxy server
- [Valkey](valkey.md) data-store; see [below](#configuring-valkey-optional) for details about installation
- (optional) [Apache Tika Server](tika.md)

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file:

```yaml
########################################################################
#                                                                      #
# openarchiver                                                         #
#                                                                      #
########################################################################

openarchiver_enabled: true

openarchiver_hostname: openarchiver.example.com

########################################################################
#                                                                      #
# /openarchiver                                                        #
#                                                                      #
########################################################################
```

**Note**: hosting Open Archiver under a subpath (by configuring the `openarchiver_path_prefix` variable) does not seem to be possible due to Open Archiver's technical limitations.

### Enabling signing up

By default account registration for the service is disabled. To enable it, add the following configuration to your `vars.yml` file:

```yaml
openarchiver_environment_variables_allow_registration: false
```

### Configuring the mailer (optional)

On Open Archiver you can set up a mailer for functions such as password recovery. If you enable the [exim-relay](exim-relay.md) service in your inventory configuration, the playbook will automatically configure it as a mailer for the service.

>[!NOTE]
> Without setting an authentication method such as DKIM, SPF, and DMARC for your hostname, emails are most likely to be quarantined as spam at recipient's mail servers. If you have set up a mail server with the [exim-relay Ansible role](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay), you can enable DKIM signing with it. Refer [its documentation](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay/blob/main/docs/configuring-exim-relay.md#enable-dkim-support-optional) for details.

### Connecting to a Meilisearch instance (optional)

To enable the search and filtering functions, you can optionally have the Open Archiver instance connect to a Meilisearch instance.

Meilisearch is available on the playbook. Enabling it and setting the default admin API key automatically configures the Open Archiver instance to connect to it.

See [this page](meilisearch.md) for details about how to install it and setting the key for the Meilisearch instance.

>[!NOTE]
> The Meilisearch instance needs to be exposed to the internet. Setting a hostname of the instance to `meilisearch_hostname` automatically exposes it.

### Configuring Valkey (optional)

Valkey can optionally be enabled for caching data. This playbook supports it, and you can set up a Valkey instance by enabling it on `vars.yml`.

If Open Archiver is the sole service which requires Valkey on your server, it is fine to set up just a single Valkey instance. However, **it is not recommended if there are other services which require it, because sharing the Valkey instance has security concerns and possibly causes data conflicts**, as described on the [documentation for configuring Valkey](valkey.md). In this case, you should install a dedicated Valkey instance for each of them.

If you are unsure whether you will install other services along with Open Archiver or you have already set up services which need Valkey (such as [Nextcloud](nextcloud.md), [Vikunja](vikunja.md), and [Docmost](docmost.md)), it is recommended to install a Valkey instance dedicated to Open Archiver.

*See [below](#setting-up-a-shared-valkey-instance) for an instruction to install a shared instance.*

#### Setting up a dedicated Valkey instance

To create a dedicated instance for Open Archiver, you can follow the steps below:

1. Adjust the `hosts` file
2. Create a new `vars.yml` file for the dedicated instance
3. Edit the existing `vars.yml` file for the main host

*See [this page](../running-multiple-instances.md) for details about configuring multiple instances of Valkey on the same server.*

##### Adjust `hosts`

At first, you need to adjust `inventory/hosts` file to add a supplementary host for Open Archiver.

The content should be something like below. Make sure to replace `mash.example.com` with your hostname and `YOUR_SERVER_IP_ADDRESS_HERE` with the IP address of the host, respectively. The same IP address should be set to both, unless the Valkey instance will be served from a different machine.

```ini
[mash_servers]
[mash_servers:children]
mash_example_com

[mash_example_com]
mash.example.com ansible_host=YOUR_SERVER_IP_ADDRESS_HERE
mash.example.com-openarchiver-deps ansible_host=YOUR_SERVER_IP_ADDRESS_HERE
…
```

`mash_example_com` can be any string and does not have to match with the hostname.

You can just add an entry for the supplementary host to `[mash_example_com]` if there are other entries there already.

##### Create `vars.yml` for the dedicated instance

Then, create a new directory where `vars.yml` for the supplementary host is stored. If `mash.example.com` is your main host, name the directory as `mash.example.com-openarchiver-deps`. Its path therefore will be `inventory/host_vars/mash.example.com-openarchiver-deps`.

After creating the directory, add a new `vars.yml` file inside it with a content below. It will have running the playbook create a `mash-openarchiver-valkey` instance on the new host, setting `/mash/openarchiver-valkey` to the base directory of the dedicated Valkey instance.

```yaml
# This is vars.yml for the supplementary host of Open Archiver.

---

########################################################################
#                                                                      #
# Playbook                                                             #
#                                                                      #
########################################################################

# Put a strong secret below, generated with `pwgen -s 64 1` or in another way
mash_playbook_generic_secret_key: ''

# Override service names and directory path prefixes
mash_playbook_service_identifier_prefix: 'mash-openarchiver-'
mash_playbook_service_base_directory_name_prefix: 'openarchiver-'

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
# openarchiver                                                         #
#                                                                      #
########################################################################

# Add the base configuration as specified above

# Point Open Archiver server to its dedicated Valkey instance
openarchiver_redis_hostname: mash-openarchiver-valkey

# Make sure the Open Archiver server service (mash-openarchiver-server.service) starts after its dedicated Valkey service (mash-openarchiver-valkey.service)
openarchiver_systemd_required_services_list_custom:
  - "mash-openarchiver-valkey.service"

# Make sure the Open Archiver server container is connected to the container network of its dedicated Valkey service (mash-openarchiver-valkey)
openarchiver_container_additional_networks_custom:
  - "mash-openarchiver-valkey"

########################################################################
#                                                                      #
# /openarchiver                                                        #
#                                                                      #
########################################################################
```

Running the installation command will create the dedicated Valkey instance named `mash-openarchiver-valkey`.

#### Setting up a shared Valkey instance

If you host only Open Archiver on this server, it is fine to set up a single shared Valkey instance.

To install the single instance and hook Open Archiver to it, add the following configuration to `inventory/host_vars/mash.example.com/vars.yml`:

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
# openarchiver                                                         #
#                                                                      #
########################################################################

# Add the base configuration as specified above

# Point Open Archiver server to the shared Valkey instance
openarchiver_redis_hostname: "{{ valkey_identifier }}"

# Make sure the Open Archiver server service (mash-openarchiver-server.service) starts after the shared Valkey service (mash-valkey.service)
openarchiver_systemd_required_services_list_custom:
  - "{{ valkey_identifier }}.service"

# Make sure the Open Archiver server container is connected to the container network of the shared Valkey service (mash-valkey)
openarchiver_container_additional_networks_custom:
  - "{{ valkey_identifier }}"

########################################################################
#                                                                      #
# /openarchiver                                                        #
#                                                                      #
########################################################################
```

Running the installation command will create the shared Valkey instance named `mash-valkey`.

## Installation

If you have decided to install the dedicated Valkey instance for Open Archiver, make sure to run the [installing](../installing.md) command for the supplementary host (`mash.example.com-openarchiver-deps`) first, before running it for the main host (`mash.example.com`).

Note that running the `just` commands for installation (`just install-all` or `just setup-all`) automatically takes care of the order. See [here](../running-multiple-instances.md#1-adjust-hosts) for more details about it.

## Usage

After running the command for installation, the Open Archiver's API server becomes available at the URL specified with `openarchiver_hostname` and `openarchiver_path_prefix`, and the Salt Rim instance becomes available at the URL specified with `openarchiver_hostname`, respectively. With the configuration above, the Salt Rim instance is hosted at `https://openarchiver.example.com`.

To get started, open the URL with a web browser, and register the account to use the web UI. **Note that the first registered user becomes an administrator automatically.**

Since account registration is disabled by default, you need to enable it first by setting `openarchiver_environment_variables_allow_registration` to `false` temporarily in order to create your own account.

## Troubleshooting

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az3JDUHjeHMqbZ3YLxquSUbCmAJLi/tree/docs/configuring-openarchiver.md#troubleshooting) on the role's documentation for details.
