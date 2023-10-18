# Postgres

[PostgreSQL](https://www.postgresql.org) is a powerful, open source object-relational database system with over 35 years of active development that has earned it a strong reputation for reliability, feature robustness, and performance.

Many of the services installed by this playbook require a Postgres database.

Enabling the Postgres database service will automatically wire all other services which require such a database to use it.


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# devture-postgres                                                     #
#                                                                      #
########################################################################

devture_postgres_enabled: true

# Put a strong password below, generated with `pwgen -s 64 1` or in another way
devture_postgres_connection_password: ''

########################################################################
#                                                                      #
# /devture-postgres                                                    #
#                                                                      #
########################################################################
```

## Importing

### Importing an existing Postgres database from another installation (optional)

Follow this section if you'd like to import your database from a previous installation.

### Prerequisites

The playbook supports importing Postgres dump files in **text** (e.g. `pg_dump > dump.sql`) or **gzipped** formats (e.g. `pg_dump | gzip -c > dump.sql.gz`).

Importing multiple databases (as dumped by `pg_dumpall`) is also supported.

Before doing the actual import, **you need to upload your Postgres dump file to the server** (any path is okay).


### Importing a dump file

To import, run this command (make sure to replace `SERVER_PATH_TO_POSTGRES_DUMP_FILE` with a file path on your server):

```sh
just run-tags import-postgres \
--extra-vars=server_path_postgres_dump=SERVER_PATH_TO_POSTGRES_DUMP_FILE \
--extra-vars=postgres_default_import_database=main
```

**Notes**:

- `SERVER_PATH_TO_POSTGRES_DUMP_FILE` must be a file path to a Postgres dump file on the server (not on your local machine!)
- `postgres_default_import_database` defaults to `main`, which is useful for importing multiple databases (for dumps made with `pg_dumpall`). If you're importing a single database (e.g. `miniflux`), consider changing `postgres_default_import_database` to the name of the database (e.g. `miniflux`)
- after importing a large database, it's a good idea to run [an `ANALYZE` operation](https://www.postgresql.org/docs/current/sql-analyze.html) to make Postgres rebuild its database statistics and optimize its query planner. You can easily do this via the playbook by running `just run-tags run-postgres-vacuum -e postgres_vacuum_preset=analyze` (see [Vacuuming PostgreSQL](#vacuuming-postgresql) for more details).


## Maintenance

This section shows you how to perform various maintenance tasks related to the Postgres database server used by various components of this playbook.

Table of contents:

- [Getting a database terminal](#getting-a-database-terminal), for when you wish to execute SQL queries

- [Vacuuming PostgreSQL](#vacuuming-postgresql), for when you wish to run a Postgres [VACUUM](https://www.postgresql.org/docs/current/sql-vacuum.html) (optimizing disk space)

- [Backing up PostgreSQL](#backing-up-postgresql), for when you wish to make a backup

- [Upgrading PostgreSQL](#upgrading-postgresql), for upgrading to new major versions of PostgreSQL. Such **manual upgrades are sometimes required**.

- [Tuning PostgreSQL](#tuning-postgresql) to make it run faster

### Getting a database terminal

You can use the `/mash/postgres/bin/cli` tool to get interactive terminal access ([psql](https://www.postgresql.org/docs/15/app-psql.html)) to the PostgreSQL server.

By default, this tool puts you in the `main` database, which contains nothing.

To see the available databases, run `\list` (or just `\l`).

To change to another database (for example `miniflux`), run `\connect miniflux` (or just `\c miniflux`).

You can then proceed to write queries. Example: `SELECT COUNT(*) FROM users;`

**Be careful**. Modifying the database directly (especially as services are running) is dangerous and may lead to irreversible database corruption.
When in doubt, consider [making a backup](#backing-up-postgresql).


### Vacuuming PostgreSQL

Deleting lots data from Postgres does not make it release disk space, until you perform a [`VACUUM` operation](https://www.postgresql.org/docs/current/sql-vacuum.html).

You can run different `VACUUM` operations via the playbook, with the default preset being `vacuum-complete`:

- (default) `vacuum-complete`: stops all services temporarily and runs `VACUUM FULL VERBOSE ANALYZE`.
- `vacuum-full`: stops all services temporarily and runs `VACUUM FULL VERBOSE`
- `vacuum`: runs `VACUUM VERBOSE` without stopping any services
- `vacuum-analyze` runs `VACUUM VERBOSE ANALYZE` without stopping any services
- `analyze` runs `ANALYZE VERBOSE` without stopping any services (this is just [ANALYZE](https://www.postgresql.org/docs/current/sql-analyze.html) without doing a vacuum, so it's faster)

**Note**: for the `vacuum-complete` and `vacuum-full` presets, you'll need plenty of available disk space in your Postgres data directory (usually `/mash/postgres/data`). These presets also stop all services while the vacuum operation is running.

Example playbook invocations:

- `just run-tags run-postgres-vacuum`: runs the default `vacuum-complete` preset and restarts all services
- `just run-tags run-postgres-vacuum -e postgres_vacuum_preset=analyze`: runs the `analyze` preset with all services remaining operational at all times


### Backing up PostgreSQL

To automatically make Postgres database backups on a fixed schedule, consider enabling the [Postgres Backup](postgres-backup.md) service.

To make a one-off back up of the current PostgreSQL database, make sure it's running and then execute a command like this on the server:

```bash
/usr/bin/docker exec \
--env-file=/mash/postgres/env-postgres-psql \
mash-postgres \
/usr/local/bin/pg_dumpall -h mash-postgres \
| gzip -c \
> /mash/postgres.sql.gz
```

Restoring a backup made this way can be done by [importing it](#importing).


### Upgrading PostgreSQL

Once this playbook installs Postgres for you, it attempts to preserve the Postgres version it starts with.
This is because newer Postgres versions cannot start with data generated by older Postgres versions.

Upgrades must be performed manually.

This playbook can upgrade your existing Postgres setup with the following command:

```sh
just run-tags upgrade-postgres
```

**The old Postgres data directory is backed up** automatically, by renaming it to `/mash/postgres/data-auto-upgrade-backup`.
To rename to a different path, pass some extra flags to the command above, like this: `--extra-vars="postgres_auto_upgrade_backup_data_path=/another/disk/mash-postgres-before-upgrade"`

The auto-upgrade-backup directory stays around forever, until you **manually decide to delete it**.

As part of the upgrade, the database is dumped to `/tmp`, an upgraded and empty Postgres server is started, and then the dump is restored into the new server.
To use a different directory for the dump, pass some extra flags to the command above, like this: `--extra-vars="postgres_dump_dir=/directory/to/dump/here"`

To save disk space in `/tmp`, the dump file is gzipped on the fly at the expense of CPU usage.
If you have plenty of space in `/tmp` and would rather avoid gzipping, you can explicitly pass a dump filename which doesn't end in `.gz`.
Example: `--extra-vars="postgres_dump_name=mash-postgres-dump.sql"`

**All databases, roles, etc. on the Postgres server are migrated**.


## Tuning PostgreSQL

PostgreSQL can be [tuned](https://wiki.postgresql.org/wiki/Tuning_Your_PostgreSQL_Server) to make it run faster. This is done by passing extra arguments to the Postgres process.

The [Postgres Ansible role](https://github.com/devture/com.devture.ansible.role.postgres) **already does some tuning by default**, which matches the [tuning logic](https://github.com/le0pard/pgtune/blob/master/src/features/configuration/configurationSlice.js) done by websites like https://pgtune.leopard.in.ua/.
You can manually influence some of the tuning variables . These parameters (variables) are injected via the `devture_postgres_postgres_process_extra_arguments_auto` variable.

Most users should be fine with the automatically-done tuning. However, you may wish to:

- **adjust the automatically-deterimned tuning parameters manually**: change the values for the tuning variables defined in the Postgres role's [default configuration file](https://github.com/devture/com.devture.ansible.role.postgres/blob/main/defaults/main.yml) (see `devture_postgres_max_connections`, `devture_postgres_data_storage` etc). These variables are ultimately passed to Postgres via a `devture_postgres_postgres_process_extra_arguments_auto` variable

- **turn automatically-performed tuning off**: override it like this: `devture_postgres_postgres_process_extra_arguments_auto: []`

- **add additional tuning parameters**: define your additional Postgres configuration parameters in `devture_postgres_postgres_process_extra_arguments_custom`. See `devture_postgres_postgres_process_extra_arguments_auto` defined in the Postgres role's [default configuration file](https://github.com/devture/com.devture.ansible.role.postgres/blob/main/defaults/main.yml) for inspiration


## Recommended other services

You may also wish to look into:

- [Postgres Backup](postgres-backup.md) for backing up your Postgres database

- [Prometheus](prometheus.md), [prometheus-postgres-exporter](prometheus-postgres-exporter.md) and [Grafana](grafana.md) for monitoring your Postgres database
