# 2024-07-06

## Traefik v3 and HTTP/3 are here now

**TLDR**: Traefik was migrated from v2 to v3. Minor changes were done to the playbook. Mostly everything else worked out of the box. Most people will not have to do any tweaks to their configuration. In addition, [HTTP/3](https://en.wikipedia.org/wiki/HTTP/3) support is now auto-enabled for the `web-secure` (port 443) and `matrix-federation` (port `8448`) entrypoints. If you have a firewall in front of your server and you wish to benefit from `HTTP3`, you will need to open the `443` and `8448` UDP ports in it.

### Traefik v3

The reverse-proxy that the playbook uses by default (Traefik) has recently been upgraded to v3 (see [this blog post](https://traefik.io/blog/announcing-traefik-proxy-v3-rc/) to learn about its new features). Version 3 includes some small breaking configuration changes requiring a [migration](https://doc.traefik.io/traefik/migration/v2-to-v3/).

We have **updated the playbook to Traefik v3** (make sure to run `just roles` / `make roles` to get it).

Most (all) MASH roles should not require any changes and should work with Traefik v3 by default.

**Most people using the playbook should not have to do any changes**.

If you're using the playbook's Traefik instance to reverse-proxy to some other services of your own (not managed by the playbook), you may wish to review their Traefik labels and make sure they're in line with the [Traefik v2 to v3 migration guide](https://doc.traefik.io/traefik/migration/v2-to-v3/).

If you've tweaked any of this playbook's `_path_prefix` variables and made them use a regular expression, you will now need to make additional adjustments. The playbook makes extensive use of `PathPrefix()` matchers in Traefik rules and `PathPrefix` does not support regular expressions anymore. To work around it, you may now need to override a whole `_traefik_rule` variable and switch it from [`PathPrefix` to `PathRegexp`](https://doc.traefik.io/traefik/routing/routers/#path-pathprefix-and-pathregexp).

You **may potentially downgrade to Traefik v2** (if necessary) by adding `devture_traefik_verison: v2.11.4` to your configuration.


### HTTP/3 is enabled by default

In Traefik v3, [HTTP/3](https://en.wikipedia.org/wiki/HTTP/3) support is no longer considered experimental now.
Due to this, **the playbook auto-enables HTTP3** for the `web-secure` (port 443) entrypoint.

HTTP3 uses the UDP protocol and **the playbook (together with Docker) will make sure that the appropriate port** (`443` over UDP) **is exposed and whitelisted in your server's firewall**. However, **if you have another firewall in front of your server** (as is the case for many cloud providers), **you will need to manually open this UDP port**.

If you do not open the UDP port correctly or there is some other issue, clients (browsers, mostly) will fall-back to [HTTP/2](https://en.wikipedia.org/wiki/HTTP/2) or even [HTTP/1.1](https://en.wikipedia.org/wiki/HTTP).

Still, if HTTP/3 cannot function correctly in your setup, it's best to disable advertising support for it (and misleading clients into trying to use HTTP/3).

To **disable HTTP/3**, you can use the following configuration:

```yml
devture_traefik_config_entrypoint_web_secure_http3_enabled: false
```


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
