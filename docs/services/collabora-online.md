# Collabora Online

The [Collabora Online Development Edition (CODE)](https://www.collaboraoffice.com/) office suite, together with the [Office App](https://apps.nextcloud.com/apps/richdocuments) for [Nextcloud](nextcloud.md) enables you to edit office documents online.


## Dependencies

This service requires the following other services:

- a [Postgres](postgres.md) database
- a [Traefik](traefik.md) reverse-proxy server


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# collabora-online                                                     #
#                                                                      #
########################################################################

collabora_online_enabled: true

collabora_online_hostname: collabora.example.com

# A password for the admin interface, available at: https://COLLABORA_ONLINE_DOMAIN/browser/dist/admin/admin.html
# Use only alpha-numeric characters
collabora_online_env_variable_password: ''

collabora_online_aliasgroup: "https://{{ nextcloud_hostname | replace('.', '\\.') }}:443"

########################################################################
#                                                                      #
# /collabora-online                                                    #
#                                                                      #
########################################################################
```

In the example configuration above, we configure the service to be hosted at `https://collabora.example.com`.


## Integrating with Nextcloud

To learn how to integrate Collabora Online with Nextcloud, see the [Collabora Online section](nextcloud.md#collabora-online) in our Nextcloud documentation.


## Admin Interface

There's an admin interface with various statistics and information at: `https://COLLABORA_ONLINE_DOMAIN/browser/dist/admin/admin.html`

Use your admin credentials for logging in:

- the default username is `admin`, as specified in `collabora_online_env_variable_username`
- the password is the one you've specified in `collabora_online_env_variable_password`
