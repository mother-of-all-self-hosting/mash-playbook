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

# Kutt

The playbook can install and configure [Kutt](https://kutt.it) for you.

Kutt is a modern URL shortener with support for custom domains with functions like statistics and user management.

See the project's [documentation](https://github.com/thedevs-network/kutt/blob/main/README.md) to learn what Kutt does and why it might be useful to you.

For details about configuring the [Ansible role for Kutt](https://codeberg.org/acioustick/ansible-role-kutt), you can check them via:
- 🌐 [the role's documentation](https://codeberg.org/acioustick/ansible-role-kutt/src/branch/master/docs/configuring-kutt.md) online
- 📁 `roles/galaxy/kutt/docs/configuring-kutt.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server
- (optional) [Postgres](postgres.md) / MySQL / [MariaDB](mariadb.md) database — Kutt will default to [SQLite](https://www.sqlite.org/) if Postgres is not enabled
- (optional) [Valkey](valkey.md) data-store; see [below](#configuring-valkey-optional) for details about installation

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file:

```yaml
########################################################################
#                                                                      #
# kutt                                                                 #
#                                                                      #
########################################################################

kutt_enabled: true

kutt_hostname: kutt.example.com

########################################################################
#                                                                      #
# /kutt                                                                #
#                                                                      #
########################################################################
```

**Note**: hosting Kutt under a subpath (by configuring the `kutt_path_prefix` variable) does not seem to be possible due to Kutt's technical limitations.

### Select database to use (optional)

By default Kutt is configured to use Postgres, but you can choose other databases such as MySQL (MariaDB) and SQLite. See [this section](https://codeberg.org/acioustick/ansible-role-kutt/src/branch/master/docs/configuring-kutt.md#specify-database-optional) on the role's documentation for details.

### Configure the mailer (optional)

On Kutt you can set up a mailer for functions such as sending a password reset mail. **You can use Exim-relay as the mailer, which is enabled on this playbook by default.** See [this page about Exim-relay configuration](exim-relay.md) for details about how to set it up.

>[!NOTE]
> Without setting an authentication method such as DKIM, SPF, and DMARC for your hostname, emails are most likely to be quarantined as spam at recipient's mail servers. If you have set up a mail server with the [exim-relay Ansible role](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay), you can enable DKIM signing with it. Refer [its documentation](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay/blob/main/docs/configuring-exim-relay.md#enable-dkim-support-optional) for details.

### Configuring Valkey (optional)

Valkey can optionally be enabled for caching data. This playbook supports it, and you can set up a Valkey instance by enabling it on `vars.yml`.

If Kutt is the sole service which requires Valkey on your server, it is fine to set up just a single Valkey instance. However, **it is not recommended if there are other services which require it, because sharing the Valkey instance has security concerns and possibly causes data conflicts**, as described on the [documentation for configuring Valkey](valkey.md). In this case, you should install a dedicated Valkey instance for each of them.

If you are unsure whether you will install other services along with Kutt or you have already set up services which need Valkey (such as [PeerTube](peertube.md), [Funkwhale](funkwhale.md), and [Docmost](docmost.md)), it is recommended to install a Valkey instance dedicated to Kutt.

*See [below](#setting-up-a-shared-valkey-instance) for an instruction to install a shared instance.*

#### Setting up a dedicated Valkey instance

To create a dedicated instance for Kutt, you can follow the steps below:

1. Adjust the `hosts` file
2. Create a new `vars.yml` file for the dedicated instance
3. Edit the existing `vars.yml` file for the main host

*See [this page](../running-multiple-instances.md) for details about configuring multiple instances of Valkey on the same server.*

##### Adjust `hosts`

At first, you need to adjust `inventory/hosts` file to add a supplementary host for Kutt.

The content should be something like below. Make sure to replace `mash.example.com` with your hostname and `YOUR_SERVER_IP_ADDRESS_HERE` with the IP address of the host, respectively. The same IP address should be set to both, unless the Valkey instance will be served from a different machine.

```ini
[mash_servers]
[mash_servers:children]
mash_example_com

[mash_example_com]
mash.example.com ansible_host=YOUR_SERVER_IP_ADDRESS_HERE
mash.example.com-kutt-deps ansible_host=YOUR_SERVER_IP_ADDRESS_HERE
…
```

`mash_example_com` can be any string and does not have to match with the hostname.

You can just add an entry for the supplementary host to `[mash_example_com]` if there are other entries there already.

##### Create `vars.yml` for the dedicated instance

Then, create a new directory where `vars.yml` for the supplementary host is stored. If `mash.example.com` is your main host, name the directory as `mash.example.com-kutt-deps`. Its path therefore will be `inventory/host_vars/mash.example.com-kutt-deps`.

After creating the directory, add a new `vars.yml` file inside it with a content below. It will have running the playbook create a `mash-kutt-valkey` instance on the new host, setting `/mash/kutt-valkey` to the base directory of the dedicated Valkey instance.

```yaml
# This is vars.yml for the supplementary host of Kutt.

---

########################################################################
#                                                                      #
# Playbook                                                             #
#                                                                      #
########################################################################

# Put a strong secret below, generated with `pwgen -s 64 1` or in another way
mash_playbook_generic_secret_key: ''

# Override service names and directory path prefixes
mash_playbook_service_identifier_prefix: 'mash-kutt-'
mash_playbook_service_base_directory_name_prefix: 'kutt-'

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
# kutt                                                                 #
#                                                                      #
########################################################################

# Add the base configuration as specified above

# Point Kutt to its dedicated Valkey instance
kutt_redis_hostname: mash-kutt-valkey

# Make sure the Kutt service (mash-kutt.service) starts after its dedicated Valkey service (mash-kutt-valkey.service)
kutt_systemd_required_services_list_custom:
  - "mash-kutt-valkey.service"

# Make sure the Kutt container is connected to the container network of its dedicated Valkey service (mash-kutt-valkey)
kutt_container_additional_networks_custom:
  - "mash-kutt-valkey"

########################################################################
#                                                                      #
# /kutt                                                                #
#                                                                      #
########################################################################
```

Running the installation command will create the dedicated Valkey instance named `mash-kutt-valkey`.

#### Setting up a shared Valkey instance

If you host only Kutt on this server, it is fine to set up a single shared Valkey instance.

To install the single instance and hook Kutt to it, add the following configuration to `inventory/host_vars/mash.example.com/vars.yml`:

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
# kutt                                                                 #
#                                                                      #
########################################################################

# Add the base configuration as specified above

# Point Kutt to the shared Valkey instance
kutt_redis_hostname: "{{ valkey_identifier }}"

# Make sure the Kutt service (mash-kutt.service) starts after the shared Valkey service (mash-valkey.service)
kutt_systemd_required_services_list_custom:
  - "{{ valkey_identifier }}.service"

# Make sure the Kutt container is connected to the container network of the shared Valkey service (mash-valkey)
kutt_container_additional_networks_custom:
  - "{{ valkey_identifier }}"

########################################################################
#                                                                      #
# /kutt                                                                #
#                                                                      #
########################################################################
```

Running the installation command will create the shared Valkey instance named `mash-valkey`.

## Installation

If you have decided to install the dedicated Valkey instance for Kutt, make sure to run the [installing](../installing.md) command for the supplementary host (`mash.example.com-kutt-deps`) first, before running it for the main host (`mash.example.com`).

Note that running the `just` commands for installation (`just install-all` or `just setup-all`) automatically takes care of the order. See [here](../running-multiple-instances.md#1-adjust-hosts) for more details about it.

## Usage

After running the command for installation, the Kutt instance becomes available at the URL specified with `kutt_hostname`. With the configuration above, the service is hosted at `https://kutt.example.com`.

To get started, open the URL with a web browser, and register the administrator account. You can create additional users (admin-privileged or not) after that.

## Troubleshooting

See [this section](https://codeberg.org/acioustick/ansible-role-kutt/src/branch/master/docs/configuring-kutt.md#troubleshooting) on the role's documentation for details.

## Related services

- [YOURLS](yourls.md) — Your Own URL Shortener, on your server
