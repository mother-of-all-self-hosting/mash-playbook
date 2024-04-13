# Wallabag
[Wallabag](https://wallabag.org/) is a self-hosted application for saving web pages to read them later.

This role is **not** affiliated with the Wallabag project. 

The role is created by [Bergrübe](https://github.com/Bergruebe/ansible-role-wallabag) with information from the official [documentation](https://doc.wallabag.org/en/) and the [Wallabag Docker Hub page](https://hub.docker.com/r/wallabag/wallabag/).

## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server
- (optional) the [Postgres](postgres.md) database server
- (optional) the [exim-relay](exim-relay.md) mailer

Wallabag can be run with a sqlite database, but if the Postgres database is activated, it will be used automatically.
With manual configuration, you can also use [MariaDB](mariadb.md) instead of Postgres.

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# wallabag                                                             #
#                                                                      #
########################################################################

wallabag_enabled: true
wallabag_domain: "wallabag.example.com"

wallabag_locale: 'en'

# Put something random in here
wallabag_secret: ''

########################################################################
#                                                                      #
# /wallabag                                                            #
#                                                                      #
########################################################################
```

## Email configuration
If the exim-relay mailer is enabled, the role will automatically configure Wallabag to use it.
If you want to use a different mailer, you can configure it manually with following variables:

```yaml
wallabag_mailer_dsn: "smtp://user:pass@smtp.example.com:465"
wallabag_from_email: "wallabag@example.com"
wallabag_twofactor_sender: "wallabag@example.com"
```
You can find more information in the Wallabag [documentation](https://doc.wallabag.org/en/admin/mailer).

## Manual database configuration
If you don't want to use the by the playbook managed Postgres database, you can configure Wallabag to use a different database with the following variables:
```yaml
wallabag_database_driver: "pdo_pgsql" # or "pdo_mysql" or "pdo_sqlite"
wallabag_database_hostname: "HOSTNAME"
wallabag_database_port: "PORT"
wallabag_database_name: "DATABASE"
wallabag_database_username: "USERNAME"
wallabag_database_password: "PASSWORD"
wallabag_database_charset: "utf8"
wallabag_database_table_prefix: "wallabag_"
```

## Usage
After [installing](../installing.md), you can access Wallabag at your `wallabag_domain` with the default credentials `wallabag:wallabag`.
