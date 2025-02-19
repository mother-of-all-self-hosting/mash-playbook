# ILMO

[Ilmo](https://github.com/moan0s/ILMO2) is an open source library management tool.

Read [the documentation](https://ilmo2.readthedocs.io/) to learn what you can do with it.

> [!WARNING]
> This service is a custom solution for a small library. Feel free to use it but don't expect a solution that works for every use case

## Dependencies

This service requires the following other services:

- a [Postgres](postgres.md) database
- a [Traefik](traefik.md) reverse-proxy server


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# ilmo                                                                 #
#                                                                      #
########################################################################

ilmo_enabled: true
ilmo_hostname: ilmo.example.com
ilmo_instance_name: "My library"

########################################################################
#                                                                      #
# /ilmo                                                                #
#                                                                      #
########################################################################
```

## Setting up the first user

You need to create a first user (unless you import an existing database).
You can do this conveniently by running

```bash
just run-tags ilmo-add-superuser --extra-vars=username=USERNAME --extra-vars=password=PASSWORD --extra-vars=email=EMAIL
```

## Usage

After installation, you can go to the ILMO URL, as defined in `ilmo_hostname`. Log in with the user credentials from above.

Follow the [ILMO documentation](https://ilmo2.readthedocs.io/en/latest/index.html) to learn how to use ILMO.

## Migrate an existing instance

The following assumes you want to migrate from `serverA` to `serverB` (managed by mash) but you just cave to adjust the copy commands if you are on the same server.

Stop the initial instance on `serverA`

```bash
serverA$ systemctl stop ilmo
```

Dump the database (depending on your existing setup you might have to adjust this)
```
serverA$ pg_dump ilmo > latest.sql
```

Copy the files to the new server

```bash
serverA$ rsync -av -e "ssh" latest.sql root@serverB:/mash/ilmo/
serverA$ rsync -av -e "ssh" data/* root@serverB:/mash/ilmo/data/
```

Install (but don't start) the service and database on the server and import the database.

```bash
yourPC$ just run-tags install-postgres
yourPC$ just run-tags install-ilmo
yourPC$ just run-tags import-postgres --extra-vars=server_path_postgres_dump=/mash/ilmo/latest.sql --extra-vars=postgres_default_import_database=mash-ilmo
```

Start the services on the new server

```bash
yourPC$ just run-tags start
```

Done 🥳

### Troubleshooting

If you by accident started the service before importing the database you should

* stop the service
* use `/mash/postgres/bin/cli` to get a database interface
* Delete the existing database (THIS WILL DELETE ALL DATA!) `DROP DATABASE ilmo WITH (FORCE);`
* Continue from "Install (but don't start) the service and database on the server and import the database."
