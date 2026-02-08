<!--
SPDX-FileCopyrightText: 2020 - 2024 MDAD project contributors
SPDX-FileCopyrightText: 2020 - 2025 Slavi Pantaleev
SPDX-FileCopyrightText: 2020 Aaron Raimist
SPDX-FileCopyrightText: 2020 Chris van Dijk
SPDX-FileCopyrightText: 2020 Dominik Zajac
SPDX-FileCopyrightText: 2020 Mickaël Cornière
SPDX-FileCopyrightText: 2022 François Darveau
SPDX-FileCopyrightText: 2022 Julian Foad
SPDX-FileCopyrightText: 2022 Warren Bailey
SPDX-FileCopyrightText: 2023 Antonis Christofides
SPDX-FileCopyrightText: 2023 Felix Stupp
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 MASH project contributors
SPDX-FileCopyrightText: 2023 Niels Bouma
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 Gergely Horváth
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara
SPDX-FileCopyrightText: 2025 IUCCA

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Immich

The playbook can install and configure [Immich](https://github.com/immich-app/immich) for you.

Immich is a self-hosted photo and video management solution, into which you can easily [import your photos from Google Photos](#importing-photos-from-google-photos) (or [a few other places](https://github.com/simulot/immich-go?tab=readme-ov-file#the-upload-command)).

See the project's [documentation](https://immich.app/docs/overview/welcome) to learn what Immich does and why it might be useful to you.

For details about configuring the [Ansible role for Immich](https://github.com/mother-of-all-self-hosting/ansible-role-immich), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-immich/blob/main/docs/configuring-immich.md) online

## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server
- a **custom** [Postgres](postgres.md) database, powered by the [Immich-specific Postgres image](https://github.com/immich-app/base-images/tree/main/postgres) (based on [pgvector](https://github.com/pgvector/pgvector), but also includes additional extensions). See [Configuration overview](#configuration-overview) for details about installation
- a [Valkey](valkey.md) data-store. See [Configuration overview](#configuration-overview) for details about installation
- (optional) [exim-relay](exim-relay.md) for sending emails via this service


## Adjusting the playbook configuration

### Configuration overview

Immich requires a **custom** [Postgres](postgres.md) database instance (powered by the [Immich-specific Postgres image](https://github.com/immich-app/base-images/tree/main/postgres)) and a [Valkey](valkey.md) data-store (which cannot safely be shared with other services running on the same host).

We recommend organizing your Ansible inventory like this:

- **a dedicated inventory host for some Immich dependencies** (e.g. `mash.example.com-immich-deps`), which installs the Immich dependencies that cannot be safely shared with other services, like:

  - the [Valkey](valkey.md) data-store
  - the **custom** (Immich-specific) [Postgres](postgres.md) instance

- **a main inventory host** (e.g. `mash.example.com`) which installs:

  - various other [services](../supported-services.md) that you had already configured

  - the Immich dependencies that can be reused by other services without conflict ([Traefik](traefik.md); optionally [exim-relay](exim-relay.md))

  - Immich itself

With this recommended approach, the only services that are split out (out of the main `mash.example.com` inventory host) are those that **must** be split out (dedicated instances of Immich dependencies).

<details>
<summary>💡 Other configuration layouts are also possible</summary>

For example, you may prepare a dedicated inventory host (e.g. `mash.example.com-immich` or `immich.example.com`) for Immich, which:

- targets the same server (e.g. same IP address as `mash.example.com`)
- reuses the existing [Traefik](traefik.md) installation from `mash.example.com` (as described in the [Traefik managed by you](traefik.md#traefik-managed-by-you) guide)
- installs all Immich dependencies (e.g. [Valkey](valkey.md); **custom** (Immich-specific) [Postgres](postgres.md); optionally [exim-relay](exim-relay.md))
- installs Immich itself

With this alternative approach, all Immich services are split out (into a new `mash.example.com-immich` inventory host), except for the services that **must** be shared (e.g. [Traefik](traefik.md)).

This alternative approach is possible, but is **not described** here. The documentation below assumes you're using the first (recommended) approach.
</details>

### Configuration for the dedicated Immich dependencies inventory host

💡 Make sure you've familiarized yourself with the [Configuration overview](#configuration-overview) section above.

This section is about configuring your dedicated Immich dependencies inventory host (e.g. `mash.example.com-immich-deps`), which will host dedicated instances of Immich dependencies like [Valkey](valkey.md) and the **custom** (Immich-specific) [Postgres](postgres.md) instance.

See the [Running multiple instances of the same service on the same host](../running-multiple-instances.md) documentation for how to configure your dedicated `mash.example.com-immich-deps` inventory host and its variables.

We recommend the following `vars.yml` (e.g. `inventory/host_vars/example.com-immich-deps/vars.yml`) configuration:

```yml
---
########################################################################
#                                                                      #
# Playbook                                                             #
#                                                                      #
########################################################################

# Put a strong secret below, generated with `pwgen -s 64 1` or in another way
mash_playbook_generic_secret_key: ""

# Override service names and directory path prefixes
mash_playbook_service_identifier_prefix: 'mash-immich-'
mash_playbook_service_base_directory_name_prefix: 'immich-'

########################################################################
#                                                                      #
# /Playbook                                                            #
#                                                                      #
########################################################################


########################################################################
#                                                                      #
# Various other overrides                                              #
#                                                                      #
########################################################################

# See: docs/configuring-ipv6.md
devture_systemd_docker_base_ipv6_enabled: true

########################################################################
#                                                                      #
# /Various other overrides                                             #
#                                                                      #
########################################################################


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


########################################################################
#                                                                      #
# postgres                                                             #
#                                                                      #
########################################################################

postgres_enabled: true

# Put a strong secret below, generated with `pwgen -s 64 1` or in another way
postgres_connection_password: ""

postgres_container_image_registry_prefix_upstream_default: ghcr.io/
postgres_container_image_name: immich-app/postgres
postgres_container_image_suffix: ""

# We pin Postgres to a specific major version or versions.
# The version/versions defined here have corresponding `postgres_container_image_vXX_version` overrides below,
# so that the Postgres role would install Immich/Postgres (see https://github.com/immich-app/base-images), instead of vanilla Postgres.
#
# When a new Immich/Postgres version becomes available and the same major version is supported by the Postgres role, you can:
# - override the variable (e.g. `postgres_container_image_vXX_version`) for it by defining it below and pointing to an Immich/Postgres container image
# - adjust `postgres_allowed_versions_custom` to allow upgrading to the new major version
# - run `--tags=upgrade-postgres`
# - clean up:
#   - remove the variable override for the old Postgres version (e.g. `postgres_container_image_vXX_version`)
#   -adjust `postgres_allowed_versions_custom` to only contain the new Postgres version
postgres_allowed_versions_custom: [18]

postgres_container_image_v18_version: 18-vectorchord0.5.3-pgvector0.8.1

postgres_initdb_args_list_custom:
  - "--data-checksums"

# The Immich Postgres custom entrypoint copies `/var/postgresql-conf-tpl/postgresql.${DB_STORAGE_TYPE,,}.conf`
# into `/etc/postgresql/postgresql.conf`, so we need to run as a privileged-enough user
# that can write to the filesystem.
# See: https://github.com/immich-app/base-images/blob/489692aaafce6c4d005537809cd48b82f206a9bb/postgres/immich-docker-entrypoint.sh#L7-L17
#
# Still, we wish for the files to be owned by a UID/GID that corresponds to `postgres:postgres` in the container.
postgres_uid: 999
postgres_gid: 999

postgres_container_uid: 0
postgres_container_gid: 0
postgres_container_read_only_enabled: false
postgres_container_cap_drop_all_enabled: false

# We use an arbitrary user/group in `postgres_uid` (that matches the `postgres` user that exists in the container image's `/etc/passwd` file).
# As such, we don't wish to mount the host's `/etc/passwd` file,
# which is unlikely to have a matching entry.
postgres_container_mount_etc_passwd_enabled: false

# Launch Postgres like Immich Postgres intends (passing in a custom config file).
# See: https://github.com/immich-app/base-images/blob/489692aaafce6c4d005537809cd48b82f206a9bb/postgres/Dockerfile#L42
postgres_postgres_process_extra_arguments_custom:
  - "-c"
  - "config_file=/etc/postgresql/postgresql.conf"

postgres_managed_databases_additional:
  - name: "{{ immich_database_name }}"
    username: "{{ immich_database_username }}"
    password: "{{ immich_database_password }}"
    additional_sql_queries: |-
      {{
        ["\c " + immich_database_name]
        +
        immich_database_preparation_sql_queries
      }}

########################################################################
#                                                                      #
# /postgres                                                            #
#                                                                      #
########################################################################


########################################################################
#                                                                      #
# immich                                                               #
#                                                                      #
########################################################################

immich_database_hostname: "{{ postgres_connection_hostname }}"
immich_database_port: "{{ postgres_connection_port }}"

# Put a strong secret below, generated with `pwgen -s 64 1` or in another way
immich_database_password: ""
immich_database_sslmode: disable

########################################################################
#                                                                      #
# /immich                                                              #
#                                                                      #
########################################################################
```

💡 Some Immich variables (`immich_database_*`) are defined (overwritten) above, but Immich is intentionally not enabled (`immich_enabled: false`), because we don't wish to install Immich on this host. Rather, we'd only like to install its dependencies.

When done adjusting the `vars.yml` file for your dedicated Immich host (e.g. `mash.example.com-immich-deps`), re-run the [installation](../installing.md) process for that host (e.g. `just install-all -l example.com-immich-deps`).

Installation will prepare the dedicated Immich dependencies (with their files under `/mash/immich-*` directories on the host) and you can proceed to the next step: [Configuration for your main inventory host](#configuration-for-your-main-inventory-host).

### Configuration for your main inventory host

💡 Make sure you've familiarized yourself with the [Configuration overview](#configuration-overview) section above.

This section is about configuring your main inventory host (e.g. `mash.example.com`), which will host Immich itself, various other [services](../supported-services.md) that you're already hosting there, as well as some Immich dependencies which can safely be shared between services (e.g. [exim-relay](exim-relay.md) and [Traefik](traefik.md)).

#### Adjusting Traefik configuration for long-running uploads

We recommend **adjusting your Traefik configuration** to allow long-running uploads (which may be necessary for uploading large video files over slow connections to Immich).

```yml
########################################################################
#                                                                      #
# traefik                                                              #
#                                                                      #
########################################################################

# Your regular Traefik configuration here.

# Increase some timeouts to allow for longer image uploads for Immich.
traefik_config_entrypoint_web_transport_respondingTimeouts_readTimeout: 1800s
traefik_config_entrypoint_web_transport_respondingTimeouts_writeTimeout: 1800s
traefik_config_entrypoint_web_transport_respondingTimeouts_idleTimeout: 1800s

########################################################################
#                                                                      #
# /traefik                                                             #
#                                                                      #
########################################################################
```

#### Optional: enabling exim-relay

If you'll be configuring Immich to send email notifications, you may wish to route all emails through [exim-relay](exim-relay.md). Exim-relay can be pointed to another SMTP server and various [services](../supported-services.md) can re-use it.

Follow our [exim-relay documentation](exim-relay.md) documentation to set it up.

> [!WARNING]
> Installing exim-relay auto-wires Immich for contacting it. To actually enable email-notifications (and make them go through exim-relay), you will need to [adjust notification settings](#adjusting-notification-settings) from Immich's Administration UI after Immich is installed.


#### Configuring Immich

Finally, all dependencies are in place and you can adjust your main inventory host's `vars.yml` file in a way that installs Immich.

The base configuration you may wish to add to `vars.yml` is like this:

```yml
########################################################################
#                                                                      #
# immich                                                               #
#                                                                      #
########################################################################

immich_enabled: true

immich_hostname: immich.mash.example.com

immich_server_environment_variable_tz: Europe/Sofia

# This points to the dedicated (for Immich) Valkey installation,
# configured in the other inventory host (e.g. `mash.example.com-immich-deps`).
immich_redis_hostname: mash-immich-valkey

# This wires the Immich/Server systemd service to:
# - the dedicated (for Immich) Valkey installation (see `mash.example.com-immich-deps`)
# - the dedicated (for Immich) custom PostgreSQL installation (see `mash.example.com-immich-deps`)
immich_server_systemd_required_services_list_custom:
  - "mash-immich-valkey.service"
  - "mash-immich-postgres.service"

# This wires the Immich/Server container to:
# - the network of the dedicated (for Immich) Valkey installation (see `mash.example.com-immich-deps`)
# - the network of the dedicated (for Immich) custom PostgreSQL installation (see `mash.example.com-immich-deps`)
immich_server_container_additional_networks_custom:
  - "mash-immich-valkey"
  - "mash-immich-postgres"

# This points to the dedicated (for Immich) custom PostgreSQL installation,
# configured in the other inventory host (e.g. `mash.example.com-immich-deps`).
#
# The password used here MUST match the one used in the
# `mash.example.com-immich-deps` inventory host's `vars.yml` file.
immich_database_hostname: mash-immich-postgres
immich_database_port: 5432
immich_database_password: ""
immich_database_sslmode: disable

########################################################################
#                                                                      #
# /immich                                                              #
#                                                                      #
########################################################################
```

💡 Before [Installing](#installation), **consider doing some additional Immich configuration tweaking via Ansible**, as described below.


##### Disabling the Machine Learning component

The [Immich role for Ansible](https://github.com/mother-of-all-self-hosting/ansible-role-immich) used by this playbook, supports selectively enabling/disabling of its components (`server` and `machine-learning`).

**By default, both components are enabled**, which should be what most users want.

If you don't wish for **local** machine-learning-based processing to be done on your photos (perhaps you're on very weak hardware), you can disable the `machine-learning` component by using this **additional** configuration in your `vars.yml` file:

```yml
immich_machine_learning_enabled: false
```

> [!WARNING]
> Disabling the Machine Learning component this way (via Ansible) will prevent it from being installed. However, Immich's `server` component will still auto-configure itself with Machine Learning enabled and will try to reach a Machine Learning component that isn't there. You may wish to disable Machine Learning from Immich's Administration settings after installation. See the [Machine Learning settings](#adjusting-machine-learning-settings) section below for more details.

##### Enabling Hardware Acceleration for Machine Learning

By default, Machine Learning is done on the CPU.

You can speed up Machine Learning significantly (**even if you only have an integrated GPU**) if you enable hardware acceleration for Machine Learning.

Refer to Immich's [Hardware Acceleration for Machine Learning](https://immich.app/docs/features/ml-hardware-acceleration) documentation for prerequisites, then tune the Machine Learning Ansible variables.

The [Immich role for Ansible](https://github.com/mother-of-all-self-hosting/ansible-role-immich) provides a helpful preset variable (`immich_machine_learning_hardware_acceleration`) that you can use to enable hardware acceleration for Machine Learning.

Example **additional** configuration for your `vars.yml` file:

```yml
# Valid values: armnn, cuda, cpu, openvino, openvino-wsl, rknn, rocm
immich_machine_learning_hardware_acceleration: openvino
```

💡 For Intel-based CPUs with an integrated GPU, set this to `openvino`.

> [!WARNING]
> Hardware-acceleration-enabled machine-learning images appear to be missing for some platforms (like `rocm`), so you may not have much luck with this setting. See: [Missing hardware-accelerated container image tags for machine-learning for some platforms #24533](https://github.com/immich-app/immich/issues/24533).

💡 Defaults are generally fine, but you may also wish to tweak [Machine Learning settings](#adjusting-machine-learning-settings) after installation.

##### Enabling Hardware Acceleration for video transcoding

By default, video transcoding (via [ffmpeg](https://ffmpeg.org/)) is done on the CPU.

You can speed up video transcoding significantly (**even if you only have an integrated GPU**) if you enable hardware acceleration for video transcoding.

Refer to Immich's [Hardware Transcoding](https://immich.app/docs/features/hardware-transcoding) documentation for prerequisites, then tune the transcoding Ansible variables.

The [Immich role for Ansible](https://github.com/mother-of-all-self-hosting/ansible-role-immich) provides a helpful preset variable (`immich_server_transcoding_hardware_acceleration`) that you can use to enable hardware acceleration for video transcoding.

Example **additional** configuration for your `vars.yml` file:

```yml
# Valid values: cpu, nvenc, quicksync, rkmpp, vaapi, vaapi-wsl
immich_server_transcoding_hardware_acceleration: quicksync
```

💡 For Intel-based CPUs with an integrated GPU, set this to `quicksync`.

> [!WARNING]
> Enabling hardware acceleration for transcoding here (in the Ansible configuration) is not enough to make Immich actually use it. After Immich installation, make sure to enable hardware acceleration for transcoding from the [Adjusting Video Transcoding settings](#adjusting-video-transcoding-settings) section.

##### URL

In the example configuration above, we configure the service to be hosted at `https://immich.mash.example.com/`.

Immich [does not currently support being hosted at a subpath](https://github.com/immich-app/immich/issues/14530) (e.g. `/immich`).

##### Preventing the setup page from appearing

When you first access Immich, a welcome/setup page is shown which allows anyone to sign up and register as an admin.

For **first-time installations**, you should leave this enabled (which is the default), so that you can create your admin user.

However, **after you've completed the initial setup**, you may wish to prevent the setup page from ever appearing again. This is useful as a security measure — if for whatever reason your database is reset, anyone who accesses your Immich instance would be able to register as an admin.

To prevent the setup page from appearing, add the following **additional** configuration to your `vars.yml` file:

```yml
immich_server_environment_variable_immich_allow_setup: false
```

##### Other configuration

Unfortunately, most of Immich's configuration cannot be managed via Ansible and needs to be done from the UI, after it's installed. After installation, check the [Usage](#usage) section below for some recommendations for things you may wish to change.


## Installation

As described in [Configuration overview](#configuration-overview), we're dealing with 2 inventory hosts (`mash.example.com-immich-deps` and `mash.example.com`).

You need to run the [installing](../installing.md) command for the supplementary host (`mash.example.com-immich-deps`) first, before running it for the main host (`mash.example.com`).


## Usage

After installation, you can go to the Immich URL, as defined in `immich_hostname`.

Follow the sections below for **important post-installation steps**.

### Setup wizard

When accessing your Immich instance for the first time, you will be greeted by a **setup wizard**.

You can **create your first (admin) user** and **configure some settings via this wizard**.

We recommend enabling the [Storage Templating](https://immich.app/docs/administration/storage-template/) feature from this wizard, and choosing (from the dropdown) a storage layout that suits you.

💡 After completing the setup wizard, consider [Preventing the setup page from appearing](#preventing-the-setup-page-from-appearing) by adjusting your configuration and re-running the installation (e.g. `just install-service immich`). This prevents the setup page from being shown again if your database is ever reset.

### Administration settings

After you've installed Immich, **we recommend doing some settings**.

> [!WARNING]
> Even if you have enabled hardware acceleration or email-integration (via exim-relay) in your Ansible configuration, you **must** do settings from the Immich UI (after installation), or these features won't work.

Go to the **Administration** page (a homepage URL of `/admin/users`) and follow the guides below.

#### Change the Storage label for your first user (admin)

By default, the first user you create has a storage label of `admin`.

It's probably better if you assign another username to it, like `john.doe`.

On the **Administration settings** / **Users** page (a URL of `/admin/users`):

1. Click the **View User** button (an eye icon) for your user.
2. Use the **Edit user** button
3. Adjust the **Storage label** field and click **Confirm**

💡 If you had already uploaded some photos before doing this change, you will need to re-run the **Storage Template Migration** job from the **Jobs** menu to apply the new storage label to your existing photos.

#### Disabling database dumps

By default, Immich configures nightly (at 2am) [automatic database dumps](https://immich.app/docs/administration/backup-and-restore/#automatic-database-dumps).

**We recommend disabling this**, because:

- MASH passes non-superuser Postgres database credentials to Immich, so **the backup process fails anyway**

  The [Without superuser permission](https://immich.app/docs/administration/postgres-standalone#without-superuser-permission) section of the [Pre-existing Postgres](https://immich.app/docs/administration/postgres-standalone) documentation for Immich says:

  > Currently, automated backups require superuser permission due to the usage of `pg_dumpall`.

  This is correct. Immich's attempts to create a database dump result in the following error log messages:

  ```
  ERROR [Microservices:Backup failed with code 1] Database Backup Failure
  ERROR [Microservices:BackupService] Gzip exited with code 0 but pgdump exited with 1
  ERROR [Microservices:{}] Unable to run job handler (DatabaseBackup): Backup failed with code 1
  ```

  To disable database dumps, go to the **Administration** settings / **Settings** (a URL of `/admin/system-settings`) / **Database Dump Settings** and **disable** the **Enable database dumps** option.

- we recommend that you **build your own comprehensive backup strategy**

  💡 When building scripts for backing up your server, you can use the `/mash/immich-postgres/bin/dump-all <path-to-output-directory>` script to dump the [Postgres](postgres.md) database. Invoking it will place a `latest-dump.sql.zst` file in the specified directory.

#### Adjusting Machine Learning settings

Machine Learning is configured from the **Administration** settings / **Settings** (a URL of `/admin/system-settings`) / **Machine Learning Settings**.

Regardless of whether you've [disabled the Machine Learning component](#disabling-the-machine-learning-component) (via Ansible), Immich auto-enables it by default and tries to do machine learning. By default, the Machine Learning URL is configured as `http://immich-machine-learning:3003`.

When the Machine Learning component is enabled (which it is by default), the Immich Ansible role automatically sets up a container alias, so that `immich-machine-learning` leads to the Machine Learning container (whatever its identifier happens to be; e.g. `mash-immich-machine-learning`).

You may host the Machine Learning component on a different (more powerful or better-GPU-accelerated) host. If so, you'll need to adjust the Machine Learning URL. Such a setup is not described in this documentation.

#### Adjusting Video Transcoding settings

Video Transcoding is configured from the **Administration** settings / **Settings** (a URL of `/admin/system-settings`) / **Video Transcoding Settings**.

You probably wish to adjust a few different things here.

1. **Transcode policy**, to specify:

  - **Accepted video codecs** = **only `H.264`**

  If your Immich installation will serve various devices (new and old) and various browsers (Chromium-based and Firefox), you'd better pick a format that plays well on all.

  Right now, this probably eliminates all options other than `H.264`.

  💡 If you're hoping to use Hardware Acceleration for transcoding, your GPU (even if it's an integrated one) better have support for the selected codec (or codecs).

  - **Accepted audio codecs** = **only `AAC`**

  - **Accepted containers** = nothing selected (which means "only MP4")

2. **Encoding options**, to specify:

  - **Video codec** = `h264`

  - **Audio codec** = `aac`

  - **Target resolution** = `720p` (though, adjust as necessary; `original` may be a good option, but underpowered devices may struggle with it)

  - **Preset** = `fast` (perhaps better storage and quality than the default `ultrafast`, but adjust as necessary)

3. **Hardware Acceleration**

  - **Acceleration API** = choose the one that matches your hardware and configuration preset in [Enabling Hardware Acceleration for video transcoding](#enabling-hardware-acceleration-for-video-transcoding).

  - **Hardware decoding** = enabled (but consider disabling if it doesn't work well for you)

#### Adjusting Notification settings

If you have enabled the [exim-relay](exim-relay.md) service for the same MASH inventory host, it would be wired in such a way, so that Immich could reach it.

However, **Immich doesn't enable email notifications and won't use exim-relay by default**.

You need to go to **Administration** settings / **Settings** (a URL of `/admin/system-settings`) / **Notification Settings** / **Email** and then adjust these settings:

- **Enable email notifications** = enabled

- **Host**: point to your SMTP host or to `exim-relay`'s container name (e.g. `mash-exim-relay`) if using [exim-relay](exim-relay.md)

- **Port**: point to your SMTP port or to `exim-relay`'s container port (e.g. `8025`) if using [exim-relay](exim-relay.md)

- **Username**: leave empty if using [exim-relay](exim-relay.md)

- **Password**: leave empty if using [exim-relay](exim-relay.md)

- **From Address**: e.g. `Immich Photo Server <noreply@example.com>`. Adjust as necessary.

#### Adjusting the server's public URL

By default, Immich does not know its own public URL. Without knowing its public URL:

- ✅ when generating share links, the URL would be auto-generated correctly based on the current URL you're accessing from

- 🚫 when inviting people to albums, Immich would send an `https://my.immich.app/*` URL, which is incorrect

To fix this, go to **Administration** settings / **Settings** (a URL of `/admin/system-settings`) / **Server Settings** and adjust the **External domain** field, setting it to something like: `https://immich.example.com`.

### Creating additional users

Go to **Administration** settings / **Users** (a URL of `/admin/users`) and click **Create User**.

After creation, consider adjusting the **Storage label** for the new user to set it to a user-friendly username (e.g. `john.doe`). The process is described in the [Change the Storage label for your first user (admin)](#change-the-storage-label-for-your-first-user-admin) section - follow the same steps to do it for the new user.

After creation, you can edit the user to mark them as an administrator.

### Importing photos from elsewhere

Importing photos from [a few different places](https://github.com/simulot/immich-go?tab=readme-ov-file#the-upload-command) could be done with [Immich-Go](https://github.com/simulot/immich-go).

You may also import manually by:

- uploading files via a browser (or the Immich API)

- setting up some directory where you'll drop the files and configure Immich to scan & import them. This may involve mounting an additional volume to the Immich/Server container (you may use the `immich_server_container_additional_volumes_custom` variable for that), unless you reuse the existing data path (`/mash/immich/server/data`) which is already mounted to `/data` in the container.

#### Importing photos from Google Photos

Follow [Immich-Go](https://github.com/simulot/immich-go)'s [Google Photos Best Practices](https://github.com/simulot/immich-go?tab=readme-ov-file#google-photos-best-practices) section for the full details.

You'll need to create an API key in your Immich account and then run a command similar to this:

```sh
./immich-go upload from-google-photos \
--api-key=API_KEY_HERE \
--server=https://immich.example.com \
/path/to/google-takeout/*.zip
```

💡 If the user you're importing to is not an admin, also consider passing `--admin-api-key=ADMIN_API_KEY_HERE` or you'll get an error saying that an underprivileged API key cannot pause background jobs.

💡 Various import flags exist (see `./immich-go upload from-google-photos --help`), but the default invocation should generally yield a good result.

💡 While the import is running and Immich is doing post-processing (a process which could take hours), Immich will likely show a "broken image" placeholder for many of the imported photos. You can observe the post-processing progress in **Administration** settings / **Jobs** (a URL of `/admin/jobs-status`).

## Troubleshooting

### Check the service's logs

You can find the logs in [systemd-journald](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html) by logging in to the server with SSH and running `journalctl -fu mash-immich`.

### Fix the password authentication error on Postgres

If `immich_database_password` is not specified on your `vars.yml` file, you'll get the error related to the password authentication on Postgres as below:

```txt
PostgresError: password authentication failed for user "immich"
```

If you have copied and reuse the example configuration described above, make sure to set the same password to the variable on both of your `vars.yml` files (i.e. main one and the other for your dedicated Immich dependencies inventory host).

## Related services

- [Immich Kiosk](immich-kiosk.md) — Highly configurable slideshow for displaying Immich pictures and videos on browsers and devices
