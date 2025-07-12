# MongoDB

[MongoDB](https://www.mongodb.com/) is a source-available cross-platform document-oriented (NoSQL) database program.

Some of the services installed by this playbook require a MongoDB database.

Enabling the MongoDB database service will automatically wire all other services which require such a database to use it.


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# mongodb                                                              #
#                                                                      #
########################################################################

mongodb_enabled: true

# Put a strong password below, generated with `pwgen -s 64 1` or in another way
mongodb_root_password: ''

########################################################################
#                                                                      #
# /mongodb                                                             #
#                                                                      #
########################################################################
```

## Importing

### Importing an existing MongoDB database from another installation (optional)

Follow this section if you'd like to import your database from a previous installation.

### Prerequisites

The playbook supports importing **gzipped** MongoDB database dumps (created with `mongodump --gzip -o /directory`).

Before doing the actual import, **you need to upload your MongoDB dump file to the server** (any path is okay).


### Importing a dump

To import, run this command (make sure to replace `SERVER_PATH_TO_MONGODB_DUMP_DIRECTORY` with a file path on your server):

```sh
just run-tags import-mongodb \
--extra-vars=mongodb_server_path_dump=SERVER_PATH_TO_MONGODB_DUMP_DIRECTORY
```

**Note** that `SERVER_PATH_TO_MONGODB_DUMP_DIRECTORY` must be a path to a **gzipped** MongoDB dump directory on the server (not on your local machine!)


## Maintenance

This section shows you how to perform various maintenance tasks related to the MongoDB database server used by various components of this playbook.

Table of contents:

- [Getting a database terminal](#getting-a-database-terminal), for when you wish to execute queries

- [Backing up MongoDB](#backing-up-mongodb), for when you wish to make a backup

### Getting a database terminal

You can use the `/mash/mongodb/bin/cli` tool to get interactive terminal access using the MongoDB Shell [mongosh](https://www.mongodb.com/docs/mongodb-shell/).

By default, this tool puts you in the `admin` database, which contains nothing.

To see the available databases, run `show dbs`.

To change to another database (for example `infisical`), run `use infisical`.

To see the available tables in the current database, run `show tables`.

You can then proceed to write queries. Example: `db.users.find()`

**Be careful**. Modifying the database directly (especially as services are running) is dangerous and may lead to irreversible database corruption.
When in doubt, consider [making a backup](#backing-up-mongodb).


### Backing up MongoDB

To make a one-off back up of the current MongoDB database, make sure it's running and then execute a command like this on the server:

```bash
# Prepare the backup directory
mkdir /path-to-some-directory
chown mash:mash /path-to-some-directory

# Back up
/mash/mongodb/bin/dump-all /path-to-some-directory
```

Restoring a backup made this way can be done by [importing it](#importing).
