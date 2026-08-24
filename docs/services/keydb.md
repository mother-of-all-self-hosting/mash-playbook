<!--
SPDX-FileCopyrightText: 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# KeyDB (removed)

🪦 The playbook used to be able to install and configure [KeyDB](https://docs.keydb.dev/), but no longer includes this service, as the KeyDB project has been unmaintained since 2023 (its last release, 6.3.4, dates from then) and the role to install it ([ansible-role-keydb](https://github.com/mother-of-all-self-hosting/ansible-role-keydb)) has been deprecated.

>[!NOTE]
> KeyDB is a fork of Redis, and [Valkey](valkey.md) (another Redis fork — the one this playbook has recommended since 2024-11-23) is protocol-compatible with it. Services that used to point at your KeyDB instance can point at a Valkey instance instead.

## Uninstalling the service manually

If you still have KeyDB installed on your server, the playbook can no longer help you uninstall it and you will need to do it manually. To uninstall manually, run these commands on the server:

```sh
systemctl disable --now mash-keydb.service

rm -rf /mash/keydb
```

If you were [running multiple instances of the KeyDB service](../running-multiple-instances.md), repeat the commands for each instance's service name and base path.

## Related services

- [Redis](redis.md) — In-memory data store used by millions of developers as a database, cache, streaming engine, and message broker
- [Valkey](valkey.md) — Flexible distributed key-value datastore that is optimized for caching and other realtime workloads, forked from Redis
