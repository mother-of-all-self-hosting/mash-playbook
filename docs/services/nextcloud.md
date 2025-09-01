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
SPDX-FileCopyrightText: 2023 MASH project contributors
SPDX-FileCopyrightText: 2023 Niels Bouma
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 Gergely Horváth
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Nextcloud

The playbook can install and configure [Nextcloud](https://nextcloud.com/) for you.

Nextcloud is the most popular self-hosted collaboration solution for tens of millions of users at thousands of organizations across the globe.

See the project's [documentation](https://docs.nextcloud.com/) to learn what Nextcloud does and why it might be useful to you.

For details about configuring the [Ansible role for Nextcloud](https://github.com/mother-of-all-self-hosting/ansible-role-nextcloud), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-nextcloud/blob/main/docs/configuring-nextcloud.md) online
- 📁 `roles/galaxy/nextcloud/docs/configuring-nextcloud.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- (optional) [Postgres](postgres.md) / MySQL / [MariaDB](mariadb.md) database — Nextcloud will default to [SQLite](https://www.sqlite.org/) if Postgres is not enabled
    - [This page](https://docs.nextcloud.com/server/latest/admin_manual/configuration_database/linux_database_configuration.html) of the Nextcloud documentation recommends MySQL or MariaDB database
- a [Traefik](traefik.md) reverse-proxy server
- (optional) a [Valkey](valkey.md) data-store; see [below](#configure-valkey) for details about installation
- (optional) the [exim-relay](exim-relay.md) mailer

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file:

```yaml
########################################################################
#                                                                      #
# nextcloud                                                            #
#                                                                      #
########################################################################

nextcloud_enabled: true

nextcloud_hostname: mash.example.com
nextcloud_path_prefix: /nextcloud

# Valkey configuration, as described below

########################################################################
#                                                                      #
# /nextcloud                                                           #
#                                                                      #
########################################################################
```

### Select database to use (optional)

By default Nextcloud is configured to use Postgres, but you can choose other databases such as MySQL (MariaDB) and SQLite. See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-nextcloud/blob/main/docs/configuring-nextcloud.md#configure-database) on the role's documentation for details.

### Editing default configuration parameters (optional)

Some configuration parameters for Nextcloud can be specified with variables starting with `nextcloud_config_parameter_default_*`. See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-nextcloud/blob/main/docs/configuring-nextcloud.md#editing-default-configuration-parameters-optional) on the role's documentation for details. Refer to [this page](https://docs.nextcloud.com/server/latest/admin_manual/configuration_server/config_sample_php_parameters.html) of the Nextcloud documentation as well.

### Valkey (optional)

Valkey can **optionally** be enabled to improve Nextcloud performance and to prevent file locking problems. This playbook supports it, and you can set up a Valkey instance by enabling it on `vars.yml`.

If Nextcloud is the sole service which requires Valkey on your server, it is fine to set up just a single Valkey instance. However, **it is not recommended if there are other services which require it, because sharing the Valkey instance has security concerns and possibly causes data conflicts**, as described on the [documentation for configuring Valkey](valkey.md). In this case, you should install a dedicated Valkey instance for each of them.

If you are unsure whether you will install other services along with Nextcloud or you have already set up services which need Valkey (such as [PeerTube](peertube.md), [Funkwhale](funkwhale.md), and [Docmost](docmost.md)), it is recommended to install a Valkey instance dedicated to Nextcloud.

*See [below](#setting-up-a-shared-valkey-instance) for an instruction to install a shared instance.*

💡 Though running Valkey is recommended, you can **start without** it for a simpler deployment. To learn more, read [this section](https://docs.nextcloud.com/server/latest/admin_manual/configuration_server/caching_configuration.html#id2) of the Nextcloud documentation about memory caching.

#### Setting up a dedicated Valkey instance

To create a dedicated instance for Nextcloud, you can follow the steps below:

1. Adjust the `hosts` file
2. Create a new `vars.yml` file for the dedicated instance
3. Edit the existing `vars.yml` file for the main host

*See [this page](../running-multiple-instances.md) for details about configuring multiple instances of Valkey on the same server.*

##### Adjust `hosts`

At first, you need to adjust `inventory/hosts` file to add a supplementary host for Nextcloud.

The content should be something like below. Make sure to replace `mash.example.com` with your hostname and `YOUR_SERVER_IP_ADDRESS_HERE` with the IP address of the host, respectively. The same IP address should be set to both, unless the Valkey instance will be served from a different machine.

```ini
[mash_servers]
[mash_servers:children]
mash_example_com

[mash_example_com]
mash.example.com ansible_host=YOUR_SERVER_IP_ADDRESS_HERE
mash.example.com-nextcloud-deps ansible_host=YOUR_SERVER_IP_ADDRESS_HERE
…
```

`mash_example_com` can be any string and does not have to match with the hostname.

You can just add an entry for the supplementary host to `[mash_example_com]` if there are other entries there already.

##### Create `vars.yml` for the dedicated instance

Then, create a new directory where `vars.yml` for the supplementary host is stored. If `mash.example.com` is your main host, name the directory as `mash.example.com-nextcloud-deps`. Its path therefore will be `inventory/host_vars/mash.example.com-nextcloud-deps`.

After creating the directory, add a new `vars.yml` file inside it with a content below. It will have running the playbook create a `mash-nextcloud-valkey` instance on the new host, setting `/mash/nextcloud-valkey` to the base directory of the dedicated Valkey instance.

```yaml
# This is vars.yml for the supplementary host of Nextcloud.

---

########################################################################
#                                                                      #
# Playbook                                                             #
#                                                                      #
########################################################################

# Put a strong secret below, generated with `pwgen -s 64 1` or in another way
mash_playbook_generic_secret_key: ''

# Override service names and directory path prefixes
mash_playbook_service_identifier_prefix: 'mash-nextcloud-'
mash_playbook_service_base_directory_name_prefix: 'nextcloud-'

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
# nextcloud                                                            #
#                                                                      #
########################################################################

# Add the base configuration as specified above

# Point Nextcloud to its dedicated Valkey instance
nextcloud_redis_hostname: mash-nextcloud-valkey

# Make sure the Nextcloud service (mash-nextcloud.service) starts after its dedicated Valkey service (mash-nextcloud-valkey.service)
nextcloud_systemd_required_services_list_custom:
  - "mash-nextcloud-valkey.service"

# Make sure the Nextcloud container is connected to the container network of its dedicated Valkey service (mash-nextcloud-valkey)
nextcloud_container_additional_networks_custom:
  - "mash-nextcloud-valkey"

########################################################################
#                                                                      #
# /nextcloud                                                           #
#                                                                      #
########################################################################
```

Running the installation command will create the dedicated Valkey instance named `mash-nextcloud-valkey`.

#### Setting up a shared Valkey instance

If you host only Nextcloud on this server, it is fine to set up a single shared Valkey instance.

To install the single instance and hook Nextcloud to it, add the following configuration to `inventory/host_vars/mash.example.com/vars.yml`:

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
# nextcloud                                                            #
#                                                                      #
########################################################################

# Add the base configuration as specified above

# Point Nextcloud to the shared Valkey instance
nextcloud_redis_hostname: "{{ valkey_identifier }}"

# Make sure the Nextcloud service (mash-nextcloud.service) starts after the shared Valkey service (mash-valkey.service)
nextcloud_systemd_required_services_list_custom:
  - "{{ valkey_identifier }}.service"

# Make sure the Nextcloud container is connected to the container network of the shared Valkey service (mash-valkey)
nextcloud_container_additional_networks_custom:
  - "{{ valkey_identifier }}"

########################################################################
#                                                                      #
# /nextcloud                                                           #
#                                                                      #
########################################################################
```

Running the installation command will create the shared Valkey instance named `mash-valkey`.

### Samba (optional)

You can enable [Samba](https://www.samba.org/) external Windows fileshares using [smbclient](https://www.samba.org/samba/docs/current/man-html/smbclient.1.html). See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-nextcloud/blob/main/docs/configuring-nextcloud.md#enable-samba-optional) on the role's documentation for details.

## Installation

If you have decided to install the dedicated Valkey instance for Nextcloud, make sure to run the [installing](../installing.md) command for the supplementary host (`mash.example.com-nextcloud-deps`) first, before running it for the main host (`mash.example.com`).

Note that running the `just` commands for installation (`just install-all` or `just setup-all`) automatically takes care of the order. See [here](../running-multiple-instances.md#1-adjust-hosts) for more details about it.

## Usage

After running the command for installation, the Nextcloud instance becomes available at the URL specified with `nextcloud_hostname` and `nextcloud_path_prefix`. With the configuration above, the service is hosted at `https://mash.example.com/nextcloud`.

Before logging in to the instance, update the configuration (URL paths, trusted reverse-proxies, etc.) by running the command below:

```sh
just run-tags adjust-nextcloud-config
```

>[!NOTE]
> You should re-run the command every time the Nextcloud version is updated.

### Checking SMTP server configuration

The playbook automatically configures a SMTP server (Exim-relay), to which the Nextcloud instance connects to send emails. After logging in as the admin user, you can check the configuration at `https://mash.example.com/nextcloud/settings/admin` for basic administration settings.

Before sending a test mail, **make sure to set the email address of the admin user** at `https://mash.example.com/nextcloud/settings/user`. Otherwise hitting the "Send email" button on the page returns the 400 error, as the instance does not know where to send the mail. See the browser's console for details.

### Single-Sign-On (SSO) integration

Nextcloud supports Single-Sign-On (SSO) via LDAP, SAML, and OIDC. To make use of it, an identity provider like [authentik](authentik.md) or [Keycloak](keycloak.md) needs to be set up.

For example, you can enable SSO with authentik via OIDC by following the steps below:

* Create a new provider in authentik and trim the client secret to less than 64 characters
* Create an application in authentik using this provider
* Install the app `user_oidc` in Nextcloud
* Fill in the details from authentik in the app settings

Refer to [this blogpost by a third party](https://blog.cubieserver.de/2022/complete-guide-to-nextcloud-oidc-authentication-with-authentik/) for details.

**Notes**:
- The official documentation of authentik to connect nextcloud via SAML does not seem to work (as of August 2023).
- If you cannot log in due to an error (the error message contains `SHA1 mismatch`), make sure that Nextcloud users and authentik users do not have the same name. If they do, check `Use unique user ID` in the OIDC App settings.

## Related services

### Collabora Online Development Edition

On Nextcloud it is possible to integrate the Collabora Online Development Edition (CODE) office suite. This playbook supports it, and you can set up a CODE instance by enabling it on `vars.yml`. You can follow the [documentation](code.md) to install it.

By default, this playbook is configured to automatically integrate the CODE instance with the Nextcloud instance which this playbook manages, if both of them are enabled.

After installing both CODE and Nextcloud, run this command to install and configure the [Office](https://apps.nextcloud.com/apps/richdocuments) app for Nextcloud:

```sh
just run-tags install-nextcloud-app-collabora
```

Open the URL `https://mash.example.com/nextcloud/settings/admin/richdocuments` to have the instance set up the connection with the CODE instance.

You should then be able to open any document (`.doc`, `.odt`, `.pdf`, etc.) and create new ones in Nextcloud Files with Collabora Online Development Edition's editor.

>[!NOTE]
> By default, various private IPv4 networks are whitelisted to connect to the WOPI API (document serving API). If your CODE instance does not live on the same server as Nextcloud, you may need to adjust the list of networks. If necessary, redefine the `nextcloud_app_collabora_wopi_allowlist` environment variable on `vars.yml`.

### Preview Generator

It is also possible to set up preview generation by following the steps below. See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-nextcloud/blob/main/docs/configuring-nextcloud.md#enable-preview-generator-app-optional) on the role's documentation for details.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-nextcloud/blob/main/docs/configuring-nextcloud.md#troubleshooting) on the role's documentation for details.
