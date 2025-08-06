<!--
SPDX-FileCopyrightText: 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Valkey

The playbook can install and configure [Valkey](https://valkey.io/) for you.

Valkey is a fork of [Redis](redis.md), a flexible distributed key-value datastore that is optimized for caching and other realtime workloads.

See the project's [documentation](https://valkey.io/docs/) to learn what Valkey does and why it might be useful to you.

Some of the services installed by this playbook require a Valkey data store. As this playbook supports [Redis](redis.md) and [KeyDB](keydb.md) as well, we recommend using Valkey since 2024-11-23.

> [!WARNING]
> Because Valkey is not as flexible as [Postgres](postgres.md) when it comes to authentication and data separation, it's **recommended that you run separate Valkey instances** (one for each service). Valkey supports multiple database and a [SELECT](https://valkey.io/commands/select/) command for switching between them. However, **reusing the same Valkey instance is not good enough** because:
>
> - if all services use the same Valkey instance and database (id = 0), services may conflict with one another
> - the number of databases is limited to [16 by default](https://github.com/valkey-io/valkey/blob/33f42d7fb597ce28040f184ee57ed86d6f6ffbd8/valkey.conf#L396), which may or may not be enough. With configuration changes, this is solvable.
> - some services do not support switching the Valkey database and always insist on using the default one (id = 0)
> - Valkey [does not support different authentication credentials for its different databases](https://stackoverflow.com/a/37262596), so each service can potentially read and modify other services' data
>
> If you're only hosting a single service (like [PeerTube](peertube.md) or [NetBox](netbox.md)) on your server, you can get away with running a single instance. If you're hosting multiple services, you should prepare separate instances for each service.

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process to **host a single instance of the Valkey service**:

```yaml
########################################################################
#                                                                      #
# valkey                                                               #
#                                                                      #
########################################################################

valkey_enabled: true

########################################################################
#                                                                      #
# /valkey                                                              #
#                                                                      #
########################################################################
```

To **host multiple instances of the Valkey service**, follow the [Running multiple instances of the same service on the same host](../running-multiple-instances.md) documentation or the **Valkey** section (if available) of the service you're installing.

## Usage

After installation, your Valkey instance becomes available.

The purpose of the Valkey component in this Ansible playbook is to serve as a dependency for other [services](../supported-services.md). For this use-case, you don't need to do anything special beyond enabling the component per your choice (whether hosting a single instance or multiple ones).

## Related services

- [KeyDB](keydb.md) — In-memory data store used by millions of developers as a database, cache, streaming engine, and message broker, forked from Redis
- [Redis](redis.md) — In-memory data store used by millions of developers as a database, cache, streaming engine, and message broker
