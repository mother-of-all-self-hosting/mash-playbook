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

If you are unsure whether you will install other services along with Nextcloud or you have already set up services which need Valkey, it is recommended to install a Valkey instance dedicated to Nextcloud. See [below](#setting-up-a-shared-valkey-instance) for an instruction to install a shared instance.

💡 It is dubious whether using Valkey helps much, so we recommend that you **start without** it for a simpler deployment. To learn more, read the [Memory caching](https://docs.nextcloud.com/server/latest/admin_manual/configuration_server/caching_configuration.html) section of the Nextcloud documentation.

#### Setting up a dedicated Valkey instance

To create a dedicated instance for Nextcloud, you can follow the steps below:

1. Adjust the `hosts` file
2. Create a new `vars.yml` file for the dedicated instance
3. Edit the existing `vars.yml` file for the main host

##### Adjust `hosts`

At first, you need to adjust `inventory/hosts` file to add a supplementary host for Nextcloud. See [here](../running-multiple-instances.md#re-do-your-inventory-to-add-supplementary-hosts) for details.

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

**Notes**:
- As this `vars.yml` file will be used for the new host, make sure to set `mash_playbook_generic_secret_key`. It does not need to be same as the one on `vars.yml` for the main host. Without setting it, the Valkey instance will not be configured.
- Since these variables are used to configure the service name and directory path of the Valkey instance, you do not have to have them matched with the hostname of the server. For example, even if the hostname is `www.example.com`, you do **not** need to set `mash_playbook_service_base_directory_name_prefix` to `www-`. If you are not sure which string you should set, you might as well use the values as they are.

```yaml
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

# Make sure the Nextcloud service (mash-nextcloud.service) starts after its dedicated KeyDB service (mash-nextcloud-valkey.service)
nextcloud_systemd_required_services_list_custom:
  - "mash-nextcloud-valkey.service"

# Make sure the Nextcloud container is connected to the container network of its dedicated KeyDB service (mash-nextcloud-valkey)
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

# Make sure the Nextcloud service (mash-nextcloud.service) starts after the shared KeyDB service (mash-valkey.service)
nextcloud_systemd_required_services_list_custom:
  - "{{ valkey_identifier }}.service"

# Make sure the Nextcloud container is connected to the container network of the shared KeyDB service (mash-valkey)
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

###  Single-Sign-On / Authentik

Nextcloud supports Single-Sign-On (SSO) via LDAP, SAML, and OIDC. To make use of this you'll need a Identity Provider like [authentik](./authentik.md) or [Keycloak](./keycloak.md). The following assumes you use authentik.


**The official documentation of authentik to connect nextcloud via SAML seems broken**

MASH can connect Nextcloud with authentik via OIDC. The setup is quite straightforward, refer to [this blogpost by Jack](https://blog.cubieserver.de/2022/complete-guide-to-nextcloud-oidc-authentication-with-authentik/) for a full explanation.

In short you should:

* Create a new provider in authentik and trim the client secret to <64 characters
* Create an application in authentik using this provider
* Install the app `user_oidc` in Nextcloud
* Fill in the details from authentik in the app settings

**Troubleshooting**

If you encounter problems during login check (error message containes `SHA1 mismatch`) that
* Nextcloud users and authentik users do not have the same name -> if they do check `Use unique user ID` in the OIDC App settings

### Samba

To enable [Samba](https://www.samba.org/) external Windows fileshares using [smbclient](https://www.samba.org/samba/docs/current/man-html/smbclient.1.html), add the following additional configuration to your `vars.yml` file:

```yml
nextcloud_container_image_customizations_samba_enabled: true
```

## Installation

If you have decided to install the dedicated Valkey instance for Nextcloud, make sure to run the [installing](../installing.md) command for the supplementary host (`mash.example.com-nextcloud-deps`) first, before running it for the main host (`mash.example.com`).

Note that running the `just` commands for installation (`just install-all` or `just setup-all`) automatically takes care of the order. See [here](../running-multiple-instances.md#re-do-your-inventory-to-add-supplementary-hosts) for more details about it.

## Usage

After [installation](../installing.md), you should follow Nextcloud's setup wizard at the URL you've chosen.

You can choose any username/password for your account.

In **Storage & database**, you should choose PostgreSQL (changing the default **SQLite** choice), with the credentials you see after running `just run-tags print-nextcloud-db-credentials`

Once you've fully installed Nextcloud, you'd better adjust its default configuration (URL paths, trusted reverse-proxies, etc.) by running: `just run-tags adjust-nextcloud-config`


## Recommended other services

### Collabora Online

To integrate the [Collabora Online](collabora-online.md) office suite, first install it by following its dedicated documentation page.

Then add the following **additional** Nextcloud configuration:

```yaml
nextcloud_collabora_app_wopi_url: "{{ collabora_online_url }}"

# By default, various private IPv4 networks are whitelited to connect to the WOPI API (document serving API).
# If your Collabora Online installation does not live on the same server as Nextcloud,
# you may need to adjust the list of networks.
# If necessary, redefined the `nextcloud_collabora_app_wopi_allowlist` environment variable here.
```

There's **no need** to [re-run the playbook](../installing.md) after adjusting your `vars.yml` file.
You should, however run: `just run-tags install-nextcloud-app-collabora`

This will install and configure the [Office](https://apps.nextcloud.com/apps/richdocuments) app for Nextcloud.

You should then be able to click any document (`.doc`, `.odt`, `.pdf`, etc.) in Nextcloud Files and it should automatically open a Collabora Online editor.

You can also create new documents via the "plus" button.

### Preview Generator

It is possible to setup preview generation, using this playbook.

First modify your `vars.yml` file by adding at least the following line (other options are also present, check the corresponding `defaults/main.yml` file):

```yaml
nextcloud_preview_enabled: true
```

then install Nextcloud (or rerun the playbook if already installed).

Next, from the Settings/Application menu in your Nextcloud instance install the preview generator app (https://apps.nextcloud.com/apps/previewgenerator).

After the application is installed run `just run-tags adjust-nextcloud-config` that will start the original preview-generation and when finished, enables the periodic generation of new images.

The original generation may take a long time, but a continuous prompt is presented by ansible as some visual feedback (it is being run as an async task), however it will timeout after approximately 27 hours.

On 60GBs, most of the data being images, it took about 10 minutes to finish.

If it takes more time to run than a day, you may want to start it from the host by calling

```sh
/usr/bin/env docker exec mash-nextcloud-server php /var/www/html/occ preview:generate-all
```

Also, please note: every time Nextcloud version is updated, you should rerun: `just run-tags adjust-nextcloud-config`.

Other supported variables:

`nextcloud_preview_preview_max_x` and `nextcloud_preview_preview_max_y` sets the maximum size of the preview in pixels..
Their default value according to the [documentation](https://docs.nextcloud.com/server/latest/admin_manual/configuration_files/previews_configuration.html) is `null` which is set by the playbook.
Using a numeric value will set the corresponding nextcloud variable and sets the size of the preview images.

`nextcloud_preview_app_jpeg_quality` JPEG quality setting for preview images.
The default follows upstream default with 80.
