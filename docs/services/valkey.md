<!--
SPDX-FileCopyrightText: 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Valkey

The playbook can install and configure [Valkey](https://valkey.io/) for you.

Valkey is a fork of [Redis](redis.md), a flexible distributed key-value datastore that is optimized for caching and other realtime workloads.

See the project's [documentation](https://valkey.io/docs/) to learn what Valkey does and why it might be useful to you.

Some of the services installed by this playbook require a Valkey data store. As this playbook supports Redis as well, we recommend using Valkey since 2024-11-23.

For details about configuring the [Ansible role for Valkey](https://github.com/mother-of-all-self-hosting/ansible-role-valkey), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-valkey/blob/main/docs/configuring-valkey.md) online
- 📁 `roles/galaxy/valkey/docs/configuring-valkey.md` locally, if you have [fetched the Ansible roles](../installing.md)

> [!WARNING]
> Because Valkey is not as flexible as [Postgres](postgres.md) when it comes to authentication and data separation, it's **recommended that you run separate Valkey instances** (one for each service). Refer to the role's documentation for details.
>
> If you're only hosting a single service (like [PeerTube](peertube.md) or [NetBox](netbox.md)) on your server, you can get away with running a single instance. If you're hosting multiple services, you should prepare separate ones for each service.

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

To host multiple instances of the Valkey service, follow the [Running multiple instances of the same service on the same host](../running-multiple-instances.md) documentation or the **Valkey** section (if available) of the service you're installing.

## Usage

After running the command for installation, the Valkey instance becomes available.

The purpose of the Valkey component in this Ansible playbook is to serve as a dependency for other [services](../supported-services.md). For this use-case, you don't need to do anything special beyond enabling the component per your choice (whether hosting a single instance or multiple ones).

## Related services

- [Redis](redis.md) — In-memory data store used by millions of developers as a database, cache, streaming engine, and message broker
