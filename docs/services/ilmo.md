<!--
SPDX-FileCopyrightText: 2020 Aaron Raimist
SPDX-FileCopyrightText: 2020 Chris van Dijk
SPDX-FileCopyrightText: 2020 Dominik Zajac
SPDX-FileCopyrightText: 2020 Mickaël Cornière
SPDX-FileCopyrightText: 2020-2024 MDAD project contributors
SPDX-FileCopyrightText: 2020-2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2022 François Darveau
SPDX-FileCopyrightText: 2022 Julian Foad
SPDX-FileCopyrightText: 2022 Warren Bailey
SPDX-FileCopyrightText: 2023 Antonis Christofides
SPDX-FileCopyrightText: 2023 Felix Stupp
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2023-2025 MASH project contributors
SPDX-FileCopyrightText: 2024 Thomas Miceli
SPDX-FileCopyrightText: 2024 noah
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# ILMO

The playbook can install and configure [Ilmo](https://github.com/moan0s/ILMO2) for you.

Ilmo is an open source library management tool.

See the project's [documentation](https://ilmo2.readthedocs.io/) to learn what ILMO does and why it might be useful to you.

> [!WARNING]
> This service is a custom solution for a small library. Feel free to use it but don't expect a solution that works for every use case

## Dependencies

This service requires the following other services:

- [Postgres](postgres.md) database
- [Traefik](traefik.md) reverse-proxy server

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

## Usage

After running the command for installation, the ILMO instance becomes available at the URL specified with `ilmo_hostname`. With the configuration above, the service is hosted at `https://ilmo.example.com`.

To log in to the service and get started, you have to create a user ("superuser") at first. To do so, run the command below after replacing `USERNAME`, `PASSWORD`, and `EMAIL_ADDRESS`:

```bash
ansible-playbook -i inventory/hosts setup.yml --tags=ilmo-add-superuser -e username=USERNAME -e password=PASSWORD -e email=EMAIL_ADDRESS
```

Follow the [ILMO documentation](https://ilmo2.readthedocs.io/en/latest/index.html) to learn how to use ILMO.

## Migrate an existing instance

If you want to migrate your existing ILMO instance with a Postgres database to another server, you can follow the procedure described as below.

**Note**: the following assumes you will migrate from **serverA** to **serverB**. Adjust the commands for copying files, if you are migrating on the same server (from an existing ILMO instance to the new one to start managing it with a playbook, for example).

### Stop the existing instance

First, stop the existing instance by logging in to **serverA** with SSH and running the command below.

```sh
serverA$ systemctl stop ilmo
```

### Dump database

Then, dump the database by running the command below. Note that you might have to adjust the command, depending on your existing installation.

```sh
serverA$ pg_dump ilmo > latest.sql
```

### Copy files to the new server

After dumping the database, let's copy data to a new server by using a tool such as `rsync`. To do so, log in to **serverA** with SSH, install it if not available, and then run the commands below.

```sh
serverA$ rsync -av -e "ssh" latest.sql root@serverB:/mash/ilmo/

serverA$ rsync -av -e "ssh" data/* root@serverB:/mash/ilmo/data/
```

### Install the service

Next, install the service by running the playbook as below on your local computer:

```sh
yourPC$ just run-tags install-postgres

yourPC$ just run-tags install-ilmo
```

**Do not run `start` tag yet.** Otherwise, the database could not be imported properly.

### Import the database

After installing it, import the database by running the playbook as below:

```sh
yourPC$ just run-tags import-postgres --extra-vars=server_path_postgres_dump=/mash/ilmo/latest.sql --extra-vars=postgres_default_import_database=mash-ilmo
```

### Start the services

After importing the database have completed, start the services by running the playbook:

```sh
yourPC$ just run-tags start
```

## Troubleshooting

If you by accident started the service before importing the database you should

- stop the service
- use `/mash/postgres/bin/cli` to get a database interface
- Delete the existing database (THIS WILL DELETE ALL DATA!) `DROP DATABASE ilmo WITH (FORCE);`
- Continue from "Install (but don't start) the service and database on the server and import the database."
