# Nextcloud

[Nextcloud](https://nextcloud.com/) is the most popular self-hosted collaboration solution for tens of millions of users at thousands of organizations across the globe.


## Dependencies

This service requires the following other services:

- a [Postgres](postgres.md) database
- a [Traefik](traefik.md) reverse-proxy server


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

########################################################################
#                                                                      #
# /nextcloud                                                           #
#                                                                      #
########################################################################
```

In the example configuration above, we configure the service to be hosted at `https://mash.example.com/nextcloud`.

You can remove the `nextcloud_path_prefix` variable definition, to make it default to `/`, so that the service is served at `https://mash.example.com/`.


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
