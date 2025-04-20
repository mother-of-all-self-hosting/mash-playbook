# Forgejo

[Forgejo](https://forgejo.org/) is a self-hosted lightweight software forge (Git hosting service, etc.), an alternative to [Gitea](https://gitea.io/) (that this playbook also [supports](gitea.md)).


## Dependencies

This service requires the following other services:

- a [Postgres](postgres.md) database
- a [Traefik](traefik.md) reverse-proxy server


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# forgejo                                                              #
#                                                                      #
########################################################################

forgejo_enabled: true

# Forgejo uses port 22 by default.
# We recommend that you move your regular SSH server to another port,
# and stick to this default.
#
# If you wish to use another port, uncomment the variable below
# and adjust the port as you see fit.
# forgejo_ssh_port: 222

forgejo_hostname: mash.example.com
forgejo_path_prefix: /forgejo

########################################################################
#                                                                      #
# /forgejo                                                             #
#                                                                      #
########################################################################
```

In the example configuration above, we configure the service to be hosted at `https://mash.example.com/forgejo`.

You can remove the `forgejo_path_prefix` variable definition, to make it default to `/`, so that the service is served at `https://mash.example.com/`.


## Usage

After installation, you should be able to access your new Forgejo instance at the configured URL (see above).

Going there, you'll be taken to the initial setup wizard, which will let you assign some paswords and other configuration.


## Recommended other services

You may also wish to look into [Woodpecker CI](woodpecker-ci.md) and [Forgejo Runner](forgejo-runner.md), which can integrate nicely with Forgejo.


## Integration with Woodpecker CI

If you want to integrate Forgejo with [Woodpecker CI](woodpecker-ci.md), and if you plan to serve Woodpecker CI under a subpath on the same host as Forgejo (e.g., Forgejo lives at `https://mash.example.com` and Woodpecker CI lives at `https://mash.example.com/ci`), then you need to configure Forgejo to use the host's external IP when invoking webhooks from Woodpecker CI. You can do it by setting the following variables:

```yaml
forgejo_container_add_host_domain_name: "{{ woodpecker_ci_server_hostname }}"
forgejo_container_add_host_domain_ip_address: "{{ ansible_host }}"

# If ansible_host points to an internal IP address, you may need to allow Forgejo to make requests to it.
# By default, requests are only allowed to external IP addresses for security reasons.
# See: https://forgejo.org/docs/latest/admin/config-cheat-sheet/#webhook-webhook
forgejo_container_additional_environment_variables: |
  FORGEJO__webhook__ALLOWED_HOST_LIST=external,{{ ansible_host }}
```

## Migrating from Gitea

Forgejo is a fork of [Gitea](./gitea.md). Migrating Gitea (versions up to and including v1.22.0) to Forgejo was relatively easy, but [Gitea versions after v1.22.0 do not allow such transparent upgrades anymore](https://forgejo.org/2024-12-gitea-compatibility/).

Nevertheless, upgrades may be possible with some manual work.

Below is a rough guide to help you migrate from Gitea (tested with version v1.23.1) to Forgejo (v10.0.0).

> [!WARNING]
> 2FA does not seem to be working in Forgejo, but [some work](https://codeberg.org/forgejo/forgejo/pulls/7251) has landed in [v10.0.2](https://codeberg.org/forgejo/forgejo/src/commit/c5c0948ae5c96a694cc36945c3d9d5dae439bdd0/release-notes-published/10.0.2.md) which possibly improves things. If this is something you require to get working, do know that it's still an unsolved problem. Details for resetting/disabling 2FA are below.

1. Adjust `vars.yml` to enable the Forgejo service (prepare DNS records if using a dedicated hostname instead of your old Gitea hostname). We do not disable Gitea just yet.

2. Stop Gitea by running this on the server: `systemctl disable --now mash-gitea.service`

3. Dump the Gitea database and adapt for Forgejo

	Run these commands on the server:

	```sh
	mkdir /mash/gitea-to-forgejo-migration
	chown $(id -u mash):$(id -g mash) /mash/gitea-to-forgejo-migration

	docker run \
	--rm \
	--user=$(id -u mash):$(id -g mash) \
	--cap-drop=ALL \
	--env-file=/mash/postgres/env-postgres-psql \
	--mount type=bind,src=/mash/gitea-to-forgejo-migration,dst=/out \
	--network=mash-postgres \
	--entrypoint=/bin/sh \
	docker.io/postgres:17.2-alpine \
	-c 'set -o pipefail && pg_dump -h mash-postgres -d gitea > /out/forgejo.sql'

	sed --in-place 's/OWNER TO gitea/OWNER TO forgejo/g' /mash/gitea-to-forgejo-migration/forgejo.sql
	```

4. Prepare the `forgejo` Postgres database by running the playbook: `just run-tags install-postgres`

5. Import the database dump into the `forgejo` Postgres database

	Run this command on the server:

	```sh
	docker run \
	--rm \
	--user=$(id -u mash):$(id -g mash) \
	--cap-drop=ALL \
	--env-file=/mash/postgres/env-postgres-psql \
	--mount type=bind,src=/mash/gitea-to-forgejo-migration,dst=/out \
	--network=mash-postgres \
	--entrypoint=/bin/sh \
	docker.io/postgres:17.2-alpine \
	-c 'set -o pipefail && psql -h mash-postgres -d forgejo < /out/forgejo.sql'
	```

6. Install Forgejo using the playbook, but do not start it yet: `just run-tags install-forgejo`

7. Sync some files from Gitea by running these commands on the server

	```sh
	rsync -avr /mash/gitea/data/. /mash/forgejo/data/.

	# These files seem to live in a different place now, so we move them around.
	mv /mash/forgejo/data/data/gitea/repo-avatars /mash/forgejo/data/repo-avatars
	rmdir /mash/forgejo/data/data/gitea
	```

8. **For Gitea versions older than v1.22, skip this step**. For newer versions, revert the `forgejo` database to a schema migration version that Forgejo supports

	In this guide, we're using Gitea v1.23.1, the database schema version for which (`312`) is newer than what Forgejo supports (`305`).
	We need to [revert all migrations that are newer than `305`](https://github.com/go-gitea/gitea/tree/v1.23.1/models/migrations/v1_23).

	This may not always be possible or easy. For Gitea v1.23.1, the reverts can be done by running `/mash/postgres/bin/cli`, switching to the `forgejo` database (`\c forgejo`), and running the following queries:

	```sql
	-- Revert 311
	ALTER TABLE issue DROP COLUMN time_estimate;

	-- Revert 310
	ALTER TABLE protected_branch DROP column priority;

	-- Revert 309
	DROP INDEX IF EXISTS "IDX_notification_u_s_uu";
	DROP INDEX IF EXISTS "IDX_notification_user_id";
	DROP INDEX IF EXISTS "IDX_notification_repo_id";
	DROP INDEX IF EXISTS "IDX_notification_status";
	DROP INDEX IF EXISTS "IDX_notification_source";
	DROP INDEX IF EXISTS "IDX_notification_issue_id";
	DROP INDEX IF EXISTS "IDX_notification_commit_id";
	DROP INDEX IF EXISTS "IDX_notification_updated_by";

	-- Revert 308
	DROP INDEX IF EXISTS "IDX_action_r_u_d";
	DROP INDEX IF EXISTS "IDX_action_au_r_c_u_d";
	DROP INDEX IF EXISTS "IDX_action_c_u_d";
	DROP INDEX IF EXISTS "IDX_action_c_u";

	-- Revert 307
	-- Nothing to do

	-- Revert 306
	ALTER TABLE protected_branch DROP COLUMN block_admin_merge_override;

	-- Mark as reverted
	UPDATE version SET version = 305;
	```

9. Start Forgejo by running this on the server: `systemctl start mash-forgejo.service`

10. Complete the Forgejo installation on the web

	Forgejo may show an Installation page at the base URL with various configuration options, most of which prefilled.

	Our experience was that:

	- the "Run as user" field was empty, but required and "read only". Using the browser's inspector was necessary to remove the `readonly` attribute from the field, so we could enter a `git` value in it

	- the "Disable self-registration" checkbox (which is rightfully checked) had to be disabled to prevent an error saying: "You cannot disable user self-registration without creating an administrator account."

	After completing the installation, you should be able to access your new Forgejo instance.

11. Reset 2FA authentication settings for all users

	Forgejo seems to suffer from some issues when handling 2FA login and will return a "500 internal server error" while checking your 2FA code.
	This may be because some secret keys reset during the Gitea -> Forgejo migration, or most likely due to some bug.

	If you're experiencing issues with 2FA, run `/mash/postgres/bin/cli`, switch to the `forgejo` database (`\c forgejo`) and execute the following query:

	```psql
	DELETE FROM two_factor;
	```

	After this, you should be able to log in without being prompted for 2FA.
	Adding 2FA to your account later may be possible, but we also found issues with that:

	> SettingsTwoFactor: Failed to save two factor, pq: invalid byte sequence for encoding "UTF8": ...

	This is probably a bug.

12. If everything is working and you're happy with the migration, consider cleaning up

	You can do this by:

	- removing the Gitea configuration from `vars.yml` and [re-running the playbook](../installing.md) (e.g. `just run-tags setup-gitea`). This will delete the `/mash/gitea` directory
	- dropping the `gitea` database from the Postgres server (execute `/mash/postgres/bin/cli` and run `DROP DATABASE gitea;`)
	- deleting the `/mash/gitea-to-forgejo-migration` temporary directory: `rm -rf /mash/gitea-to-forgejo-migration`
