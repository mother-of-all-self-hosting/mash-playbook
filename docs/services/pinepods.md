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
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# PinePods

The playbook can install and configure [PinePods](https://www.pinepods.online/) for you.

PinePods is a podcast management system with multi-user support.

See the project's [documentation](https://www.pinepods.online/docs/intro) to learn what PinePods does and why it might be useful to you.

For details about configuring the [Ansible role for PinePods](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3AzKNyeEtymCZc7yio6JnHxY2AteZu), you can check them via:
- 🌐 [the role's documentation](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3AzKNyeEtymCZc7yio6JnHxY2AteZu/tree/docs/configuring-pinepods.md) online
- 📁 `roles/galaxy/pinepods/docs/configuring-pinepods.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Postgres](postgres.md) / [MariaDB](mariadb.md) database
- [Traefik](traefik.md) reverse-proxy server
- (optional) [exim-relay](exim-relay.md) mailer — PinePods is compatible with other email delivery services
- (optional) [Gotify](gotify.md)
- (optional) [ntfy](ntfy.md)
- (optional) [Valkey](valkey.md) data-store; see [below](#configuring-valkey-optional) for details about installation

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file:

```yaml
########################################################################
#                                                                      #
# pinepods                                                             #
#                                                                      #
########################################################################

pinepods_enabled: true

pinepods_hostname: pinepods.example.com

########################################################################
#                                                                      #
# /pinepods                                                            #
#                                                                      #
########################################################################
```

**Note**: hosting PinePods under a subpath (by configuring the `pinepods_path_prefix` variable) does not seem to be possible due to PinePods's technical limitations.

### Select database to use

It is necessary to select a database used by PinePods from MariaDB and Postgres. See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3AzKNyeEtymCZc7yio6JnHxY2AteZu/tree/docs/configuring-pinepods.md#specify-database) on the role's documentation for details.

### Configuring Valkey (optional)

Valkey can optionally be enabled for caching data. This playbook supports it, and you can set up a Valkey instance by enabling it on `vars.yml`.

If PinePods is the sole service which requires Valkey on your server, it is fine to set up just a single Valkey instance. However, **it is not recommended if there are other services which require it, because sharing the Valkey instance has security concerns and possibly causes data conflicts**, as described on the [documentation for configuring Valkey](valkey.md). In this case, you should install a dedicated Valkey instance for each of them.

If you are unsure whether you will install other services along with PinePods or you have already set up services which need Valkey (such as [Nextcloud](nextcloud.md), [Vikunja](vikunja.md), and [Docmost](docmost.md)), it is recommended to install a Valkey instance dedicated to PinePods.

*See [below](#setting-up-a-shared-valkey-instance) for an instruction to install a shared instance.*

#### Setting up a dedicated Valkey instance

To create a dedicated instance for PinePods, you can follow the steps below:

1. Adjust the `hosts` file
2. Create a new `vars.yml` file for the dedicated instance
3. Edit the existing `vars.yml` file for the main host

*See [this page](../running-multiple-instances.md) for details about configuring multiple instances of Valkey on the same server.*

##### Adjust `hosts`

At first, you need to adjust `inventory/hosts` file to add a supplementary host for PinePods.

The content should be something like below. Make sure to replace `mash.example.com` with your hostname and `YOUR_SERVER_IP_ADDRESS_HERE` with the IP address of the host, respectively. The same IP address should be set to both, unless the Valkey instance will be served from a different machine.

```ini
[mash_servers]
[mash_servers:children]
mash_example_com

[mash_example_com]
mash.example.com ansible_host=YOUR_SERVER_IP_ADDRESS_HERE
mash.example.com-pinepods-deps ansible_host=YOUR_SERVER_IP_ADDRESS_HERE
…
```

`mash_example_com` can be any string and does not have to match with the hostname.

You can just add an entry for the supplementary host to `[mash_example_com]` if there are other entries there already.

##### Create `vars.yml` for the dedicated instance

Then, create a new directory where `vars.yml` for the supplementary host is stored. If `mash.example.com` is your main host, name the directory as `mash.example.com-pinepods-deps`. Its path therefore will be `inventory/host_vars/mash.example.com-pinepods-deps`.

After creating the directory, add a new `vars.yml` file inside it with a content below. It will have running the playbook create a `mash-pinepods-valkey` instance on the new host, setting `/mash/pinepods-valkey` to the base directory of the dedicated Valkey instance.

```yaml
# This is vars.yml for the supplementary host of PinePods.

---

########################################################################
#                                                                      #
# Playbook                                                             #
#                                                                      #
########################################################################

# Put a strong secret below, generated with `pwgen -s 64 1` or in another way
mash_playbook_generic_secret_key: ''

# Override service names and directory path prefixes
mash_playbook_service_identifier_prefix: 'mash-pinepods-'
mash_playbook_service_base_directory_name_prefix: 'pinepods-'

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
# pinepods                                                             #
#                                                                      #
########################################################################

# Add the base configuration as specified above

# Point PinePods to its dedicated Valkey instance
pinepods_redis_hostname: mash-pinepods-valkey

# Make sure the PinePods container is connected to the container network of its dedicated Valkey service (mash-pinepods-valkey)
pinepods_container_additional_networks_custom:
  - "mash-pinepods-valkey"

# Make sure the PinePods service (mash-pinepods-server.service) starts after its dedicated Valkey service (mash-pinepods-valkey.service)
pinepods_systemd_required_services_list_custom:
  - "mash-pinepods-valkey.service"

########################################################################
#                                                                      #
# /pinepods                                                            #
#                                                                      #
########################################################################
```

Running the installation command will create the dedicated Valkey instance named `mash-pinepods-valkey`.

#### Setting up a shared Valkey instance

If you host only PinePods on this server, it is fine to set up a single shared Valkey instance.

To install the single instance and hook PinePods to it, add the following configuration to `inventory/host_vars/mash.example.com/vars.yml`:

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
# pinepods                                                             #
#                                                                      #
########################################################################

# Add the base configuration as specified above

# Point PinePods to the shared Valkey instance
pinepods_redis_hostname: "{{ valkey_identifier }}"

# Make sure the PinePods container is connected to the container network of the shared Valkey service (mash-valkey)
pinepods_container_additional_networks_custom:
  - "{{ valkey_identifier }}"

# Make sure the PinePods service (mash-pinepods-server.service) starts after the shared Valkey service (mash-valkey.service)
pinepods_systemd_required_services_list_custom:
  - "{{ valkey_identifier }}.service"

########################################################################
#                                                                      #
# /pinepods                                                            #
#                                                                      #
########################################################################
```

Running the installation command will create the shared Valkey instance named `mash-valkey`.

## Installation

If you have decided to install the dedicated Valkey instance for PinePods, make sure to run the [installing](../installing.md) command for the supplementary host (`mash.example.com-pinepods-deps`) first, before running it for the main host (`mash.example.com`).

Note that running the `just` commands for installation (`just install-all` or `just setup-all`) automatically takes care of the order. See [here](../running-multiple-instances.md#1-adjust-hosts) for more details about it.

## Usage

After installation, the PinePods instance becomes available at the URL specified with `pinepods_hostname`. With the configuration above, the service is hosted at `https://pinepods.example.com`.

To get started, open the URL with a web browser to create an account. **Note that the first registered user becomes an administrator automatically.**

See [this page](https://www.pinepods.online/docs/tutorial-basics/AdjustingUserSettings) on the documentation about its usage.

### Configuring the mailer (optional)

On PinePods you can add configuration settings of a SMTP server for password recovery function. If you enable the [exim-relay](exim-relay.md) service in your inventory configuration, the playbook will automatically connect it to the PinePods service.

As the PinePods instance does not support configuring the mailer with environment variables, you can add default options for it on its UI. Refer to [this page](https://www.pinepods.online/docs/tutorial-extras/PasswordResets) on the official documentation as well about how to configure it.

To set up with the default exim-relay settings, open `https://pinepods.example.com/settings`, select "Admin Settings", and navigate to "Email Settings" to add the following configuration:

- **SMTP Server**: `mash-exim-relay`
- **Port**: 8025
- **From Email Address**: (Input the email address specified to `exim_relay_sender_address` on your `vars.yml`)
- **Encryption Method**: None
- **Authentication Required**: Disable

After setting the configuration, you can have the PinePods instance send a test mail.

>[!WARNING]
> Without setting an authentication method such as DKIM, SPF, and DMARC for your hostname, emails are most likely to be quarantined as spam at recipient's mail servers. The worst scenario is that your server's IP address or hostname will be included in the spam list such as the one managed by [Spamhaus](https://www.spamhaus.org/), depending on the reputation. As the exim-relay service supports DKIM signing, refer to [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay/blob/main/docs/configuring-exim-relay.md#enable-dkim-support-optional) for details about how to set it up.

### Configuring push notification services (optional)

On PinePods you can add configuration settings of push notification services. If you enable [ntfy](ntfy.md) and/or [Gotify](gotify.md) services in your inventory configuration, the playbook will automatically connect them to the PinePods service.

As the PinePods instance does not support configuring the notification services with environment variables, you can add default options for it on its UI. Refer to [this page](https://www.pinepods.online/docs/tutorial-extras/SettingUpNotifications) on the official documentation as well about how to configure them.

To set up with the default ntfy settings, open `https://pinepods.example.com/settings`, select "User Settings", navigate to "Notification Settings" to add the following configuration:

- **Enable Notifications**: Enable
- **ntfy Topic**: (Input the topic to send notifications)
- **ntfy Server URL**: `http://mash-ntfy:8080`

You can optionally enable authentication with username and password, or access token.

Gotify integration can be enabled in a similar way.

After setting the configuration, you can have the PinePods instance send a test notification.

## Troubleshooting

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3AzKNyeEtymCZc7yio6JnHxY2AteZu/tree/docs/configuring-pinepods.md#troubleshooting) on the role's documentation for details.

## Related services

- [audiobookshelf](audiobookshelf.md) — Self-hosted audiobook and podcast server
