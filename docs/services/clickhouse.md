# ClickHouse

[ClickHouse](https://clickhouse.com/) is an open-source column-oriented DBMS for online analytical processing (OLAP) that allows users to generate analytical reports using SQL queries in real-time.

Some of the services installed by this playbook require a ClickHouse database.

Enabling the ClickHouse database service will automatically wire all other services which require such a database to use it.


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# clickhouse                                                           #
#                                                                      #
########################################################################

clickhouse_enabled: true

# Put a strong password below, generated with `pwgen -s 64 1` or in another way
clickhouse_root_passsword: ''

########################################################################
#                                                                      #
# /clickhouse                                                          #
#                                                                      #
########################################################################
```

### Getting a database terminal

You can use the `/mash/clickhouse/bin/cli` tool to get interactive terminal access to the ClickHouse server.

## Upgrading ClickHouse

ClickHouse is supposed to auto-upgrade its data as you upgrade to a newer version. There's nothing special that needs to be done.

## Backing up ClickHouse

The `/mash/clickhouse/backups` directory is mounted as `/backups` into the container and is an allowed disk for backups called `backups`.

You can export a single database table by using [the CLI](#getting-a-database-terminal) and running a command like this:

```sql
BACKUP TABLE test TO Disk('backups', 'test.zip');
```

Read the [Backup and Restore](https://clickhouse.com/docs/en/operations/backup) article in the official documentation to learn more.

For better (more en-masse) exporting, it may be beneficial to use the 3rd party [clickhouse-backup](https://github.com/AlexAkulov/clickhouse-backup) tool, but this is not supported by the playbook yet.
