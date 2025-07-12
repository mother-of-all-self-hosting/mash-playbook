<!--
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 MASH project contributors
SPDX-FileCopyrightText: 2023 Niels Bouma
SPDX-FileCopyrightText: 2023 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2024 Gergely Horváth

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Nextcloud

[Nextcloud](https://nextcloud.com/) is the most popular self-hosted collaboration solution for tens of millions of users at thousands of organizations across the globe.


## Dependencies

This service requires the following other services:

- a [Postgres](postgres.md) database
- a [Traefik](traefik.md) reverse-proxy server
- (optional) a [Valkey](valkey.md) data-store; see [below](#configure-valkey) for details about installation
- (optional) the [exim-relay](exim-relay.md) mailer


## Configuration

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

In the example configuration above, we configure the service to be hosted at `https://mash.example.com/nextcloud`.

You can remove the `nextcloud_path_prefix` variable definition, to make it default to `/`, so that the service is served at `https://mash.example.com/`.

### Valkey

Valkey can **optionally** be enabled to improve Nextcloud performance.

If Nextcloud is the sole service which requires Valkey on your server, it is fine to set up just a single Valkey instance. However, **it is not recommended if there are other services which require it, because sharing the Valkey instance has security concerns and possibly causes data conflicts**, as described on the [documentation for configuring Valkey](valkey.md). In this case, you should install a dedicated Valkey instance for each of them.

If you are unsure whether you will install other services along with Nextcloud or you have already set up services which need Valkey (such as [PeerTube](peertube.md), [Funkwhale](funkwhale.md), and [Docmost](docmost.md)), it is recommended to install a Valkey instance dedicated to Nextcloud.

*See [below](#setting-up-a-shared-valkey-instance) for an instruction to install a shared instance.*

💡 It is dubious whether using Valkey helps much, so we recommend that you **start without** it for a simpler deployment. To learn more, read the [Memory caching](https://docs.nextcloud.com/server/latest/admin_manual/configuration_server/caching_configuration.html) section of the Nextcloud documentation.

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

#### Adjust Nextcloud configuration file

If a Valkey instance is enabled for Nextcloud in either way, adjust your Nextcloud configuration file (e.g. `/mash/nextcloud/data/config/config.php`) to **add** this:

```php
  'memcache.distributed' => '\OC\Memcache\Redis',
  'memcache.locking' => '\OC\Memcache\Redis',
  'redis' => [
     'host' => 'VALKEY_HOSTNAME_HERE',
     'port' => 6379,
  ],
```

Where `VALKEY_HOSTNAME_HERE` is to be replaced with:

- `mash-nextcloud-valkey` if the dedicated Valkey instance is used
- `mash-valkey` if the single Valkey instance is used

### Samba

To enable [Samba](https://www.samba.org/) external Windows fileshares using [smbclient](https://www.samba.org/samba/docs/current/man-html/smbclient.1.html), add the following configuration to your `vars.yml` file:

```yaml
nextcloud_container_image_customizations_samba_enabled: true
```

## Installation

If you have decided to install the dedicated Valkey instance for Nextcloud, make sure to run the [installing](../installing.md) command for the supplementary host (`mash.example.com-nextcloud-deps`) first, before running it for the main host (`mash.example.com`).

Note that running the `just` commands for installation (`just install-all` or `just setup-all`) automatically takes care of the order. See [here](../running-multiple-instances.md#1-adjust-hosts) for more details about it.

## Usage

After installation, your Nextcloud instance becomes available at the URL specified with `nextcloud_hostname` and `nextcloud_path_prefix`. With the configuration above, the service is hosted at `https://mash.example.com/nextcloud`.

To get started, go to the URL and follow Nextcloud's set up wizard.

In **Storage & database**, it is recommended to choose PostgreSQL (changing the default **SQLite** choice). To check credentials for it, run this command: `just run-tags print-nextcloud-db-credentials`

Once you have completed the set up wizard, update the configuration (URL paths, trusted reverse-proxies, etc.) by running this command: `just run-tags adjust-nextcloud-config`. **You should re-run the command every time the Nextcloud version is updated.**

### Single-Sign-On (SSO) integration

Nextcloud supports Single-Sign-On (SSO) via LDAP, SAML, and OIDC. To make use of it, an Identity Provider like [authentik](./authentik.md) or [Keycloak](./keycloak.md) needs to be set up.

For example, you can enable SSO with authentik via OIDC by following the steps below:

* Create a new provider in authentik and trim the client secret to less than 64 characters
* Create an application in authentik using this provider
* Install the app `user_oidc` in Nextcloud
* Fill in the details from authentik in the app settings

Refer to [this blogpost by a third party](https://blog.cubieserver.de/2022/complete-guide-to-nextcloud-oidc-authentication-with-authentik/) for details.

**Notes**:
- The official documentation of authentik to connect nextcloud via SAML does not seem to work (as of August 2023).
- If you cannot log in due to an error (the error message contains `SHA1 mismatch`), make sure that Nextcloud users and authentik users do not have the same name. If they do, check `Use unique user ID` in the OIDC App settings.

## Recommended services

### Collabora Online

To integrate the [Collabora Online](collabora-online.md) office suite, first install it by following its documentation page.

Then, add the following configuration for Nextcloud:

```yaml
nextcloud_collabora_app_wopi_url: "{{ collabora_online_url }}"
```

**Note**: by default, various private IPv4 networks are whitelited to connect to the WOPI API (document serving API). If your Collabora Online installation does not live on the same server as Nextcloud, you may need to adjust the list of networks. If necessary, redefine the `nextcloud_collabora_app_wopi_allowlist` environment variable on `vars.yml`.

After adding the configuration, run this command to install and configure the [Office](https://apps.nextcloud.com/apps/richdocuments) app for Nextcloud: `just run-tags install-nextcloud-app-collabora`

You should then be able to open any document (`.doc`, `.odt`, `.pdf`, etc.) and create new ones in Nextcloud Files with Collabora Online editor.

### Preview Generator

It is also possible to set up preview generation by following the steps below.

#### Enable preview on `vars.yml`

First, add the following configuration to `vars.yml` and run the playbook.

```yaml
nextcloud_preview_enabled: true
```

Other supported variables:

- `nextcloud_preview_preview_max_x` and `nextcloud_preview_preview_max_y`
  - Set the maximum size of the preview in pixels. The default value on this playbook is `null`. Setting a numeric value configures the corresponding nextcloud variable and the size of the preview images. See the [documentation](https://docs.nextcloud.com/server/latest/admin_manual/configuration_files/previews_configuration.html) for details.
- `nextcloud_preview_app_jpeg_quality`
  - JPEG quality for preview images. The default value is 80, based on the value by the upstream project.

Check `defaults/main.yml` for Nextcloud for other options.

#### Install the app on Nextcloud and run the command for config adjustment

Next, install the preview generator app (https://apps.nextcloud.com/apps/previewgenerator) from the Settings/Application menu in your Nextcloud instance.

After it is installed, run the command `just run-tags adjust-nextcloud-config` against your server. It starts original preview-generation and enables periodic generation of new images on your server.

**Notes**:
- The original generation may take a long time, and a continuous prompt is presented by Ansible as some visual feedback (it is being run as an async task). Note it will timeout after approximately 27 hours. For reference, it should take about 10 minutes to finish generating previews of 60 GB data, most of which being image files.
- If it takes more time to run than a day, you may want to start it by running the command on the host:
  ```sh
  /usr/bin/env docker exec mash-nextcloud-server php /var/www/html/occ preview:generate-all
  ```
