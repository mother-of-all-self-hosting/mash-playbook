<!--
SPDX-FileCopyrightText: 2023 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Redis

The playbook can install and configure [Redis](https://redis.io/) for you.

Redis is a free and open-source, in-memory data store used as a database, cache, streaming engine, and message broker.

See the project's [documentation](https://redis.io/docs/latest/) to learn what Redis does and why it might be useful to you.

Some of the services installed by this playbook require a Redis (compatible) data store. As this playbook supports [Valkey](valkey.md) as well, we recommend using Valkey since 2024-11-23.

For details about configuring the [Ansible role for Redis](https://github.com/mother-of-all-self-hosting/ansible-role-redis), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-redis/blob/main/docs/configuring-redis.md) online
- 📁 `roles/galaxy/redis/docs/configuring-redis.md` locally, if you have [fetched the Ansible roles](../installing.md)

> [!WARNING]
> Because Redis is not as flexible as [Postgres](postgres.md) when it comes to authentication and data separation, it's **recommended that you run separate Redis instances** (one for each service). Refer to the role's documentation for details.
>
> If you're only hosting a single service (like [PeerTube](peertube.md) or [NetBox](netbox.md)) on your server, you can get away with running a single instance. If you're hosting multiple services, you should prepare separate ones for each service.

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

To host multiple Redis instances, follow the [Running multiple instances of the same service on the same host](../running-multiple-instances.md) documentation.

## Usage

After running the command for installation, the Redis instance becomes available.

The purpose of Redis in this playbook is to serve as a dependency for other [services](../supported-services.md). Since this playbook no longer provides setting instructions for Redis but for Valkey, you can refer to these instructions and adjust them for Redis as necessary.

## Related services

- [Valkey](valkey.md) — Flexible distributed key-value datastore that is optimized for caching and other realtime workloads, forked from Redis
