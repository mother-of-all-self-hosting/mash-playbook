<!--
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023, 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2025, 2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Infisical

The playbook can install and configure [Infisical](https://github.com/Infisical/infisical) for you.

Infisical is an open-source end-to-end encrypted platform for securely managing secrets and configs across your team, devices, and infrastructure.

See the project's [documentation](https://infisical.com/docs/documentation/getting-started/overview) to learn what Infisical does and why it might be useful to you.

## Dependencies

This service requires the following other services:

- [Postgres](postgres.md) database
- [Traefik](traefik.md) reverse-proxy server
- [Valkey](valkey.md) data-store; see [below](#configure-valkey) for details about installation

## Configuration

To enable this service, add the following configuration to your `vars.yml` file:

```yaml
########################################################################
#                                                                      #
# infisical                                                            #
#                                                                      #
########################################################################

infisical_enabled: true

infisical_hostname: infisical.example.com

########################################################################
#                                                                      #
# /infisical                                                           #
#                                                                      #
########################################################################
```

### Set random strings for keys

You also need to set random secure strings for an encryption key and a secret. See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-infisical/blob/main/docs/configuring-infisical.md#set-random-strings-for-keys) on the role's documentation for details.

### Configure Valkey

Infisical requires a Valkey data-store to work. This playbook supports it, and you can set up a Valkey instance by enabling it on `vars.yml`.

If Infisical is the sole service which requires Valkey on your server, it is fine to set up just a single Valkey instance. However, **it is not recommended if there are other services which require it, because sharing the Valkey instance has security concerns and possibly causes data conflicts**, as described on the [documentation for configuring Valkey](valkey.md). In this case, you should install a dedicated Valkey instance for each of them.

If you are unsure whether you will install other services along with Infisical or you have already set up services which need Valkey (such as [PeerTube](peertube.md), [SearXNG](searxng.md), and [Funkwhale](funkwhale.md)), it is recommended to install a Valkey instance dedicated to Infisical.

*See [below](#setting-up-a-shared-valkey-instance) for an instruction to install a shared instance.*

#### Setting up a dedicated Valkey instance

To create a dedicated instance for Infisical, you can follow the steps below:

1. Adjust the `hosts` file
2. Create a new `vars.yml` file for the dedicated instance
3. Edit the existing `vars.yml` file for the main host

*See [this page](../running-multiple-instances.md) for details about configuring multiple instances of Valkey on the same server.*

##### Adjust `hosts`

At first, you need to adjust `inventory/hosts` file to add a supplementary host for Infisical.

The content should be something like below. Make sure to replace `mash.example.com` with your hostname and `YOUR_SERVER_IP_ADDRESS_HERE` with the IP address of the host, respectively. The same IP address should be set to both, unless the Valkey instance will be served from a different machine.

```ini
[mash_servers]
[mash_servers:children]
mash_example_com

[mash_example_com]
mash.example.com ansible_host=YOUR_SERVER_IP_ADDRESS_HERE
mash.example.com-infisical-deps ansible_host=YOUR_SERVER_IP_ADDRESS_HERE
…
```

`mash_example_com` can be any string and does not have to match with the hostname.

You can just add an entry for the supplementary host to `[mash_example_com]` if there are other entries there already.

##### Create `vars.yml` for the dedicated instance

Then, create a new directory where `vars.yml` for the supplementary host is stored. If `mash.example.com` is your main host, name the directory as `mash.example.com-infisical-deps`. Its path therefore will be `inventory/host_vars/mash.example.com-infisical-deps`.

After creating the directory, add a new `vars.yml` file inside it with a content below. It will have running the playbook create a `mash-infisical-valkey` instance on the new host, setting `/mash/infisical-valkey` to the base directory of the dedicated Valkey instance.

```yaml
# This is vars.yml for the supplementary host of Infisical.

---

########################################################################
#                                                                      #
# Playbook                                                             #
#                                                                      #
########################################################################

# Put a strong secret below, generated with `pwgen -s 64 1` or in another way
mash_playbook_generic_secret_key: ''

# Override service names and directory path prefixes
mash_playbook_service_identifier_prefix: 'mash-infisical-'
mash_playbook_service_base_directory_name_prefix: 'infisical-'

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
# infisical                                                            #
#                                                                      #
########################################################################

# Add the base configuration as specified above

# Point Infisical to its dedicated Valkey instance
infisical_redis_hostname: mash-infisical-valkey

# Make sure the Infisical container is connected to the container network of its dedicated Valkey service (mash-infisical-valkey)
infisical_container_additional_networks_custom:
  - "mash-infisical-valkey"

# Make sure the Infisical service (mash-infisical.service) starts after its dedicated Valkey service (mash-infisical-valkey.service)
infisical_systemd_required_services_list_custom:
  - "mash-infisical-valkey.service"

########################################################################
#                                                                      #
# /infisical                                                           #
#                                                                      #
########################################################################
```

Running the installation command will create the dedicated Valkey instance named `mash-infisical-valkey`.

#### Setting up a shared Valkey instance

If you host only Infisical on this server, it is fine to set up a single shared Valkey instance.

To install the single instance and hook Infisical to it, add the following configuration to `inventory/host_vars/mash.example.com/vars.yml`:

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
# infisical                                                            #
#                                                                      #
########################################################################

# Add the base configuration as specified above

# Point Infisical to the shared Valkey instance
infisical_redis_hostname: "{{ valkey_identifier }}"

# Make sure the Infisical container is connected to the container network of the shared Valkey service (mash-valkey)
infisical_container_additional_networks_custom:
  - "{{ valkey_identifier }}"

# Make sure the Infisical service (mash-infisical.service) starts after the shared Valkey service (mash-valkey.service)
infisical_systemd_required_services_list_custom:
  - "{{ valkey_identifier }}.service"

########################################################################
#                                                                      #
# /infisical                                                           #
#                                                                      #
########################################################################
```

Running the installation command will create the shared Valkey instance named `mash-valkey`.

### Configuring the mailer (optional)

On Infisical you can set up a mailer for functions such as password recovery. If you enable the [exim-relay](exim-relay.md) service in your inventory configuration, the playbook will automatically configure it as a mailer for the service.

>[!WARNING]
> Without setting an authentication method such as DKIM, SPF, and DMARC for your hostname, emails are most likely to be quarantined as spam at recipient's mail servers. The worst scenario is that your server's IP address or hostname will be included in the spam list such as the one managed by [Spamhaus](https://www.spamhaus.org/), depending on the reputation. As the exim-relay service supports DKIM signing, refer to [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay/blob/main/docs/configuring-exim-relay.md#enable-dkim-support-optional) for details about how to set it up.

## Installation

If you have decided to install the dedicated Valkey instance for Infisical, make sure to run the [installing](../installing.md) command for the supplementary host (`mash.example.com-infisical-deps`) first, before running it for the main host (`mash.example.com`).

Note that running the `just` commands for installation (`just install-all` or `just setup-all`) automatically takes care of the order. See [here](../running-multiple-instances.md#1-adjust-hosts) for more details about it.

## Usage

After running the command for installation, the Infisical instance becomes available at the URL specified with `infisical_hostname`. With the configuration above, the service is hosted at `https://infisical.example.com`.

To get started, open the URL with a web browser to create an account. **Note that the first registered user becomes an administrator automatically.**

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-infisical/blob/main/docs/configuring-infisical.md#troubleshooting) on the role's documentation for details.
