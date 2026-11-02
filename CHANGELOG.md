# CHANGELOG

## 2026-10-30

### Woodpecker CI's directories moved

Woodpecker CI's server and agent directories moved from `/mash/woodpecker-ci/server` and `/mash/woodpecker-ci/agent` to `/mash/woodpecker-ci-server` and `/mash/woodpecker-ci-agent`. Their shared parent directory was owned by the `mash` user, who could rename the agent's directory (now owned by root) and put another in its place.

The next playbook run moves the server's directory, recreates the agent's, and deletes the old parent once it is empty. If you set `woodpecker_ci_server_base_path` or `woodpecker_ci_agent_base_path` in your `vars.yml`, your paths are left alone. To skip the migration, set `mash_playbook_migration_woodpecker_ci_paths_migration_enabled: false` (not recommended).

### The base directory (`/mash`) is now owned by root

The playbook now makes the base directory (`mash_playbook_base_path`, `/mash` by default) owned by `root`, with the `mash` group and the same mode (`0750`). Previously it was owned by the `mash` user.

Whoever owns this directory can rename any service's directory in it, even one owned by root, and put another in its place. A service that runs something as root from its directory relies on this not being possible.

Nothing changes for you: the services' own directories keep their owners, and the `mash` user can still reach them through the group. The next playbook run changes the owner. To keep the old owner, set `mash_playbook_base_path_uid: "{{ mash_playbook_uid }}"` in your `vars.yml` (not recommended).

## 2026-10-25

### The playbook's wiring moved from `templates/` to `components/`

This affects you only if you run the playbook without `just`, or keep local changes to the files in `templates/`. If you use `just` and your inventory, nothing changes for you: your inventory stays as it is, and the playbook configures your services as before.

Each role the playbook can use is now wired in by a component in [`components/`](components) (one directory per role), instead of `templates/group_vars_mash_servers`, `templates/requirements.yml` and `templates/setup.yml`. Before each run, `just` generates `requirements.yml`, `setup.yml` and `group_vars/mash_servers/` (now a directory) from the components your inventory uses.

**If you run the playbook without `just`**, generate these files from `components/` after each update instead of copying the templates, as described in [Installing](docs/installing.md).

**If you changed files in `templates/`**, move your changes to your inventory (e.g. `vars.yml`), which overrides the playbook's wiring, and discard them (`git checkout -- templates/`) before updating, as `just update` cannot pull the playbook otherwise. See the [developer documentation](docs/developer-documentation.md#3-update-the-mash-playbook-to-support-your-created-ansible-role) for the structure of components.

**If you go back to an older version of the playbook** (e.g. with `git checkout`), delete the generated directory first (`rm -r group_vars/mash_servers`), as older versions generate a file in its place.

### Your inventory can have components of its own

You can now extend the playbook with components in your inventory's `components/` directory (e.g. `inventory/components/`): to run your own tasks at a given point of the run, to install a service with a role the playbook does not support, or to register your own systemd services. See [Extending the playbook with your own components](docs/extending-the-playbook.md).

**If your inventory already has a `components/` directory for something else**, move it elsewhere: the playbook now reads it, and stops with an error, because it does not contain components.

### The playbook is now optimized by default, and installs its roles on its own

This affects everyone. Before running the playbook (e.g. with `just install-all`), the `just` recipes now:

- include only the roles of the services enabled in your inventory (its `host_vars` and `group_vars`). Previously, this optimization had to be enabled with `just optimize`.
- install missing and outdated roles, and delete the roles of services which are no longer in use. `just roles` is no longer needed after pulling the playbook or enabling a service.

See [Ansible roles and optimization](docs/just.md#ansible-roles-and-optimization) for details.

**If you enable services only through variables in your `hosts` file, or with `--extra-vars` on the command line**, the optimization does not see them, so these services would be left out. Before your first run after updating, move these variables to `vars.yml` (or another file in `host_vars`/`group_vars`), or run `just optimize-disable` to include all roles.

`just optimize`, `just optimize-reset`, `just optimize-restore` and `just optimize-for-host` have been removed: optimization is now always for your whole inventory and kept up to date on its own. To turn it off, use `just optimize-disable` (and `just optimize-enable` to turn it on again).

## 2026-10-20

### FMD Server 0.17: back up before upgrading

This affects existing FMD Server installations. Before rerunning the playbook, follow the [upstream upgrade precautions](https://fmd-foss.org/blog/2026/09/18/api-v2/#what-changes-for-server-operators): back up the SQLite database and test the upgrade and user-facing functionality in a staging environment. For a consistent file backup, stop FMD Server and copy its database directory (`fmd_server_database_path`, normally `/mash/findmydeviceserver/database`). The role does not make this backup or issue a validation error reminding you to do so.

The API and encryption rewrite remains backward compatible with existing accounts and clients. Account migration to API v2 is available through the Android app; it is not required for this server upgrade.

### Homarr v2 requires a backup before upgrading

This affects existing Homarr v1 installations. Before rerunning the playbook, stop Homarr and back up its data directory (`homarr_data_path`, normally `/mash/homarr/data`) and, if you use Postgres for it, its Postgres database. The first v2 start migrates the database in place, and Homarr v1 cannot use the migrated database, so rolling back requires restoring the backup. The role neither makes the backup nor stops with a validation error to remind you.

Homarr v2 no longer supports MySQL (and MariaDB). If you have set `homarr_database_type: mysql`, the role stops with an error: before upgrading, convert the database to SQLite while still on Homarr v1.77 (the version the playbook installed until now) by following the [upstream migration guide](https://homarr.dev/docs/advanced/mysql-to-sqlite), then set `homarr_database_type: sqlite`.

Refer to the [upstream release notes](https://github.com/homarr-labs/homarr/releases/tag/v2.0.0) for other application changes.

## 2026-10-18

### `just start-all` and `just start-group` restart all targeted services again

Since [conditional service restart](#conditional-service-restart-for-install--commands) was introduced, it also applied to runs with only start or restart tags. As more roles began tracking their own changes, these commands stopped restarting most services and only started those that were stopped.

Conditional restart now applies only when an `install-*` tag is selected and no `setup-*` tag. `just install-all` and `just install-service` are unchanged. `just start-all`, `just start-group` and other runs with only start or restart tags restart all their targeted services again, so they briefly interrupt running services. To keep the previous behavior for such a run, add `--extra-vars='devture_systemd_service_manager_conditional_restart_enabled=true'`.

## 2026-10-15

### Uptime Kuma v2 requires a backup before upgrading

This affects existing Uptime Kuma v1 installations. Before rerunning the playbook, stop Uptime Kuma and back up its data directory (`uptime_kuma_data_path`, normally `/mash/uptime-kuma/data`). The first v2 start migrates the database; allow it to finish without restarting the service or host. Migration can take hours, and interruption requires restoring the backup.

Debian/Raspbian Buster hosts must be upgraded to a newer OS before moving to v2: upstream reports container startup failures with Buster's `libseccomp2`. See the [upstream migration guide](https://github.com/louislam/uptime-kuma/wiki/Migration-From-v1-To-v2) for other application changes.

Follow the [role's upgrade instructions](https://github.com/mother-of-all-self-hosting/ansible-role-uptime_kuma/blob/v2.5.6-0/docs/configuring-uptime-kuma.md#upgrading-from-uptime-kuma-1x-to-2x) before upgrading. The role starts the upgrade automatically and does not make the backup or stop with a validation error to remind you.

## 2026-10-12

### (Backward Compatibility Break) TSDProxy upgraded to v2

This only affects you if you have [TSDProxy](components/tsdproxy/README.md) enabled and use proxy lists (`tsdproxy_config_files`).

TSDProxy v2 changed the format of proxy list files. The role does not manage these files, so it cannot check or convert them: before re-running the playbook, migrate them by hand following the [upstream upgrade guide](https://almeidapaulopt.github.io/tsdproxy/docs/upgrading/from-v1/), and define them with `tsdproxy_config_lists` instead of `tsdproxy_config_files`.

The role reports its other changes (renamed variables, TSDProxy v1 keys in custom configuration) with actionable errors, and container labels in the TSDProxy v1 format keep working. See the [role's upgrade notes](https://github.com/mother-of-all-self-hosting/ansible-role-tsdproxy#upgrading-from-tsdproxy-v1) for details.

## 2026-10-10

### (Backward Compatibility Break) Safer Docker cleanup, and no more journald vacuuming by default

This only affects you if you use the [cleanup](components/cleanup/README.md) role (any `system_cleanup_*` variable in your `vars.yml`).

The role has been upgraded to v2:

- **`system_cleanup_docker`** no longer runs `docker image prune -a` and `docker volume prune`. It now removes stopped containers and only those unused images which a newer image of the same repository superseded at least 3 days ago. Unused images without a newer version (of stopped services, timer-only containers, locally built images) are kept, and anonymous volumes are left alone unless you enable `system_cleanup_docker_config_remove_anonymous_volumes`. To remove superseded images right away, set `system_cleanup_docker_config_superseded_images_grace_period_days: 0`. The cleanup now lives in a script (`/mash/system-cleanup/bin/cleanup-docker`), which you can also run by hand (`--dry-run` shows what it would remove) or on a schedule (`system_cleanup_docker_timer_enabled: true`).
- **The journald vacuum timer** (`journalctl --vacuum-time=7d`) was installed on every host, whatever `system_cleanup_logs` said. It now follows `system_cleanup_logs`, which defaults to `false`, so the timer gets removed. journald already limits the space logs take up on its own. To keep the timer, set `system_cleanup_logs: true`.
- **`purge-old-kernels`** (`system_cleanup_kernels`) moved from `/usr/local/bin` to `/mash/system-cleanup/bin`.

See the role's [upgrade notes](https://github.com/mother-of-all-self-hosting/ansible-role-cleanup#upgrading-to-v2) for details.

## 2026-10-03

### The playbook's container image is no longer published

This only affects you if you run the playbook using the `ghcr.io/mother-of-all-self-hosting/mash-playbook` container image.

This image bundled the playbook and its roles, but was never part of the documented ways of running the playbook. Its build, which fetched every role from many separate git hosts, failed regularly because of temporary network errors. We have stopped building it, and the existing image will no longer receive updates.

If you used it, clone the playbook and run it with your own Ansible, or with the [`ghcr.io/devture/ansible`](https://github.com/devture/docker-ansible/pkgs/container/ansible) container image as described in [Using Ansible via Docker](docs/ansible.md#using-ansible-via-docker).

## 2026-09-27

### Jellyfin 12 requires preparation before upgrading

This affects users with Jellyfin enabled. Before rerunning the playbook, stop Jellyfin and make a full backup of its data and configuration. Check for usernames that differ only by capitalization, and remove third-party plugins until versions compatible with Jellyfin 12 are available. After the upgrade, run a full library scan; let the database migrations and first scan finish without interruption. The database changes cannot be rolled back without restoring a backup. See the [Jellyfin 12 release notes](https://jellyfin.org/posts/jellyfin-release-12.0/) for details.

## 2026-08-25

### APISIX Dashboard support removed

This only affects you if you have the standalone APISIX Dashboard (`apisix_dashboard_*` variables) enabled.

Upstream no longer ships the APISIX Dashboard as a service of its own: it is now served by APISIX itself (since 3.13), at `/ui/` on its Admin API port. Its last standalone release (3.0.1, from March 2023) was only meant for APISIX 3.0. The role that installed it ([ansible-role-apisix-dashboard](https://github.com/mother-of-all-self-hosting/ansible-role-apisix-dashboard)) has been deprecated.

You don't need to install anything to use the bundled dashboard. Making it reachable makes the Admin API reachable, and the bundled dashboard has no login of its own, so see [the APISIX role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-apisix/blob/main/docs/configuring-apisix.md#configuring-the-bundled-dashboard-web-ui) for the safe ways to reach it.

Remove the `apisix_dashboard_*` variables from your `vars.yml`, and uninstall the standalone dashboard manually, by running these commands on your server:

```sh
systemctl disable --now mash-apisix-dashboard.service

rm -rf /mash/apisix-dashboard
```

If you were [running multiple instances of the APISIX Dashboard service](docs/running-multiple-instances.md), repeat the commands for each instance's service name and base path. Your APISIX configuration (routes, upstreams, etc.) is stored in [etcd](components/etcd/README.md), and is not affected.

## 2026-08-24

### (Backward Compatibility Break) KeyDB support removed

This only affects you if you have KeyDB enabled.

KeyDB has been removed from the playbook, because the KeyDB project has been unmaintained since 2023 — its last release (6.3.4) dates from then. The role that installed it ([ansible-role-keydb](https://github.com/mother-of-all-self-hosting/ansible-role-keydb)) has been deprecated.

[Valkey](components/valkey/README.md) — also a Redis fork, protocol-compatible with KeyDB — is a well-maintained alternative and has been the playbook's recommendation since 2024-11-23. Point services that used your KeyDB instance at a Valkey instance instead.

The playbook will complain about any remaining `keydb_*` variables in your configuration. Remove them, and uninstall the service from your server manually, by running these commands on it:

```sh
systemctl disable --now mash-keydb.service

rm -rf /mash/keydb
```

If you were [running multiple instances of the KeyDB service](docs/running-multiple-instances.md), repeat the commands for each instance's service name and base path.

## 2026-08-20

### Updated Infisical requires manual database migration from MongoDB to Postgres

[Infisical](components/infisical/README.md) transitioned from MongoDB to Postgres backend on [v0.46.11](https://hub.docker.com/layers/infisical/infisical/v0.46.11-postgres/). The role to install the application ([ansible-role-infisical](https://github.com/mother-of-all-self-hosting/ansible-role-infisical)) does not provide an automated method to conduct database migration from MongoDB, so it is necessary to conduct manual migration if you have deployed an old Infisical instance with the playbook and wish to keep the data. Refer to [this page](https://infisical.com/docs/self-hosting/guides/mongo-to-postgres) for details about migration.

## 2026-08-06

### (Backward Compatibility Break) Jitsi no longer uses Colibri WebSockets

This only affects you if you have [Jitsi](components/jitsi/README.md) enabled.

Jitsi has been updated to `stable-11146-1`, which [removes Colibri WebSocket support](https://github.com/jitsi/docker-jitsi-meet/pull/2285) in favour of SCTP data channels. The Jitsi Video Bridge no longer serves HTTP at all, so a few `jitsi_jvb_*` variables are gone. The playbook will tell you which ones, if your configuration still sets them.

If you run [additional JVBs on other hosts](https://github.com/mother-of-all-self-hosting/ansible-role-jitsi/blob/main/docs/configuring-jitsi.md#set-up-additional-jvbs-for-more-video-conferences-optional), the Traefik configuration which routed `/colibri-ws/<server-id>/` to them is now dead and can be removed. Nothing will warn you about that one, as it lives in a free-form `traefik_provider_configuration_extension_yaml` block.

## 2026-07-28

### (Backward Compatibility Break) ntfy users are now declared with hashed passwords

This only affects you if you have enabled authentication for [ntfy](components/ntfy/README.md) via `ntfy_credentials`.

The ntfy role used to create users by invoking `ntfy user` commands against the running container. Since v2.14.0, ntfy can provision users and access-control entries from its own configuration file, so the role now does that instead. Besides being a lot simpler, this fixes passwords containing spaces never arriving intact.

Replace `ntfy_credentials` with `ntfy_auth_users_custom`, which takes bcrypt password hashes rather than plaintext passwords:

```yaml
ntfy_auth_users_custom:
  - username: alice
    password_hash: $2a$10$YLiO8U21sX1uhZamTLJXHuxgVC0Z/GKISibrKCLohPgtG7yIxSk4C
    role: admin
```

Generate a hash for each of your passwords by running the following command on any machine which has Docker installed. It asks for the password and prints its hash:

```sh
docker run --rm -it docker.io/binwiederhier/ntfy:latest user hash
```

The playbook will let you know if your configuration still uses `ntfy_credentials`.

Your existing ntfy users are left alone and keep working until you declare them again this way. Note that ntfy manages declared users and access-control entries declaratively, so removing one from your configuration later deletes it from ntfy's user database.

Users with the `admin` role get access to all topics. Others start with no access at all, and can be granted access to specific topics via `ntfy_auth_access_custom`. It is also now possible to control what unauthenticated visitors may do (`ntfy_auth_default_access`) and whether users may log in at all (`ntfy_enable_login`, which follows your authentication setup by default). See the role's [documentation on access control](https://github.com/mother-of-all-self-hosting/ansible-role-ntfy/blob/main/docs/configuring-ntfy.md#enable-access-control-with-authentication-optional) for details.

## 2026-03-19

### Firezone has been removed from the playbook

[Firezone](https://www.firezone.dev/) has been removed from the playbook, as the role to install it ([ansible-role-firezone](https://github.com/mother-of-all-self-hosting/ansible-role-firezone)) was deprecated in favor of [ansible-role-wg-easy](https://github.com/mother-of-all-self-hosting/ansible-role-wg-easy). The deprecated role was configured to install the legacy 0.7 version, which has reached end-of-life status and stopped receiving updates since January 31st, 2024.

The playbook will let you know if you're using any `firezone_*` variables. You'll need to remove them from `vars.yml`. If you still have Firezone installed on your server, uninstall it manually, by running these commands on it:

```sh
systemctl disable --now mash-firezone.service

rm -rf /mash/firezone

/mash/postgres/bin/cli-non-interactive -c 'DROP DATABASE firezone;'
```

If you have deployed Firezone, you might be interested in having a look at [WireGuard Easy](components/wg_easy/README.md).

## 2026-02-13

### Conditional service restart for `install-*` commands

When running `install-all` or `install-service` (whether via `just` or raw `ansible-playbook`), only services whose configuration or container image actually changed during the playbook run will now be restarted. Unchanged services are left running (or get started if they were stopped). This reduces unnecessary downtime — particularly for services like Traefik (the reverse proxy), which previously caused brief connectivity interruptions on every playbook run even when nothing changed.

When running with `setup-*` tags (e.g. `setup-all`, `setup-miniflux`), all services continue to be unconditionally restarted as before.

Currently, only Traefik tracks its own changes and benefits from conditional restart. All other services default to being restarted (the previous behavior). This is just the beginning — as more roles gain change-tracking support, playbook performance will improve and downtime will decrease dramatically, especially for `install-all` runs where most services haven't changed.

Some benchmarks from [matrix-docker-ansible-deploy](https://github.com/spantaleev/matrix-docker-ansible-deploy) for `just install-service traefik` when Traefik settings did not change (results here may vary, but should be similar):

- **Before**:
  - total time: ~56 seconds 🐌
  - Traefik restarted: yes (unnecessarily) ❌
  - dependent services restarted: yes, all of them ❌
- **After**:
  - total time: ~27 seconds ⚡
  - Traefik restarted: no ✅
  - dependent services restarted: no ✅

This behavior can be overridden via `--extra-vars='devture_systemd_service_manager_conditional_restart_enabled=false'` to force unconditional restarts. Refer to [Conditional service restart](docs/just.md#conditional-service-restart) for details.

### Set service passwords on `vars.yml` manually

After switching the algorithm of secret derivation for service passwords, it was found that some of the services which need secret strings have stopped working, as those strings were never meant to be auto-configured and should not be changed after initial configuration.

Here are the list of known affected services:

| Service name   | Command to retrieve value                                  | variable to be added on `vars.yml`                               |
| -------------- | ---------------------------------------------------------- | ---------------------------------------------------------------- |
| Duplicati      | grep 'SETTINGS_ENCRYPTION_KEY' /mash/duplicati/env         | `duplicati_environment_variable_settings_encryption_key`         |
| Homarr         | grep 'AUTH_SECRET' /mash/homarr/env                        | `homarr_environment_variables_auth_secret`                       |
| Meilisearch    | grep 'MEILI_MASTER_KEY' /mash/meilisearch/env              | `meilisearch_environment_variables_master_key`                   |
| Papra          | grep 'AUTH_SECRET' /mash/papra/env                         | `papra_environment_variables_auth_secret`                        |
| Pocket ID      | grep 'ENCRYPTION_KEY' /mash/pocket-id/env                  | `pocket_id_environment_variable_encryption_key`                  |
| syncstorage-rs | grep 'SYNC_MASTER_SECRET' /mash/syncstorage-rs-docker/env  | `syncstorage_rs_docker_environment_variable_sync_master_secret`  |
| syncstorage-rs | grep 'METRICS_HASH_SECRET' /mash/syncstorage-rs-docker/env | `syncstorage_rs_docker_environment_variable_metrics_hash_secret` |
| Typesense      | grep 'ENCRYPTION_KEY' /mash/typesense/env                  | `typesense_environment_variables_api_key`                        |

If you use a certain cervice on the list, please run the command on the server to retrieve the value, and specify the output value to the variable for it on your `vars.yml` file.

If you are not sure how to retrieve the value, you can check diff available [`a7386bb3f4fcae99229566cf81c127e590cda230`](https://github.com/mother-of-all-self-hosting/mash-playbook/commit/a7386bb3f4fcae99229566cf81c127e590cda230) and set the previous value to generate it temporarily.

## 2026-02-08

### Switched to faster secret derivation for service passwords

We've switched the method used for deriving service passwords (database passwords,
appservice tokens, etc.) from the `mash_playbook_generic_secret_key` variable.

The old method used `password_hash('sha512', rounds=655555)` (655,555 rounds of
SHA-512 hashing), which was designed for protecting low-entropy human passwords
against brute-force attacks. For deriving secrets from an already high-entropy
secret key, this many rounds provide no additional security.

The new method uses a single-round `hash('sha512')` with a unique salt per service.
This is equally secure for this use case while being dramatically faster.

**What this means for users**: all derived service passwords will change on the
next playbook run. The main/superuser database password (`postgres_connection_password`)
is not affected. All services will receive their new passwords as part of the same
run, so this should be a seamless, non-user-impacting change.

## 2025-10-29

### Miniflux upgrade to v2.2.14 may require manual work

Due to a migration in Miniflux v2.2.14, you may find that your Miniflux service fails to start with an error:

> [Migration v119] pq: must be owner of extension hstore

[This issue](https://github.com/miniflux/v2/issues/3849) affects older Miniflux installations which made use of an `hstore` Postgres extension. If the `hstore` extension is owned by a user other than `miniflux`, the migration trying to drop it will hit an error. Newer Miniflux versions never installed that extension and the migration does not need to drop it.

You can fix this issue before upgrading to Miniflux v2.2.14 or after an unsuccessful upgrade by:

1. Running this one-liner on your MASH server: `/mash/postgres/bin/cli-non-interactive -d miniflux -c "DROP EXTENSION IF EXISTS hstore;"`
2. Restarting the Miniflux service

## 2025-10-28

### authentik no longer requires a Redis-compatible datastore

Since authentik [2025.10.0](https://docs.goauthentik.io/releases/2025.10), a Redis-compatible datastore (we used to recommend [Valkey](components/valkey/README.md)) is no longer necessary. authentik no longer uses a Redis-compatible datastore at all (moving all that into Postgres).

If you have an existing authentik installation, you may now wish to remove all Valkey-related integration settings.

## 2025-10-22

### Adapting Immich/Postgres to changes in the Postgres role

The [Postgres](components/postgres/README.md) role was recently updated (refer to [this commit](https://github.com/mother-of-all-self-hosting/ansible-role-postgres/commit/b39dcdf3421a4b3d7c4a758c9b533399ede4547b)) to add support for restricting the versions that it's allowed to install.

These changes have landed into MASH playbook and we're making use of them to make [Postgres](components/postgres/README.md) play better with [Borg Backup](components/backup_borg/README.md) and avoid the risk of suffering from issues like this: [Unable to use borg backup after postgresql 18 upgrade](https://github.com/spantaleev/matrix-docker-ansible-deploy/issues/4632).

Due to these changes, **users who install Immich/Postgres** for the [Immich](components/immich/README.md) service now **need to update their `vars.yml` file** [like this](https://github.com/mother-of-all-self-hosting/mash-playbook/commit/297c414bddb37f82e066d14b66b4ae2cf4b78318), or the playbook will encourage them to upgrade to *vanilla* Postgres v18 (which is not what Immich needs).

While at it, Immich users can **consider upgrading to Immich/Postgres v18** as described in the comments seen in [the same commit](https://github.com/mother-of-all-self-hosting/mash-playbook/commit/297c414bddb37f82e066d14b66b4ae2cf4b78318) and using a new variable override of `postgres_container_image_v18_version: 18-vectorchord0.5.3-pgvector0.8.1`. After all the upgrade steps and final cleanup are done, your `vars.yml` would only contain Postgres v18 references, as seen [here](https://github.com/mother-of-all-self-hosting/mash-playbook/commit/f4dff6927e12eda413e768ab5a58ab09a434c1ba).

## 2025-08-11

### Tandoor 2.0 Update: Path Prefix & API Changes

#### (BC Break) Tandoor can no longer be installed under a path prefix

Right now, installing Tandoor under a path prefix like `/tandoor/` isn’t supported anymore.

So please make sure in your setup that:

- you **don’t set** the `tandoor_path_prefix` variable
- you **don’t override** the `tandoor_container_labels_traefik_path_prefix` variable

> [!NOTE]
> If you want to keep using a path prefix, you’ll need to:
>
> - comment out the last `fail` task (lines 36–39) in the `validate-config.yml` of the Tandoor Ansible role
> - tweak the nginx template to properly handle a prefixed path (like fixing location blocks, headers, and static/media file serving)
>
> This isn’t officially supported right now — but **we’d be happy if you contribute a pull request to bring back smooth path prefix support!**

---

#### Tandoor updated to version 2.0 — API changes may break third-party apps

Tandoor has been updated to version 2.0. This release includes **breaking changes to the API**, which may cause some third-party apps to stop working.

Here’s what that means:

- **Untare** was built for the old API — it no longer works with Tandoor 2.0 and is **no longer maintained**
- **Kitshn** is being actively developed, but only a **beta version** supports Tandoor 2.0

You can find more details in the official release notes: <https://github.com/TandoorRecipes/recipes/releases/tag/2.0.0>

## 2025-03-08

### 6️⃣ IPv6 support enablement recommended by default

Our [default example configuration](./examples/vars.yml) and [Configuring DNS](./docs/configuring-dns.md) guides now recommend enabling [IPv6](https://en.wikipedia.org/wiki/IPv6) support. We recommend that everyone enables IPv6 support for their Matrix server, even if they don't have IPv6 connectivity yet.

Our new [Configuring IPv6](./docs/configuring-ipv6.md) documentation page has more details about the playbook's IPv6 support.

**Existing playbook users** will **need to do some manual work** to enable IPv6 support. This consists of:

- enabling IPv6 support for the Docker container networks:
  - add `devture_systemd_docker_base_ipv6_enabled: true` to their `vars.yml` configuration file
  - stop all services (`just stop-all`)
  - delete all container networks on the server: `docker network rm $(docker network ls -q)`
  - re-run the playbook fully: `just install-all`

- [configuring IPv6 (`AAAA`) DNS records](./docs/configuring-ipv6.md#configuring-dns-records-for-ipv6)

> [!WARNING]
> Not all mash-playbook Ansible roles respect the `devture_systemd_docker_base_ipv6_enabled` setting yet.
> Even if you enable this setting, you may still see that some container networks and services aren't IPv6-enabled.
> **Consider sending pull requests** for the playbook roles that do not respect the `devture_systemd_docker_base_ipv6_enabled` setting yet.

## 2025-02-21

### Docker daemon options are no longer adjusted when IPv6 is enabled

We landed initial IPv6 support in the past via a `devture_systemd_docker_base_ipv6_enabled` variable that one had to toggle to `true`.

This variable did **2 different things at once**:

- ensured that container networks were created with IPv6 being enabled
- adjusted the Docker daemon's configuration to set `experimental: true` and `ip6tables: true` (a necessary prerequisite for creating IPv6-enabled networks)

Since Docker 27.0.1's [changes to how it handles IPv6](https://docs.docker.com/engine/release-notes/27/#ipv6), **adjusting the Docker daemon's configuration is no longer necessary**, because:

- `ip6tables` defaults to `true` for everyone
- `ip6tables` is out of the experimental phase, so `experimental` is no longer necessary

In light of this, we're introducing a new variable (`devture_systemd_docker_base_ipv6_daemon_options_changing_enabled`) for controlling if IPv6 should be force-enabled in the Docker daemon's configuration options.
Since most people should be on a modern enough Docker daemon version which doesn't require such changes, this variable defaults to `false`.

This change affects you like this:

- ✅ if you're **not explicitly enabling IPv6** (via `devture_systemd_docker_base_ipv6_enabled` in your configuration): you're unaffected
- ❓ if you're **explicitly enabling IPv6** (via `devture_systemd_docker_base_ipv6_enabled` in your configuration):
  - ✅ .. and you're on a modern enough Docker version (which you most likely are): the playbook will no longer mess with your Docker daemon options. You're unaffected.
  - 🔧 .. and you're on an old Docker version, you **are affected** and need to use the following configuration to restore the old behavior:

    ```yml
    # Force-enable IPv6 by changing the Docker daemon's options.
    # This is necessary for Docker < 27.0.1, but not for newer versions.
    devture_systemd_docker_base_ipv6_daemon_options_changing_enabled: true

    # Request that individual container networks are created with IPv6 enabled.
    devture_systemd_docker_base_ipv6_enabled: true
    ```

## 2024-09-27

### (BC Break) Postgres, Traefik & Woodpecker CI roles have been relocated and variable names need adjustments

Various roles have been relocated from the [devture](https://github.com/devture) organization to the [mother-of-all-self-hosting](https://github.com/mother-of-all-self-hosting) organization.

Along with the relocation, the `devture_` prefix was dropped from their variable names, so you need to adjust your `vars.yml` configuration.

You need to do the following replacements:

- `devture_postgres_` -> `postgres_`
- `devture_traefik_` -> `traefik_`
- `devture_woodpecker_ci_` -> `woodpecker_ci_`

As always, the playbook would let you know about this and point out any variables you may have missed.

## 2024-07-06

### Traefik v3 and HTTP/3 are here now

**TLDR**: Traefik was migrated from v2 to v3. Minor changes were done to the playbook. Mostly everything else worked out of the box. Most people will not have to do any tweaks to their configuration. In addition, [HTTP/3](https://en.wikipedia.org/wiki/HTTP/3) support is now auto-enabled for the `web-secure` (port 443) and `matrix-federation` (port `8448`) entrypoints. If you have a firewall in front of your server and you wish to benefit from `HTTP3`, you will need to open the `443` and `8448` UDP ports in it.

#### Traefik v3

The reverse-proxy that the playbook uses by default (Traefik) has recently been upgraded to v3 (refer to [this blog post](https://traefik.io/blog/announcing-traefik-proxy-v3-rc/) to learn about its new features). Version 3 includes some small breaking configuration changes requiring a [migration](https://doc.traefik.io/traefik/migration/v2-to-v3/).

We have **updated the playbook to Traefik v3** (make sure to run `just roles` / `make roles` to get it).

Most (all) MASH roles should not require any changes and should work with Traefik v3 by default.

**Most people using the playbook should not have to do any changes**.

If you're using the playbook's Traefik instance to reverse-proxy to some other services of your own (not managed by the playbook), you may wish to review their Traefik labels and make sure they're in line with the [Traefik v2 to v3 migration guide](https://doc.traefik.io/traefik/migration/v2-to-v3/).

If you've tweaked any of this playbook's `_path_prefix` variables and made them use a regular expression, you will now need to make additional adjustments. The playbook makes extensive use of `PathPrefix()` matchers in Traefik rules and `PathPrefix` does not support regular expressions anymore. To work around it, you may now need to override a whole `_traefik_rule` variable and switch it from [`PathPrefix` to `PathRegexp`](https://doc.traefik.io/traefik/routing/routers/#path-pathprefix-and-pathregexp).

You **may potentially downgrade to Traefik v2** (if necessary) by adding `traefik_verison: v2.11.4` to your configuration.

#### HTTP/3 is enabled by default

In Traefik v3, [HTTP/3](https://en.wikipedia.org/wiki/HTTP/3) support is no longer considered experimental now.
Due to this, **the playbook auto-enables HTTP3** for the `web-secure` (port 443) entrypoint.

HTTP3 uses the UDP protocol and **the playbook (together with Docker) will make sure that the appropriate port** (`443` over UDP) **is exposed and whitelisted in your server's firewall**. However, **if you have another firewall in front of your server** (as is the case for many cloud providers), **you will need to manually open this UDP port**.

If you do not open the UDP port correctly or there is some other issue, clients (browsers, mostly) will fall-back to [HTTP/2](https://en.wikipedia.org/wiki/HTTP/2) or even [HTTP/1.1](https://en.wikipedia.org/wiki/HTTP).

Still, if HTTP/3 cannot function correctly in your setup, it's best to disable advertising support for it (and misleading clients into trying to use HTTP/3).

To **disable HTTP/3**, you can use the following configuration:

```yml
traefik_config_entrypoint_web_secure_http3_enabled: false
```

## 2023-10-18

### Postgres parameters are automatically tuned now

The playbook has provided some hints about [Tuning PostgreSQL](docs/maintenance-postgres.md#tuning-postgresql) for quite a while now.

From now on, the [Postgres Ansible role](https://github.com/devture/com.devture.ansible.role.postgres) automatically tunes your Postgres configuration with the same [calculation logic](https://github.com/le0pard/pgtune/blob/master/src/features/configuration/configurationSlice.js) that powers <https://pgtune.leopard.in.ua/>.

Our [Tuning PostgreSQL](docs/maintenance-postgres.md#tuning-postgresql) documentation page has details about how you can turn auto-tuning off or adjust the automatically-determined Postgres configuration parameters manually.

## 2023-04-23

### (Backward Compatibility Break) authentik container variables renamed

For the authentik role there have been two containers: `authentic_worker_container` and `authentic_server_container`. To simplify the configuration, it was reduced to one container.

As the role is pretty young and to avoid confusion because of legacy and reverted design decisions all variables containing `authentik_server_container` will now start with authentik_container. This means you will have to rename these variables in your `vars.yml` if you already use authentik. If you use a standard setup this only includes the change below:

- `authentik_server_container_additional_networks_custom` -> `authentik_container_additional_networks_custom`

## 2023-03-29

### (Backward Compatibility Break) Firezone database renamed

If you are running Firezone with the default [Postgres](components/postgres/README.md) integration the playbook automatically created the database with the name `mash-firezone`.
To be consistent with how this playbook names databases for all other services, going forward we've changed the database name to be just `firezone`. You will have to rename you database manually by running the following commands on your server:

1. Stop Firezone: `systemctl stop mash-firezone`
2. Run a Postgres `psql` shell: `/mash/postgres/bin/cli`
3. Execute this query: `ALTER DATABASE "mash-firezone" RENAME TO firezone;` and then quit the shell with `\q`

Then update the playbook (don't forget to run `just roles`), run `just install-all` and you should be good to go!

## 2023-03-26

### (Backward Compatibility Break) PeerTube is no longer wired to Redis automatically

As described in our [Redis](components/redis/README.md) services docs, running a single instance of Redis to be used by multiple services is not a good practice.

For this reason, we're no longer auto-wiring PeerTube to Redis. If you're running other services (which may require Redis in the future) on the same host, it's recommended that you follow the [Creating a Redis instance dedicated to PeerTube](components/peertube/README.md#creating-a-redis-instance-dedicated-to-peertube) documentation.

If you're only running PeerTube on a dedicated server (no other services that may need Redis) or you'd like to stick to what you've used until now (a single shared Redis instance), follow the [Using the shared Redis instance for PeerTube](components/peertube/README.md#using-the-shared-redis-instance-for-peertube) documentation.

## 2023-03-25

### (Backward Compatibility Break) Docker no longer installed by default

The playbook used to install Docker and the Docker SDK for Python by default, unless you turned these off by setting `mash_playbook_docker_installation_enabled` and `devture_docker_sdk_for_python_installation_enabled` (respectively) to `false`.

From now on, both of these variables default to `false`. An empty inventory file will not install these components.

**Most** users will want to enable these, just like they would want to enable [Traefik](components/traefik/README.md) and [Postgres](components/postgres/README.md), so why default them to `false`? The answer is: it's cleaner to have "**everything** is off by default - enable as you wish" and just need to add stuff, as opposed to "**some** things are on, **some** are off - toggle as you wish".

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

## 2023-03-15

### Initial release

This is the initial release of this playbook.

#### Why create such a mega playbook?

We used to maintain separate playbooks for various services ([Matrix](https://github.com/spantaleev/matrix-docker-ansible-deploy), [Nextcloud](https://github.com/spantaleev/nextcloud-docker-ansible-deploy), [Gitea](https://github.com/spantaleev/gitea-docker-ansible-deploy), [Gitlab](https://github.com/spantaleev/gitlab-docker-ansible-deploy), [Vaultwarden](https://github.com/spantaleev/vaultwarden-docker-ansible-deploy), [PeerTube](https://github.com/spantaleev/peertube-docker-ansible-deploy), ..). They re-used Ansible roles (for [Postgres](https://github.com/devture/com.devture.ansible.role.postgres), [Traefik](https://github.com/devture/com.devture.ansible.role.traefik), etc.), but were still hard to maintain due to the large duplication of effort.

Most of these playbooks hosted services which require a Postgres database, a Traefik reverse-proxy, a backup solution, etc. All of them needed to come with documentation, etc. All these things need to be created and kept up-to-date in each and every playbook.

Having to use a dedicated Ansible playbook for each and every piece of software means that you have to juggle many playbooks and make sure they don't conflict with one another when installing services on the same server. All these related playbooks interoperated nicely, but still required at least a bit of manual configuration to achieve this interoperability.

Using specialized Ansible playbooks also means that trying out new software is difficult. Despite the playbooks being similar (which eases the learning curve), each one is still a new git repository you need to clone and maintain, etc.

Furthermore, not all pieces of software are large enough to justify having their own dedicated Ansible playbook. They have no home, so no one uses them.

We're finding the need for a playbook which combines all of this into one, so that:

- you don't need to juggle multiple Ansible playbooks
- you can try out various services easily - a few lines of extra configuration and you're ready to go
- small pieces of software (like [Miniflux](https://miniflux.app/), powered by the [miniflux](https://github.com/mother-of-all-self-hosting/ansible-role-miniflux) Ansible role) which don't have their own playbook can finally find a home
- you can use a single playbook with the quality you know and trust
- shared services (like Postgres) are maintained in one single place
- backups are made easy, because everything lives together (same base data path, same Postgres instance)

Having one large playbook with all services does not necessarily mean you need to host everything on the same server though. Feel free to use as many servers as you see fit. While containers provide some level of isolation, it's still better to not put all your eggs in one basket and create a single point of failure.

All of the aforementioned playbooks have been absorbed into this one. See the [full list of supported services here](docs/supported-services.md). The [Matrix playbook](https://github.com/spantaleev/matrix-docker-ansible-deploy) will remain separate, because it contains a huge number of components and will likely grow even more. It deserves to stand on its own.
