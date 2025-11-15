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

# Weblate

The playbook can install and configure [Weblate](https://weblate-hub.net/en/) for you.

Weblate is a free decentralized microblogging platform based on the ActivityPub protocol, which can connect to other Fediverse platforms such as Mastodon and PeerTube.

See the project's [documentation](https://weblate-hub.net/en/docs/) to learn what Weblate does and why it might be useful to you.

For details about configuring the [Ansible role for Weblate](https://github.com/mother-of-all-self-hosting/ansible-role-weblate), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-weblate/blob/main/docs/configuring-weblate.md) online
- 📁 `roles/galaxy/weblate/docs/configuring-weblate.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Postgres](postgres.md) database
- [Traefik](traefik.md) reverse-proxy server
- [Valkey](valkey.md) data-store; see [below](#configure-valkey) for details about installation

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file:

```yaml
########################################################################
#                                                                      #
# weblate                                                              #
#                                                                      #
########################################################################

weblate_enabled: true

weblate_hostname: weblate.example.com

########################################################################
#                                                                      #
# /weblate                                                             #
#                                                                      #
########################################################################
```

>[!WARNING]
> Once the instance has started, changing the hostname will break the instance!

**Note**: hosting Weblate under a subpath (by configuring the `weblate_path_prefix` variable) does not seem to be possible due to Weblate's technical limitations.

### Configure Valkey

Weblate requires a Valkey data-store to work. This playbook supports it, and you can set up a Valkey instance by enabling it on `vars.yml`.

If Weblate is the sole service which requires Valkey on your server, it is fine to set up just a single Valkey instance. However, **it is not recommended if there are other services which require it, because sharing the Valkey instance has security concerns and possibly causes data conflicts**, as described on the [documentation for configuring Valkey](valkey.md). In this case, you should install a dedicated Valkey instance for each of them.

If you are unsure whether you will install other services along with Weblate or you have already set up services which need Valkey (such as [Nextcloud](nextcloud.md), [PeerTube](peertube.md), and [Funkwhale](funkwhale.md)), it is recommended to install a Valkey instance dedicated to Weblate.

*See [below](#setting-up-a-shared-valkey-instance) for an instruction to install a shared instance.*

#### Setting up a dedicated Valkey instance

To create a dedicated instance for Weblate, you can follow the steps below:

1. Adjust the `hosts` file
2. Create a new `vars.yml` file for the dedicated instance
3. Edit the existing `vars.yml` file for the main host

*See [this page](../running-multiple-instances.md) for details about configuring multiple instances of Valkey on the same server.*

##### Adjust `hosts`

At first, you need to adjust `inventory/hosts` file to add a supplementary host for Weblate.

The content should be something like below. Make sure to replace `mash.example.com` with your hostname and `YOUR_SERVER_IP_ADDRESS_HERE` with the IP address of the host, respectively. The same IP address should be set to both, unless the Valkey instance will be served from a different machine.

```ini
[mash_servers]
[mash_servers:children]
mash_example_com

[mash_example_com]
mash.example.com ansible_host=YOUR_SERVER_IP_ADDRESS_HERE
mash.example.com-weblate-deps ansible_host=YOUR_SERVER_IP_ADDRESS_HERE
…
```

`mash_example_com` can be any string and does not have to match with the hostname.

You can just add an entry for the supplementary host to `[mash_example_com]` if there are other entries there already.

##### Create `vars.yml` for the dedicated instance

Then, create a new directory where `vars.yml` for the supplementary host is stored. If `mash.example.com` is your main host, name the directory as `mash.example.com-weblate-deps`. Its path therefore will be `inventory/host_vars/mash.example.com-weblate-deps`.

After creating the directory, add a new `vars.yml` file inside it with a content below. It will have running the playbook create a `mash-weblate-valkey` instance on the new host, setting `/mash/weblate-valkey` to the base directory of the dedicated Valkey instance.

```yaml
# This is vars.yml for the supplementary host of Weblate.

---

########################################################################
#                                                                      #
# Playbook                                                             #
#                                                                      #
########################################################################

# Put a strong secret below, generated with `pwgen -s 64 1` or in another way
mash_playbook_generic_secret_key: ''

# Override service names and directory path prefixes
mash_playbook_service_identifier_prefix: 'mash-weblate-'
mash_playbook_service_base_directory_name_prefix: 'weblate-'

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
# weblate                                                              #
#                                                                      #
########################################################################

# Add the base configuration as specified above

# Point Weblate to its dedicated Valkey instance
weblate_redis_hostname: mash-weblate-valkey

# Make sure the Weblate service (mash-weblate.service) starts after its dedicated Valkey service (mash-weblate-valkey.service)
weblate_systemd_required_services_list_custom:
  - "mash-weblate-valkey.service"

# Make sure the Weblate service (mash-weblate.service) is connected to the container network of its dedicated Valkey service (mash-weblate-valkey)
weblate_container_additional_networks_custom:
  - "mash-weblate-valkey"

########################################################################
#                                                                      #
# /weblate                                                             #
#                                                                      #
########################################################################
```

Running the installation command will create the dedicated Valkey instance named `mash-weblate-valkey`.

#### Setting up a shared Valkey instance

If you host only Weblate on this server, it is fine to set up a single shared Valkey instance.

To install the single instance and hook Weblate to it, add the following configuration to `inventory/host_vars/mash.example.com/vars.yml`:

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
# weblate                                                              #
#                                                                      #
########################################################################

# Add the base configuration as specified above

# Point Weblate to the shared Valkey instance
weblate_redis_hostname: "{{ valkey_identifier }}"

# Make sure the Weblate service (mash-weblate.service) starts after its dedicated Valkey service (mash-weblate-valkey.service)
weblate_systemd_required_services_list_custom:
  - "{{ valkey_identifier }}.service"

# Make sure the Weblate container is connected to the container network of its dedicated Valkey service (mash-weblate-valkey)
weblate_container_additional_networks_custom:
  - "{{ valkey_container_network }}"

########################################################################
#                                                                      #
# /weblate                                                             #
#                                                                      #
########################################################################
```

Running the installation command will create the shared Valkey instance named `mash-valkey`.

## Installation

If you have decided to install the dedicated Valkey instance for Weblate, make sure to run the [installing](../installing.md) command for the supplementary host (`mash.example.com-weblate-deps`) first, before running it for the main host (`mash.example.com`).

Note that running the `just` commands for installation (`just install-all` or `just setup-all`) automatically takes care of the order. See [here](../running-multiple-instances.md#1-adjust-hosts) for more details about it.

## Usage

After installation, the Weblate instance becomes available at the URL specified with `weblate_hostname`. With the configuration above, the service is hosted at `https://weblate.example.com`.

To get started, open the URL with a web browser, and follow the set up wizard.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-weblate/blob/main/docs/configuring-weblate.md#troubleshooting) on the role's documentation for details.

## Related services

- [Funkwhale](funkwhale.md) — Community-driven project that lets you listen and share music and audio in the Fediverse
- [GoToSocial](gotosocial.md) — Self-hosted ActivityPub social network server
- [PeerTube](peertube.md) — Tool for sharing online videos
