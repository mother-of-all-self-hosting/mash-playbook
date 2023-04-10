# MariaDB

[MariaDB](https://mariadb.org/) is a powerful, open source object-relational database system.

Some of the services installed by this playbook require a MariaDB database.

Enabling the MariaDB database service will automatically wire all other services which require such a database to use it.


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# mariadb                                                              #
#                                                                      #
########################################################################

mariadb_enabled: true

# Put a strong password below, generated with `pwgen -s 64 1` or in another way
mariadb_root_passsword: ''

########################################################################
#                                                                      #
# /mariadb                                                             #
#                                                                      #
########################################################################
```

### Getting a database terminal

You can use the `/mash/mariadb/bin/cli` tool to get interactive terminal access to the MariaDB server.

To see the available databases, run `SHOW DATABASES`.

To change to another existing database (for example `miniflux`), run `USE miniflux`.

You can then proceed to write queries. Example: `SELECT COUNT(*) FROM users;`

**Be careful**. Modifying the database directly (especially as services are running) is dangerous and may lead to irreversible database corruption.
When in doubt, consider [making a backup](#backing-up-mariadb).

## Upgrading MariaDB

The major MariaDB version you start with (e.g. `10.10` or `10.11`) will be kept until you manually upgrade it. The playbook will stick to this major version and only do minor version upgrades (e.g. `10.10.1` -> `10.10.3`).

For now, there's no automatic upgrade path between major MariaDB versions, but support for upgrading will be added in the future.

## Backing up MariaDB

A `/mash/mariadb/bin/dump-all` script will be installed, which can dump the database to a path of your choosing.
