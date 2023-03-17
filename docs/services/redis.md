# Redis

[Redis](https://redis.io/) is an open source, in-memory data store used by millions of developers as a database, cache, streaming engine, and message broker.

Some of the services installed by this playbook require a Redis data store.

Enabling the Redis database service will automatically wire all other services to use it.


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

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
