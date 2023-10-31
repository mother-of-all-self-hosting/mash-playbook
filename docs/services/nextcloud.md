# Nextcloud

[Nextcloud](https://nextcloud.com/) is the most popular self-hosted collaboration solution for tens of millions of users at thousands of organizations across the globe.


## Dependencies

This service requires the following other services:

- a [Postgres](postgres.md) database
- a [Traefik](traefik.md) reverse-proxy server
- a [Redis](redis.md) data-store (optional), installation details [below](#redis)


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# nextcloud                                                            #
#                                                                      #
########################################################################

nextcloud_enabled: true

nextcloud_hostname: mash.example.com
nextcloud_path_prefix: /nextcloud

# Redis configuration, as described below

########################################################################
#                                                                      #
# /nextcloud                                                           #
#                                                                      #
########################################################################
```

In the example configuration above, we configure the service to be hosted at `https://mash.example.com/nextcloud`.

You can remove the `nextcloud_path_prefix` variable definition, to make it default to `/`, so that the service is served at `https://mash.example.com/`.

### Redis

Redis can **optionally** be enabled to improve Nextcloud performance.
It's dubious whether using using Redis helps much, so we recommend that you **start without** it, for a simpler deployment.

To learn more, read the [Memory caching](https://docs.nextcloud.com/server/latest/admin_manual/configuration_server/caching_configuration.html) section of the Nextcloud documentation.

As described on the [Redis](redis.md) documentation page, if you're hosting additional services which require Redis on the same server, you'd better go for installing a separate Redis instance for each service. See [Creating a Redis instance dedicated to Nextcloud](#creating-a-redis-instance-dedicated-to-nextcloud).

If you're only running Nextcloud on this server and don't need to use Redis for anything else, you can [use a single Redis instance](#using-the-shared-redis-instance-for-nextcloud).

**Regardless** of the method of installing Redis, you may need to adjust your Nextcloud configuration file (e.g. `/mash/nextcloud/data/config/config.php`) to **add** this:

```php
  'memcache.distributed' => '\OC\Memcache\Redis',
  'memcache.locking' => '\OC\Memcache\Redis',
  'redis' => [
     'host' => 'REDIS_HOSTNAME_HERE',
     'port' => 6379,
  ],
```

Where `REDIS_HOSTNAME_HERE` is to be replaced with:

- `mash-nextcloud-redis`, when [Creating a Redis instance dedicated to Nextcloud](#creating-a-redis-instance-dedicated-to-nextcloud)
- `mash-redis`, when [using a single Redis instance](#using-the-shared-redis-instance-for-nextcloud).


#### Using the shared Redis instance for Nextcloud

To install a single (non-dedicated) Redis instance (`mash-redis`) and hook Nextcloud to it, add the following **additional** configuration:

```yaml
########################################################################
#                                                                      #
# redis                                                                #
#                                                                      #
########################################################################

redis_enabled: true

########################################################################
#                                                                      #
# /redis                                                               #
#                                                                      #
########################################################################


########################################################################
#                                                                      #
# nextcloud                                                            #
#                                                                      #
########################################################################

# Base configuration as shown above

# Point Nextcloud to the shared Redis instance
nextcloud_redis_hostname: "{{ redis_identifier }}"

# Make sure the Nextcloud service (mash-nextcloud.service) starts after the shared Redis service (mash-redis.service)
nextcloud_systemd_required_services_list_custom:
  - "{{ redis_identifier }}.service"

# Make sure the Nextcloud container is connected to the container network of the shared Redis service (mash-redis)
nextcloud_container_additional_networks_custom:
  - "{{ redis_identifier }}"

########################################################################
#                                                                      #
# /nextcloud                                                           #
#                                                                      #
########################################################################
```
This will create a `mash-redis` Redis instance on this host.

This is only recommended if you won't be installing other services which require Redis. Alternatively, go for [Creating a Redis instance dedicated to Nextcloud](#creating-a-redis-instance-dedicated-to-nextcloud).

#### Creating a Redis instance dedicated to Nextcloud

The following instructions are based on the [Running multiple instances of the same service on the same host](../running-multiple-instances.md) documentation.

Adjust your `inventory/hosts` file as described in [Re-do your inventory to add supplementary hosts](../running-multiple-instances.md#re-do-your-inventory-to-add-supplementary-hosts), adding a new supplementary host (e.g. if `nextcloud.example.com` is your main one, create `nectcloud.example.com-deps`).

Then, create a new `vars.yml` file for the

`inventory/host_vars/nextcloud.example.com-deps/vars.yml`:

```yaml
---

########################################################################
#                                                                      #
# Playbook                                                             #
#                                                                      #
########################################################################

# Put a strong secret below, generated with `pwgen -s 64 1` or in another way
# Various other secrets will be derived from this secret automatically.
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
# redis                                                                #
#                                                                      #
########################################################################

redis_enabled: true

########################################################################
#                                                                      #
# /redis                                                               #
#                                                                      #
########################################################################
```

This will create a `mash-nextcloud-redis` instance on this host with its data in `/mash/nextcloud-redis`.

Then, adjust your main inventory host's variables file (`inventory/host_vars/nextcloud.example.com/vars.yml`) like this:

```yaml
########################################################################
#                                                                      #
# nextcloud                                                            #
#                                                                      #
########################################################################

# Base configuration as shown above

# Point Nextcloud to its dedicated Redis instance
nextcloud_redis_hostname: mash-nextcloud-redis

# Make sure the Nextcloud service (mash-nextcloud.service) starts after its dedicated Redis service (mash-nextcloud-redis.service)
nextcloud_systemd_required_services_list_custom:
  - "mash-nextcloud-redis.service"

# Make sure the Nextcloud container is connected to the container network of its dedicated Redis service (mash-nextcloud-redis)
nextcloud_container_additional_networks_custom:
  - "mash-nextcloud-redis"

########################################################################
#                                                                      #
# /nextcloud                                                           #
#                                                                      #
########################################################################
```

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

## Installation

If you've decided to install a dedicated Redis instance for Nextcloud, make sure to first do [installation](../installing.md) for the supplementary inventory host (e.g. `nextcloud.example.com-deps`), before running installation for the main one (e.g. `nextcloud.example.com`).

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
