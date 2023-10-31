# 2023-10-18

## Postgres parameters are automatically tuned now

The playbook has provided some hints about [Tuning PostgreSQL](docs/maintenance-postgres.md#tuning-postgresql) for quite a while now.

From now on, the [Postgres Ansible role](https://github.com/devture/com.devture.ansible.role.postgres) automatically tunes your Postgres configuration with the same [calculation logic](https://github.com/le0pard/pgtune/blob/master/src/features/configuration/configurationSlice.js) that powers https://pgtune.leopard.in.ua/.

Our [Tuning PostgreSQL](docs/maintenance-postgres.md#tuning-postgresql) documentation page has details about how you can turn auto-tuning off or adjust the automatically-determined Postgres configuration parameters manually.


# 2023-04-23

## (Backward Compatibility Break) Authentik container variables renamed

For the authentik role there wehre initially two containers: `authentic_worker_container` and `authentic_server_container`. To simnplifiy the setup this was reduced to one container.
As the role is pretty young and to avoid confusion because of legacy and reverted design decisions all variables containing `authentik_server_container` will now start with authentik_container. This means you will have to renemae these variables in your `vars.yml` if you already use authentik. If you use a standard setup this only includes

* `authentic_server_container_additional_networks_custom` -> `authentik_container_additional_networks_custom`

# 2023-03-29

## (Backward Compatibility Break) Firezone database renamed

If you are running [Firezone](docs/services/firezone.md) with the default [Postgres](docs/services/postgres.md) integration the playbook automatically created the database with the name `mash-firezone`.
To be consistent with how this playbook names databases for all other services, going forward we've changed the database name to be just `firezone`. You will have to rename you database manually by running the following commands on your server:

1. Stop Firezone: `systemctl stop mash-firezone`
2. Run a Postgres `psql` shell: `/mash/postgres/bin/cli`
3. Execute this query: `ALTER DATABASE "mash-firezone" RENAME TO firezone;` and then quit the shell with `\q`

Then update the playbook (don't forget to run `just roles`), run `just install-all` and you should be good to go!

# 2023-03-26

## (Backward Compatibility Break) PeerTube is no longer wired to Redis automatically

As described in our [Redis](docs/services/redis.md) services docs, running a single instance of Redis to be used by multiple services is not a good practice.

For this reason, we're no longer auto-wiring PeerTube to Redis. If you're running other services (which may require Redis in the future) on the same host, it's recommended that you follow the [Creating a Redis instance dedicated to PeerTube](docs/services/peertube.md#creating-a-redis-instance-dedicated-to-peertube) documentation.

If you're only running PeerTube on a dedicated server (no other services that may need Redis) or you'd like to stick to what you've used until now (a single shared Redis instance), follow the [Using the shared Redis instance for PeerTube](docs/services/peertube.md#using-the-shared-redis-instance-for-peertube) documentation.


# 2023-03-25

## (Backward Compatibility Break) Docker no longer installed by default

The playbook used to install Docker and the Docker SDK for Python by default, unless you turned these off by setting `mash_playbook_docker_installation_enabled` and `devture_docker_sdk_for_python_installation_enabled` (respectively) to `false`.

From now on, both of these variables default to `false`. An empty inventory file will not install these components.

**Most** users will want to enable these, just like they would want to enable [Traefik](docs/services/traefik.md) and [Postgres](docs/services/postgres.md), so why default them to `false`? The answer is: it's cleaner to have "**everything** is off by default - enable as you wish" and just need to add stuff, as opposed to "**some** things are on, **some** are off - toggle as you wish".

To enable these components, you need to explicitly add something like this to your `vars.yml` file:

```yaml
########################################################################
#                                                                      #
# Docker                                                               #
#                                                                      #
########################################################################

mash_playbook_docker_installation_enabled: true

devture_docker_sdk_for_python_installation_enabled: true

########################################################################
#                                                                      #
# /Docker                                                              #
#                                                                      #
########################################################################
```

Our [example vars.yml](examples/vars.yml) file has been updated, so that new hosts created based on it will have this configuration by default.


# 2023-03-15

## Initial release

This is the initial release of this playbook.
