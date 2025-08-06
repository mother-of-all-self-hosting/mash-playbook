<!--
SPDX-FileCopyrightText: 2023 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Redis

The playbook can install and configure [Redis](https://redis.io/) for you.

Redis is a free and open source, in-memory data store used by millions of developers as a database, cache, streaming engine, and message broker.

See the project's [documentation](https://redis.io/docs/latest/) to learn what Redis does and why it might be useful to you.

Some of the services installed by this playbook require a Redis (compatible) data store. As this playbook supports [Valkey](valkey.md) and [KeyDB](keydb.md) as well, we recommend using Valkey since 2024-11-23.

> [!NOTE]
> Starting from 8.0.0, Redis is licensed under your choice of the multiple licenses, one of which is AGPLv3. See [the release note for 8.0.0](https://github.com/redis/redis/releases/tag/8.0.0) for details.

> [!WARNING]
> Because Redis is not as flexible as [Postgres](postgres.md) when it comes to authentication and data separation, it's **recommended that you run separate Redis instances** (one for each service). Redis supports multiple database and a [SELECT](https://redis.io/commands/select/) command for switching between them. However, **reusing the same Redis instance is not good enough** because:
>
> - if all services use the same Redis instance and database (id = 0), services may conflict with one another
> - the number of databases is limited to [16 by default](https://github.com/redis/redis/blob/aa2403ca98f6a39b6acd8373f8de1a7ba75162d5/redis.conf#L376-L379), which may or may not be enough. With configuration changes, this is solvable.
> - some services do not support switching the Redis database and always insist on using the default one (id = 0)
> - Redis [does not support different authentication credentials for its different databases](https://stackoverflow.com/a/37262596), so each service can potentially read and modify other services' data
>
> If you're only hosting a single service (like [PeerTube](peertube.md) or [NetBox](netbox.md)) on your server, you can get away with running a single instance. If you're hosting multiple services, you should prepare separate instances for each service.

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process to **host a single instance of the Redis service**:

```yaml
########################################################################
#                                                                      #
# redis                                                                #
#                                                                      #
########################################################################

redis_enabled: true

########################################################################
#                                                                      #
# /redis                                                               #
#                                                                      #
########################################################################
```

To **host multiple instances of the Redis service**, follow the [Running multiple instances of the same service on the same host](../running-multiple-instances.md) documentation or the **Redis** section (if available) of the service you're installing.
