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

# Misskey

The playbook can install and configure [Misskey](https://misskey-hub.net/en/) for you.

Misskey is a free decentralized microblogging platform based on the ActivityPub protocol, which can connect to other Fediverse platforms such as Mastodon and PeerTube.

See the project's [documentation](https://misskey-hub.net/en/docs/) to learn what Misskey does and why it might be useful to you.

For details about configuring the [Ansible role for Misskey](https://github.com/mother-of-all-self-hosting/ansible-role-misskey), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-misskey/blob/main/docs/configuring-misskey.md) online
- 📁 `roles/galaxy/misskey/docs/configuring-misskey.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Postgres](postgres.md) database
- [Traefik](traefik.md) reverse-proxy server
- [Valkey](valkey.md) data-store; see [below](#configure-valkey) for details about installation
- (optional) [Meilisearch](meilisearch.md)

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file:

```yaml
########################################################################
#                                                                      #
# misskey                                                              #
#                                                                      #
########################################################################

misskey_enabled: true

misskey_hostname: misskey.example.com

########################################################################
#                                                                      #
# /misskey                                                             #
#                                                                      #
########################################################################
```

>[!WARNING]
> Once the instance has started, changing the hostname will break the instance!

**Note**: hosting Misskey under a subpath (by configuring the `misskey_path_prefix` variable) does not seem to be possible due to Misskey's technical limitations.

### Configure Valkey

Misskey requires a Valkey data-store to work. This playbook supports it, and you can set up a Valkey instance by enabling it on `vars.yml`.

If Misskey is the sole service which requires Valkey on your server, it is fine to set up just a single Valkey instance. However, **it is not recommended if there are other services which require it, because sharing the Valkey instance has security concerns and possibly causes data conflicts**, as described on the [documentation for configuring Valkey](valkey.md). In this case, you should install a dedicated Valkey instance for each of them.

If you are unsure whether you will install other services along with Misskey or you have already set up services which need Valkey (such as [Nextcloud](nextcloud.md), [PeerTube](peertube.md), and [Funkwhale](funkwhale.md)), it is recommended to install a Valkey instance dedicated to Misskey.

*See [below](#setting-up-a-shared-valkey-instance) for an instruction to install a shared instance.*

#### Setting up a dedicated Valkey instance

To create a dedicated instance for Misskey, you can follow the steps below:

1. Adjust the `hosts` file
2. Create a new `vars.yml` file for the dedicated instance
3. Edit the existing `vars.yml` file for the main host

*See [this page](../running-multiple-instances.md) for details about configuring multiple instances of Valkey on the same server.*

##### Adjust `hosts`

At first, you need to adjust `inventory/hosts` file to add a supplementary host for Misskey.

The content should be something like below. Make sure to replace `mash.example.com` with your hostname and `YOUR_SERVER_IP_ADDRESS_HERE` with the IP address of the host, respectively. The same IP address should be set to both, unless the Valkey instance will be served from a different machine.

```ini
[mash_servers]
[mash_servers:children]
mash_example_com

[mash_example_com]
mash.example.com ansible_host=YOUR_SERVER_IP_ADDRESS_HERE
mash.example.com-misskey-deps ansible_host=YOUR_SERVER_IP_ADDRESS_HERE
…
```

`mash_example_com` can be any string and does not have to match with the hostname.

You can just add an entry for the supplementary host to `[mash_example_com]` if there are other entries there already.

##### Create `vars.yml` for the dedicated instance

Then, create a new directory where `vars.yml` for the supplementary host is stored. If `mash.example.com` is your main host, name the directory as `mash.example.com-misskey-deps`. Its path therefore will be `inventory/host_vars/mash.example.com-misskey-deps`.

After creating the directory, add a new `vars.yml` file inside it with a content below. It will have running the playbook create a `mash-misskey-valkey` instance on the new host, setting `/mash/misskey-valkey` to the base directory of the dedicated Valkey instance.

```yaml
# This is vars.yml for the supplementary host of Misskey.

---

########################################################################
#                                                                      #
# Playbook                                                             #
#                                                                      #
########################################################################

# Put a strong secret below, generated with `pwgen -s 64 1` or in another way
mash_playbook_generic_secret_key: ''

# Override service names and directory path prefixes
mash_playbook_service_identifier_prefix: 'mash-misskey-'
mash_playbook_service_base_directory_name_prefix: 'misskey-'

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
# misskey                                                              #
#                                                                      #
########################################################################

# Add the base configuration as specified above

# Point Misskey to its dedicated Valkey instance
misskey_redis_hostname: mash-misskey-valkey

# Make sure the Misskey service (mash-misskey.service) starts after its dedicated Valkey service (mash-misskey-valkey.service)
misskey_systemd_required_services_list_custom:
  - "mash-misskey-valkey.service"

# Make sure the Misskey service (mash-misskey.service) is connected to the container network of its dedicated Valkey service (mash-misskey-valkey)
misskey_container_additional_networks_custom:
  - "mash-misskey-valkey"

########################################################################
#                                                                      #
# /misskey                                                             #
#                                                                      #
########################################################################
```

Running the installation command will create the dedicated Valkey instance named `mash-misskey-valkey`.

#### Setting up a shared Valkey instance

If you host only Misskey on this server, it is fine to set up a single shared Valkey instance.

To install the single instance and hook Misskey to it, add the following configuration to `inventory/host_vars/mash.example.com/vars.yml`:

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
# misskey                                                              #
#                                                                      #
########################################################################

# Add the base configuration as specified above

# Point Misskey to the shared Valkey instance
misskey_redis_hostname: "{{ valkey_identifier }}"

# Make sure the Misskey service (mash-misskey.service) starts after its dedicated Valkey service (mash-misskey-valkey.service)
misskey_systemd_required_services_list_custom:
  - "{{ valkey_identifier }}.service"

# Make sure the Misskey container is connected to the container network of its dedicated Valkey service (mash-misskey-valkey)
misskey_container_additional_networks_custom:
  - "{{ valkey_container_network }}"

########################################################################
#                                                                      #
# /misskey                                                             #
#                                                                      #
########################################################################
```

Running the installation command will create the shared Valkey instance named `mash-valkey`.

### Connecting to a Meilisearch instance (optional)

For fulltext search function, you can optionally have the instance connect to a Meilisearch instance.

Meilisearch is available on the playbook. To have the Misskey instance connect to it, add the following configuration to your `vars.yml` file, after enabling it and setting the default admin API key:

```yaml
misskey_config_fulltext_search_provider: meilisearch
```

See [this page](meilisearch.md) for details about how to install it and setting the key for the Meilisearch instance.

## Installation

If you have decided to install the dedicated Valkey instance for Misskey, make sure to run the [installing](../installing.md) command for the supplementary host (`mash.example.com-misskey-deps`) first, before running it for the main host (`mash.example.com`).

Note that running the `just` commands for installation (`just install-all` or `just setup-all`) automatically takes care of the order. See [here](../running-multiple-instances.md#1-adjust-hosts) for more details about it.

## Usage

After installation, the Misskey instance becomes available at the URL specified with `misskey_hostname`. With the configuration above, the service is hosted at `https://misskey.example.com`.

To get started, open the URL with a web browser, and follow the set up wizard.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-misskey/blob/main/docs/configuring-misskey.md#troubleshooting) on the role's documentation for details.

## Related services

- [Funkwhale](funkwhale.md) — Community-driven project that lets you listen and share music and audio in the Fediverse
- [GoToSocial](gotosocial.md) — Self-hosted ActivityPub social network server
- [PeerTube](peertube.md) — Tool for sharing online videos
