# linkding

[linkding](https://github.com/sissbruecker/linkding) bookmark manager that is designed be to be minimal and fast.

## Dependencies

This service requires the following other services:

-  a [Postgres](postgres.md) database, but will fallback to [SQLite](https://www.sqlite.org/) if unavailable
-  a [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# linkding                                                             #
#                                                                      #
########################################################################

linkding_enabled: true

linkding_hostname: mash.example.com
linkding_path_prefix: /linkding

linkding_superuser_username: ''
linkding_superuser_password: ''

########################################################################
#                                                                      #
# /linkding                                                            #
#                                                                      #
########################################################################
```

In the example configuration above, we configure the service to be hosted at `https://mash.example.com/linkding`.

You can remove the `linkding_path_prefix` variable definition, so that the service is served at `https://mash.example.com/`.

### Superuser

Please note the use of [`linkding_superuser_username`](https://github.com/sissbruecker/linkding/blob/master/docs/Options.md#ld_superuser_name) and [`linkding_superuser_password`](https://github.com/sissbruecker/linkding/blob/master/docs/Options.md#ld_superuser_password) variables. These are not mandatory and are meant to be set the first time you run this role.

## Usage

After installation, you can log in with your superuser login (`linkding_superuser_username`) and password (`linkding_superuser_password`).
