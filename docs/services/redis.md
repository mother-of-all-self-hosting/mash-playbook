# Redis

[Redis](https://redis.io/) is an open source, in-memory data store used by millions of developers as a database, cache, streaming engine, and message broker.

⚠️ We used to used to advocate for using Redis, but since [Redis is now "source available"](https://redis.com/blog/redis-adopts-dual-source-available-licensing/) we recommend that you use [Valkey](valkey.md) instead. Valkey is compatible with Redis, so switching should be straightforward. You can learn more about the switch from Redis to KeyDB in [this changelog entry](https://github.com/spantaleev/matrix-docker-ansible-deploy/blob/50813c600db1c47b1f3e76707b81fe05d6c46ef5/CHANGELOG.md#backward-compatibility-break-the-playbook-now-defaults-to-valkey-instead-of-redis) for [matrix-docker-ansible-deploy](https://github.com/spantaleev/matrix-docker-ansible-deploy). Since 2024-11-23, we recommend [Valkey](valkey.md) instead of [KeyDB](./keydb.md).

Some of the services installed by this playbook require a Redis data store.

> [!WARNING]
> Because Redis is not as flexible as [Postgres](postgres.md) when it comes to authentication and data separation, it's **recommended that you run separate Redis instances** (one for each service). Redis supports multiple database and a [SELECT](https://redis.io/commands/select/) command for switching between them. However, **reusing the same Redis instance is not good enough** because:

- if all services use the same Redis instance and database (id = 0), services may conflict with one another
- the number of databases is limited to [16 by default](https://github.com/redis/redis/blob/aa2403ca98f6a39b6acd8373f8de1a7ba75162d5/redis.conf#L376-L379), which may or may not be enough. With configuration changes, this is solveable.
- some services do not support switching the Redis database and always insist on using the default one (id = 0)
- Redis [does not support different authentication credentials for its different databases](https://stackoverflow.com/a/37262596), so each service can potentially read and modify other services' data

If you're only hosting a single service (like [PeerTube](peertube.md) or [NetBox](netbox.md)) on your server, you can get away with running a single instance. If you're hosting multiple services, you should prepare separate instances for each service.


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
