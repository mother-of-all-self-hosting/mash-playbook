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
SPDX-FileCopyrightText: 2023 - 2024 MASH project contributors
SPDX-FileCopyrightText: 2023 Antonis Christofides
SPDX-FileCopyrightText: 2023 Felix Stupp
SPDX-FileCopyrightText: 2023 Gergely Horváth
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara
SPDX-FileCopyrightText: 2024 Philipp Homann

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up Nextcloud

This is an [Ansible](https://www.ansible.com/) role which installs [Nextcloud](https://nextcloud.com) to run as a [Docker](https://www.docker.com/) container wrapped in a systemd service.

Nextcloud is one of the most popular self-hosted collaboration solutions.

See the project's [documentation](https://docs.nextcloud.com) to learn what Nextcloud does and why it might be useful to you.

## Prerequisites

To run a Nextcloud instance it is necessary to prepare a database. You can use a [MySQL](https://www.mysql.com/) compatible database server, [Postgres](https://www.postgresql.org/), or [SQLite](https://www.sqlite.org/). By default it is configured to use Postgres.

If you are looking for Ansible roles for a MySQL compatible server or Postgres, you can check out [ansible-role-mariadb](https://github.com/mother-of-all-self-hosting/ansible-role-mariadb) and [ansible-role-postgres](https://github.com/mother-of-all-self-hosting/ansible-role-postgres), both of which are maintained by the [Mother-of-All-Self-Hosting (MASH)](https://github.com/mother-of-all-self-hosting) team.

>[!NOTE]
> Nextcloud recommends MySQL / MariaDB on [this page](https://docs.nextcloud.com/server/latest/admin_manual/configuration_database/linux_database_configuration.html) of the documentation. Note that not all versions of them are recommended. See [this page](https://docs.nextcloud.com/server/latest/admin_manual/installation/system_requirements.html#server) for system requirements.

## Adjusting the playbook configuration

To enable Nextcloud with this role, add the following configuration to your `vars.yml` file.

**Note**: the path should be something like `inventory/host_vars/mash.example.com/vars.yml` if you use the [MASH Ansible playbook](https://github.com/mother-of-all-self-hosting/mash-playbook).

```yaml
########################################################################
#                                                                      #
# nextcloud                                                            #
#                                                                      #
########################################################################

nextcloud_enabled: true

########################################################################
#                                                                      #
# /nextcloud                                                           #
#                                                                      #
########################################################################
```

### Set the hostname

To enable Nextcloud you need to set the hostname as well. To do so, add the following configuration to your `vars.yml` file. Make sure to replace `example.com` with your own value.

```yaml
nextcloud_hostname: "example.com"
```

After adjusting the hostname, make sure to adjust your DNS records to point the domain to your server.

>[!NOTE]
> Changing the hostname after the first installation is currently not supported by Nextcloud. See [this page](https://docs.nextcloud.com/server/latest/admin_manual/configuration_server/domain_change.html) on the documentation as well.

### Configure database

By default Nextcloud is configured to use Postgres, but you can choose other databases such as MySQL (MariaDB) and SQLite.

To use MariaDB, add the following configuration to your `vars.yml` file:

```yaml
nextcloud_database_type: mysql
```

Set `mysql` for MySQL compatible database or `sqlite` for SQLite, respectively.

For other settings, check variables such as `nextcloud_database_mysql_*` and `nextcloud_database_*` on [`defaults/main.yml`](../defaults/main.yml).

>[!NOTE]
> It is possible to convert a SQLite database to a MySQL, MariaDB or PostgreSQL database with the Nextcloud command line tool. See [this page](docs.nextcloud.com/server/latest/admin_manual/configuration_database/db_conversion.html) on the documentation for details.

### Editing default configuration parameters (optional)

Some configuration parameters are specified with variables starting with `nextcloud_config_parameter_default_*`. See below for details.

#### Configure the default language

You can set the default language on your Nextcloud instance with ISO_639-1 language codes as below:

```yml
nextcloud_config_parameter_default_language: de
```

By default it is set to English.

#### Configure the default phone region

You can set the default region for phone numbers on your Nextcloud instance with ISO 3166-1 country codes as below:

```yml
nextcloud_config_parameter_default_phone_region: GB
```

It is not set by default.

#### Configure the default timezone

It is also possible to set the default timezone with IANA identifiers such as `Europe/Berlin` as below:

```yml
nextcloud_config_parameter_default_timezone: Europe/Berlin
```

By default it is set to UTC.

>[!NOTE]
> Setting a proper timezone is important for some instances such as using Nextcloud applications like [Calendar](https://apps.nextcloud.com/apps/calendar) and [Forms](https://apps.nextcloud.com/apps/forms) where it is possible to set an expiration date to a form.

#### Defining configuration parameters by yourself

Configuration parameters (and their values) can be overridden by defining `nextcloud_config_parameters_default` by yourself. Your custom ones can be added to `nextcloud_config_parameters_custom`.

Refer to [this page](https://docs.nextcloud.com/server/latest/admin_manual/configuration_server/config_sample_php_parameters.html) of the Nextcloud documentation for details.

### Configure memory caching (optional)

Nextcloud recommends to set up memory caching for improving performance and preventing file locking problems. You can use [APCu](https://pecl.php.net/package/APCu), [Memcached](https://www.memcached.org/), and [Redis](https://redis.io/).

To enable Redis for Nextcloud, add the following configuration to your `vars.yml` file, so that the Nextcloud instance will connect to the server:

```yaml
nextcloud_redis_hostname: YOUR_REDIS_SERVER_HOSTNAME_HERE
nextcloud_redis_password: YOUR_REDIS_SERVER_PASSWORD_HERE
nextcloud_redis_port: 6379
```

Make sure to replace `YOUR_REDIS_SERVER_HOSTNAME_HERE` and `YOUR_REDIS_SERVER_PASSWORD_HERE` with your own values.

See below for details:

- <https://docs.nextcloud.com/server/latest/admin_manual/configuration_server/caching_configuration.html>
- <https://docs.nextcloud.com/server/latest/admin_manual/configuration_server/config_sample_php_parameters.html#memory-caching-backend-configuration>

If you are looking for an Ansible role for Redis, you can check out [ansible-role-redis](https://github.com/mother-of-all-self-hosting/ansible-role-redis) maintained by the [Mother-of-All-Self-Hosting (MASH)](https://github.com/mother-of-all-self-hosting) team. The roles for [KeyDB](https://keydb.dev/) ([ansible-role-keydb](https://github.com/mother-of-all-self-hosting/ansible-role-keydb)) and [Valkey](https://valkey.io/) ([ansible-role-valkey](https://github.com/mother-of-all-self-hosting/ansible-role-valkey)) are available as well.

### Configure the mailer (optional)

You can configure a SMTP mailer by adding the following configuration to your `vars.yml` file as below (adapt to your needs):

```yaml
# Set the hostname of the SMTP server
nextcloud_environment_variables_smtp_host: ""

# Set the port number of the SMTP server
nextcloud_environment_variables_smtp_port: 587

# Specify the localpart of the sender (localpart@domain)
nextcloud_environment_variables_mail_from_address: ""

# Specify the domain for the external SMTP server if it is different from the domain where Nextcloud is installed
nextcloud_environment_variables_mail_domain: ""

# Set the username for the SMTP server
nextcloud_environment_variables_smtp_name: ""

# Set the password for the SMTP server
nextcloud_environment_variables_smtp_password: ""

# Set `ssl` or `tls` if one of them is used for communication with the SMTP server
nextcloud_environment_variables_smtp_secure: ""

# Specify the method used for authentication. Set PLAIN if no authentication is required.
nextcloud_environment_variables_smtp_authtype: LOGIN
```

>[!NOTE]
> Without setting an authentication method such as DKIM, SPF, and DMARC for your hostname, emails are most likely to be quarantined as spam at recipient's mail servers. If you have set up a mail server with the [MASH project's exim-relay Ansible role](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay), you can enable DKIM signing with it. Refer [its documentation](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay/blob/main/docs/configuring-exim-relay.md#enable-dkim-support-optional) for details.

### Configure object storages as primary storage (optional)

>[!WARNING]
> Configuring an object storage on an existing Nextcloud instance as the primary one will make **all existing files on the instance inaccessible**!
>
> Before proceeding, please have a look at [this page](https://docs.nextcloud.com/server/latest/admin_manual/configuration_files/primary_storage.html) to know differences between the primary storage and an external storage. Also make sure to understand important implications of using the primary object storage, such as the one that *your files on the primary storage will ONLY be able to be retrieved through the Nextcloud instance, making it necessary to take it into consideration when planning a data backup strategy.*

It is possible to configure object storages such as OpenStack Swift or Amazon S3 or any compatible S3-implementation as the primary storage.

Since required settings are different among implementations, the role does not set default configurations for them. You can check [this section](https://github.com/docker-library/docs/blob/master/nextcloud/README.md#auto-configuration-via-environment-variables) to see what needs configuring for your storage provider. Consult the documentation by the provider as well.

To use a S3 compatible object storage as the primary storage, check `OBJECTSTORE_S3_*` environment variables. For OpenStack Swift, you can use `OBJECTSTORE_SWIFT_*` environment variables.

For example, you can have the Nextcloud instance use the bucket named `example` on Storj (a S3 compatible storage) as the primary storage by adding the following configuration to your `vars.yml` file:

```yaml
nextcloud_environment_variables_additional_variables: |
  OBJECTSTORE_S3_BUCKET=example
  OBJECTSTORE_S3_HOST=gateway.storjshare.io
  OBJECTSTORE_S3_KEY=YOUR_ACCESS_KEY_HERE
  OBJECTSTORE_S3_SECRET=YOUR_SECRET_KEY_HERE
  OBJECTSTORE_S3_USEPATH_STYLE=true
```

### Enable Samba (optional)

To enable [Samba](https://www.samba.org/) external Windows fileshares using [smbclient](https://www.samba.org/samba/docs/current/man-html/smbclient.1.html), add the following configuration to your `vars.yml` file:

```yaml
nextcloud_container_image_customizations_samba_enabled: true
```

With this configuration a customized image with the smbclient package installed will be built.

### Using an APT proxy for custom image builds (optional)

Custom image builds can be sped up considerably by serving Debian packages from an [apt-cacher-ng](https://wiki.debian.org/AptCacherNg) instance that lives on the docker-host. Configure the proxy with the variable below (use the docker-host’s LAN IP, not `127.0.0.1`, because the build container runs in its own namespace):

```yaml
mash_apt_proxy_url: "http://{{ ansible_default_ipv4.address }}:3142"
```

Leave it empty to disable proxy usage. The Dockerfile writes the proxy configuration, runs `apt-get update`, and if the proxy is unreachable (or only returns partial results) it removes the proxy file and retries without it before installing the preview/OCR stack. BuildKit cache mounts keep subsequent builds fast even without the proxy.

To host apt-cacher-ng on the docker-host you can run a lightweight compose stack (see the optional `mash_apt_proxy` role). The resulting compose file looks like:

```yaml
services:
  aptcacher:
    image: sameersbn/apt-cacher-ng
    restart: unless-stopped
    network_mode: host
    volumes:
      - /srv/apt-cacher-ng:/var/cache/apt-cacher-ng
```

Enable it by setting `mash_apt_proxy_enabled: true` along with the defaults the role exposes (`mash_apt_proxy_bind_address`, `mash_apt_proxy_port`, etc.).

You can verify the proxy is receiving traffic by forcing a recount on the status page:

```sh
curl -s "http://<host-ip>:3142/acng-report.html?doCount=Count+Data" | sed -n '1,160p'
```

When testing with a plain Debian container you may see the `_apt` sandbox warning if you download as root. To avoid it, run downloads as the `_apt` user:

```sh
docker run --rm --network=host debian:trixie bash -lc \
  'cd /tmp && su -s /bin/sh -c "apt-get -o Acquire::http::Proxy=http://<host-ip>:3142 update && \\
    apt-get -y -o Acquire::http::Proxy=http://<host-ip>:3142 download curl" _apt'
```

An example host vars snippet combining the proxy, preview tooling, and PHP overrides looks like this:

```yaml
mash_apt_proxy_url: "http://10.1.154.10:3142"

nextcloud_enabled: true
nextcloud_hostname: "nextcloud.{{ domain }}"
nextcloud_path_prefix: /

nextcloud_app_collabora_wopi_url: "{{ collabora_online_url }}"
nextcloud_app_collabora_wopi_allowlist: "127.0.0.1/8, 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16"

nextcloud_environment_variables_additional_variables: |
  PHP_MEMORY_LIMIT=1024M
  PHP_UPLOAD_LIMIT=2048M
  PHP_MAX_EXECUTION_TIME=3600

nextcloud_container_image_customizations_packages_to_install_custom:
  - ca-certificates
  - curl
  - imagemagick
  - libmagickcore-7.q16-10-extra
  - ghostscript
  - poppler-utils
  - ffmpeg
  - ffmpegthumbnailer
  - libheif1
  - librsvg2-bin
  - tesseract-ocr
  - tesseract-ocr-eng
  - tesseract-ocr-dan
  - libreoffice
  - fonts-dejavu
  - fonts-liberation
  - fonts-noto-color-emoji
  - fontconfig
  - gsfonts
  - hunspell-da
  - ocrmypdf
  - libimage-exiftool-perl
```

### Extending the configuration

There are some additional things you may wish to configure about the component.

Take a look at:

- [`defaults/main.yml`](../defaults/main.yml) for some variables that you can customize via your `vars.yml` file. You can override settings (even those that don't have dedicated playbook variables) using the `nextcloud_environment_variables_additional_variables` variable

See its [environment variables](https://github.com/docker-library/docs/blob/master/nextcloud/README.md#auto-configuration-via-environment-variables) for a complete list of Nextcloud's config options that you could put in `nextcloud_environment_variables_additional_variables`.

## Installing

After configuring the playbook, run the installation command of your playbook as below:

```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

If you use the MASH playbook, the shortcut commands with the [`just` program](https://github.com/mother-of-all-self-hosting/mash-playbook/blob/main/docs/just.md) are also available: `just install-all` or `just setup-all`

## Usage

After running the command for installation, the Nextcloud instance becomes available at the URL specified with `nextcloud_hostname` and `nextcloud_path_prefix`. With the configuration above, the service is hosted at `https://example.com`.

### Update configuration

Before logging in to the instance, update the configuration (URL paths, trusted reverse-proxies, etc.) by running the command below:

```sh
ansible-playbook -i inventory/hosts setup.yml --tags=adjust-nextcloud-config
```

>[!NOTE]
> You should re-run the command every time the Nextcloud version is updated.

You can open the URL with a web browser to log in to the instance. See [this official guide](https://docs.nextcloud.com/server/latest/admin_manual/contents.html) to get started.

### Integrate Collabora Online Development Edition (optional)

It is possible to integrate the Collabora Online Development Edition (CODE) instance to Nextcloud.

If you are looking for an Ansible role for CODE, you can check out [ansible-role-collabora-online](https://github.com/mother-of-all-self-hosting/ansible-role-collabora-online) maintained by the [Mother-of-All-Self-Hosting (MASH)](https://github.com/mother-of-all-self-hosting) team.

After installing CODE and [defining an allowed WOPI (Web Application Open Platform Interface) host](https://sdk.collaboraonline.com/docs/installation/CODE_Docker_image.html#how-to-configure-docker-image) to the `aliasgroup1` environment variable for the CODE instance, add the following configuration for Nextcloud to your `vars.yml` file:

```yaml
nextcloud_app_collabora_wopi_url: YOUR_CODE_INSTANCE_URL_HERE
```

Then, run this command to install and configure the [Office](https://apps.nextcloud.com/apps/richdocuments) app for Nextcloud:

```sh
ansible-playbook -i inventory/hosts setup.yml --tags=install-nextcloud-app-collabora
```

Open the URL `https://example.com/settings/admin/richdocuments` to have the instance set up the connection with the CODE instance.

You should then be able to open any document (`.doc`, `.odt`, `.pdf`, etc.) and create new ones in Nextcloud Files with Collabora Online Development Edition's editor.

>[!NOTE]
> By default, various private IPv4 networks are whitelisted to connect to the WOPI API (document serving API). If your CODE instance does not live on the same server as Nextcloud, you may need to adjust the list of networks. If necessary, redefine the `nextcloud_app_collabora_wopi_allowlist` environment variable on `vars.yml`.

### Enable Preview Generator app (optional)

It is also possible to set up preview generation by following the steps below.

The Preview Generator has two stages, [according to its README](https://github.com/nextcloud/previewgenerator).

- a generate-all phase — this has to be executed only a single time
- a pre-generate phase — this should be run in a cronjob. That runs quite fast if the generate-all phase finished.

As we do not want to run the generate-all phase multiple times, its execution timing is decided based on existence of the file created on the host side.

#### Enable preview on `vars.yml`

First, add the following configuration to `vars.yml` and run the playbook.

```yaml
nextcloud_preview_enabled: true
```

>[!NOTE]
> If it is set back to `false`, the host side files are cleaned up, and also the cron job is changed, not to call preview generation again. Note that the database and generated previews are kept intact thereafter.

You can edit other settings by adding the following configuration to your `vars.yml` file:

```yaml
# Specify the maximum size of the preview in pixels
nextcloud_preview_preview_max_x: MAX_HORIZONTAL_SIZE_HERE
nextcloud_preview_preview_max_y: MAX_VERTICAL_SIZE_HERE

# Specify JPEG quality for preview images
nextcloud_preview_app_jpeg_quality: MAX_QUALITY_VALUE_HERE
```

#### Run the command for config adjustment

Next, run the command below against your server, so that initial preview-generation is started and periodic generation of new images on your server is enabled:

    ```sh
    ansible-playbook -i inventory/hosts setup.yml --tags=adjust-nextcloud-config
    ```

### Post-build verification (optional)

After a custom image build completes you can run a quick acceptance sweep directly on the docker-host to ensure the preview/OCR toolchain and PHP overrides are present:

```sh
docker run --rm <image> php -m | grep -i imagick
docker run --rm <image> php -r 'echo ini_get("memory_limit"),"\n",ini_get("upload_max_filesize"),"\n",ini_get("post_max_size"),"\n",ini_get("max_execution_time"),"\n";'
docker run --rm <image> bash -lc 'convert -list format | egrep "^(PDF|PS|EPS|XPS|HEIC|WEBP) "'
docker run --rm <image> bash -lc 'convert -list configure | grep -i DELEGATES'
docker run --rm <image> tesseract --list-langs | egrep '(^| )(eng|dan)( |$)'
docker run --rm <image> ocrmypdf --version
docker run --rm <image> ffmpeg -v error -hide_banner -filters >/dev/null
docker run --rm -u 33:33 <image> bash -lc \
  'cp /usr/share/doc/base-files/copyright /tmp/in.txt && \
   soffice --headless --nologo --nodefault --nolockcheck --nocrashreport \
           --convert-to pdf --outdir /tmp /tmp/in.txt && test -s /tmp/in.pdf'
```

Running it sets up the variables and calls the generate-all script, that will also create the file —— signalling its finished state —— on the host.

**Notes**:

- The initial generation may take a long time, and a continuous prompt is presented by Ansible as some visual feedback (it is being run as an async task). Note it will timeout after approximately 27 hours. For reference, it should take about 10 minutes to finish generating previews of 60 GB data, most of which being image files.
- If it takes more time to run than a day, you may want to start it by running the command on the host:

    ```sh
    /usr/bin/env docker exec mash-nextcloud-server php /var/www/html/occ preview:generate-all
    ```

### Connecting to LDAP server

Nextcloud ships with an LDAP application to allow LDAP (including Active Directory) users to log in to the Nextcloud instance with their LDAP credentials.

#### Manual configuration

To configure the application manually, first enable the application on the Apps page in the Nextcloud instance, and then go to your Admin page where you can find the control panel with four tabs to configure the application.

Before proceeding, it is recommended to have a look at [this section](https://docs.nextcloud.com/server/latest/admin_manual/configuration_user/user_auth_ldap.html#server-tab) on the admin manual about how the application is expected to be configured for your needs. On [this page](https://docs.nextcloud.com/server/stable/admin_manual/configuration_user/user_auth_ldap_api.html#configuration-keys) is a list of the configuration keys available for LDAP configuration API as well.

#### Automatic configuration

It is also possible to configure the LDAP application for your LDAP server automatically.

First, add the following configuration for Nextcloud to your `vars.yml` file (adapt to your needs):

```yaml
# Specify the name of a admin group whose members also have administrative privileges on Nextcloud
# Example: lldap_admin
nextcloud_ldap_admin_group: ""

# Specify Distinguished Name (DN) of a user who has search privileges in the LDAP directory
# Example: uid=agent,ou=people,{{ nextcloud_ldap_base }}
nextcloud_ldap_agent_name: ""

# Specify the base DN of LDAP, from where all users and groups can be reached
# Example: dc=example,dc=com
nextcloud_ldap_base: ""

# Specify the hostname of the LDAP server
# Example: ldap://mash-lldap
nextcloud_ldap_host: ""

# Specify the base for users. It defaults to `nextcloud_ldap_base` if not specified
# Example: ou=people,{{ nextcloud_ldap_base }}
nextcloud_ldap_base_users: ""

# Specify the base for group. It defaults to `nextcloud_ldap_base` if not specified
# Example: ou=groups,{{ nextcloud_ldap_base }}
nextcloud_ldap_base_groups: ""
```

For other settings, check variables starting with `nextcloud_ldap_*` on [`defaults/main.yml`](../defaults/main.yml) and modify values per your needs and installation.

>[!NOTE]
>
> - Only `nextcloud_ldap_host` is mandatory. If your LDAP server requires authentication, it is necessary to specify `nextcloud_ldap_agent_name` as well. Note that search privilege is sufficient for the bind user.
> - The default values on `defaults/main.yml` are based on documentation at Nextcloud All-in-One repository available at [this page](https://github.com/nextcloud/all-in-one/tree/main/community-containers/lldap), intended for being used to connect to a [LLDAP](https://github.com/lldap/lldap/) server. For details about configuring LLDAP, [its guide](https://github.com/lldap/lldap/blob/main/README.md#general-configuration-guide) is worth reading.

After adding and modifying those variables, you can make use of the command below to run tasks specified on [`tasks/ldap.yml`](../tasks/ldap.yml):

```sh
ansible-playbook -i inventory/hosts setup.yml --tags=set-ldap-config-nextcloud -e agent_password=PASSWORD_OF_BIND_USER_HERE
```

To `agent_password`, set the password of the bind user (on this case: `agent`).

### Using the occ command

It is possible to run occ command, Nextcloud's command line interface, by running the `occ-nextcloud` tag, setting the `command` extra variable.

For example, you can install (and enable) [Forms](https://apps.nextcloud.com/apps/forms) by running the command as below:

```sh
ansible-playbook -i inventory/hosts setup.yml --tags=occ-nextcloud -e command="'app:install forms'"
```

See [this page](https://docs.nextcloud.com/server/latest/admin_manual/occ_command.html) for the list of available commands.

## Maintenance

### Running mimetype migrations

After the initial installation or upgrading the instance, there might appear a warning on the administration overview page at `https://example.com/settings/admin/overview` about mimetype migrations.

The command below is available for the migrations:

```sh
ansible-playbook -i inventory/hosts setup.yml --tags=mimetype-migrations-nextcloud
```

### Upgrading Nextcloud

It should be noted Nextcloud must be upgraded step by step and **you cannot skip major releases**.

For example, if you want to upgrade from version 29 to 31, you will have to upgrade from version 29 to 30, then from 30 to 31, by editing the `nextcloud_version` variable manually.

Also, **wait for background migrations to finish after major upgrades**. They are scheduled to run as a cronjob, and the schedule is defined by the `nextcloud_cron_schedule` variable.

See [this section](https://github.com/docker-library/docs/blob/master/nextcloud/README.md#update-to-a-newer-version) on the documentation of the Docker image, as well as [this page](https://docs.nextcloud.com/server/latest/admin_manual/maintenance/upgrade.html#approaching-upgrades) on the documentation for details.

## Troubleshooting

### Check the service's logs

You can find the logs in [systemd-journald](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html) by logging in to the server with SSH and running `journalctl -fu nextcloud-server` (or how you/your playbook named the service, e.g. `mash-nextcloud-server`).

### Query the server status

Run the command below to query the Nextcloud server status:

```sh
ansible-playbook -i inventory/hosts setup.yml --tags=query-status-nextcloud
```

#### Enable debug mode

You can enable debugging mode for Nextcloud by adding the following configuration to your `vars.yml` file:

```yml
nextcloud_config_parameter_debug: true
```

Make sure to run the command below to update the configuration:

```sh
ansible-playbook -i inventory/hosts setup.yml --tags=adjust-nextcloud-config
```

#### Increase logging verbosity

If you want to increase the verbosity, add the following configuration to your `vars.yml` file:

```yaml
nextcloud_config_parameter_loglevel: 0

nextcloud_config_parameter_loglevel_frontend: 0
```
