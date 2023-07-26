# Linkding

[Linkding](https://github.com/sissbruecker/linkding) bookmark manager that is designed be to be minimal and fast.

## Dependencies

This service requires the following other services:

-   a [Postgres](postgres.md) database, but [SQLite](https://www.sqlite.org/) is also a possibility (see `linkding_database_engine` below)
-   a [Traefik](traefik.md) reverse-proxy server

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

# We configure Linkding to use Postgres by default. See docs/services/postgres.md.
# To use an external Postgres server, you need to tweak additional `linkding_database_*` variables.
# Feel free to remove the line below to make Linkding use SQLite.
linkding_database_engine: postgres

linkding_superuser_username: change me
linkding_superuser_password: change me
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
