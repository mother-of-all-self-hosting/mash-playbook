# Valkey

[Valkey](https://valkey.io/) is a flexible distributed key-value datastore that is optimized for caching and other realtime workloads.

Some of the services installed by this playbook require a Valkey data store.

> [!WARNING]
> Because Valkey is not as flexible as [Postgres](postgres.md) when it comes to authentication and data separation, it's **recommended that you run separate Valkey instances** (one for each service). Valkey supports multiple database and a [SELECT](https://valkey.io/commands/select/) command for switching between them. However, **reusing the same Valkey instance is not good enough** because:

- if all services use the same Valkey instance and database (id = 0), services may conflict with one another
- the number of databases is limited to [16 by default](https://github.com/valkey-io/valkey/blob/33f42d7fb597ce28040f184ee57ed86d6f6ffbd8/valkey.conf#L396), which may or may not be enough. With configuration changes, this is solveable.
- some services do not support switching the KeyDB database and always insist on using the default one (id = 0)
- Valkey [does not support different authentication credentials for its different databases](https://stackoverflow.com/a/37262596), so each service can potentially read and modify other services' data

If you're only hosting a single service (like [PeerTube](peertube.md) or [NetBox](netbox.md)) on your server, you can get away with running a single instance. If you're hosting multiple services, you should prepare separate instances for each service.


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process to **host a single instance of the KeyDB service**:

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
