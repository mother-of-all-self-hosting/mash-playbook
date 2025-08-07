<!--
SPDX-FileCopyrightText: 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# KeyDB

The playbook can install and configure [KeyDB](https://docs.keydb.dev/) for you.

KeyDB is a fork of [Redis](redis.md), an open source, in-memory data store used by millions of developers as a database, cache, streaming engine, and message broker.

See the project's [documentation](https://docs.keydb.dev/) to learn what KeyDB does and why it might be useful to you.

Some of the services installed by this playbook require a Redis or its compatible data store including KeyDB and [Valkey](valkey.md). As this playbook supports both as well, we recommend using Valkey since 2024-11-23.

> [!WARNING]
> Because KeyDB is not as flexible as [Postgres](postgres.md) when it comes to authentication and data separation, it's **recommended that you run separate KeyDB instances** (one for each service). KeyDB supports multiple database and a [SELECT](https://docs.keydb.dev/docs/commands/#select) command for switching between them. However, **reusing the same KeyDB instance is not good enough** because:
>
> - if all services use the same KeyDB instance and database (id = 0), services may conflict with one another
> - the number of databases is limited to [16 by default](https://github.com/Snapchat/KeyDB/blob/0731a0509a82af5114da1b5aa6cf8ba84c06e134/keydb.conf#L342-L345), which may or may not be enough. With configuration changes, this is solvable.
> - some services do not support switching the KeyDB database and always insist on using the default one (id = 0)
> - KeyDB [does not support different authentication credentials for its different databases](https://stackoverflow.com/a/37262596), so each service can potentially read and modify other services' data
>
> If you're only hosting a single service (like [PeerTube](peertube.md) or [NetBox](netbox.md)) on your server, you can get away with running a single instance. If you're hosting multiple services, you should prepare separate instances for each service.


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process to **host a single instance of the KeyDB service**:

```yaml
########################################################################
#                                                                      #
# keydb                                                                #
#                                                                      #
########################################################################

keydb_enabled: true

########################################################################
#                                                                      #
# /keydb                                                               #
#                                                                      #
########################################################################
```

To **host multiple instances of the KeyDB service**, follow the [Running multiple instances of the same service on the same host](../running-multiple-instances.md) documentation or the **KeyDB** section (if available) of the service you're installing.

## Usage

After running the command for installation, the KeyDB instance becomes available.

The purpose of the KeyDB component in this Ansible playbook is to serve as a dependency for other [services](../supported-services.md). For this use-case, you don't need to do anything special beyond enabling the component per your choice (whether hosting a single instance or multiple ones).

## Related services

- [Redis](redis.md) — In-memory data store used by millions of developers as a database, cache, streaming engine, and message broker
- [Valkey](valkey.md) — Flexible distributed key-value datastore that is optimized for caching and other realtime workloads, forked from Redis
