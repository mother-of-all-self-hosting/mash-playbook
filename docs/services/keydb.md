# KeyDB

[KeyDB](https://docs.keydb.dev/) is an open source, in-memory data store used by millions of developers as a database, cache, streaming engine, and message broker.

⚠️ We used to advocate for using [Redis](redis.md), but since [Redis is now "source available"](https://redis.com/blog/redis-adopts-dual-source-available-licensing/) we started recommending that you use KeyDB instead. KeyDB is compatible with Redis, so switching should be straightforward. You can learn more about the switch from Redis to KeyDB in [this changelog entry](https://github.com/spantaleev/matrix-docker-ansible-deploy/blob/50813c600db1c47b1f3e76707b81fe05d6c46ef5/CHANGELOG.md#backward-compatibility-break-the-playbook-now-defaults-to-keydb-instead-of-redis) for [matrix-docker-ansible-deploy](https://github.com/spantaleev/matrix-docker-ansible-deploy). Since 2024-11-23, we recommend [Valkey](valkey.md) instead of [KeyDB](./keydb.md).

Some of the services installed by this playbook require a KeyDB data store.

> [!WARNING]
> Because KeyDB is not as flexible as [Postgres](postgres.md) when it comes to authentication and data separation, it's **recommended that you run separate KeyDB instances** (one for each service). KeyDB supports multiple database and a [SELECT](https://docs.keydb.dev/docs/commands/#select) command for switching between them. However, **reusing the same KeyDB instance is not good enough** because:

- if all services use the same KeyDB instance and database (id = 0), services may conflict with one another
- the number of databases is limited to [16 by default](https://github.com/Snapchat/KeyDB/blob/0731a0509a82af5114da1b5aa6cf8ba84c06e134/keydb.conf#L342-L345), which may or may not be enough. With configuration changes, this is solvable.
- some services do not support switching the KeyDB database and always insist on using the default one (id = 0)
- KeyDB [does not support different authentication credentials for its different databases](https://stackoverflow.com/a/37262596), so each service can potentially read and modify other services' data

If you're only hosting a single service (like [PeerTube](peertube.md) or [NetBox](netbox.md)) on your server, you can get away with running a single instance. If you're hosting multiple services, you should prepare separate instances for each service.


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
