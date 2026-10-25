<!--
SPDX-FileCopyrightText: 2023, 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2025, 2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Redis

The playbook can install and configure [Redis](https://redis.io/) for you.

Redis is a free and open-source, in-memory data store used as a database, cache, streaming engine, and message broker.

See the project's [documentation](https://redis.io/docs/latest/) to learn what Redis does and why it might be useful to you.

Some of the services installed by this playbook require a Redis (compatible) data store. As this playbook supports [Valkey](../valkey/README.md) as well, we recommend using Valkey since 2024-11-23.

For details about configuring the [Ansible role for Redis](https://github.com/mother-of-all-self-hosting/ansible-role-redis), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-redis/blob/main/docs/configuring-redis.md) online
- 📁 `roles/galaxy/redis/docs/configuring-redis.md` locally, if you have [fetched the Ansible roles](../../docs/installing.md)

> [!WARNING]
> Because Redis is not as flexible as [Postgres](../postgres/README.md) when it comes to authentication and data separation, it's **recommended that you run separate Redis instances** (one for each service). Refer to the role's documentation for details.
>
> If you're only hosting a single service (like [PeerTube](../peertube/README.md) or [NetBox](../netbox/README.md)) on your server, you can get away with running a single instance. If you're hosting multiple services, you should prepare separate ones for each service.

To host multiple instances of the Redis service, follow the [Running multiple instances of the same service on the same host](../../docs/running-multiple-instances.md) documentation.

## Related services

- [Valkey](../valkey/README.md) — Flexible distributed key-value datastore that is optimized for caching and other realtime workloads, forked from Redis
