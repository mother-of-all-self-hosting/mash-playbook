<!--
SPDX-FileCopyrightText: 2020 Aaron Raimist
SPDX-FileCopyrightText: 2020 Chris van Dijk
SPDX-FileCopyrightText: 2020 Dominik Zajac
SPDX-FileCopyrightText: 2020 Mickaël Cornière
SPDX-FileCopyrightText: 2020-2024 MDAD project contributors
SPDX-FileCopyrightText: 2020-2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2022 François Darveau
SPDX-FileCopyrightText: 2022 Julian Foad
SPDX-FileCopyrightText: 2022 Warren Bailey
SPDX-FileCopyrightText: 2023 Antonis Christofides
SPDX-FileCopyrightText: 2023 Felix Stupp
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 Thomas Miceli
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Duplicati

The playbook can install and configure [Duplicati](https://duplicati.com) for you.

Duplicati is a backup software that securely stores encrypted, incremental, compressed backups on local storage, cloud storage services and remote file servers. It works with standard protocols like FTP, SSH, WebDAV as well as popular services like Microsoft OneDrive, Amazon S3 (compatible) Object Storage, Google Drive, box.com, Mega, B2, and many others.

See the project's [documentation](https://docs.duplicati.com) to learn what Duplicati does and why it might be useful to you.

For details about configuring the [Ansible role for Duplicati](https://github.com/mother-of-all-self-hosting/ansible-role-duplicati), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-duplicati/blob/main/docs/configuring-duplicati.md) online
- 📁 `roles/galaxy/duplicati/docs/configuring-duplicati.md` locally, if you have [fetched the Ansible roles](../installing.md)

>[!NOTE]
> As the Duplicati instance runs as the Docker container, it is necessary to mount the directory which includes files to back up on the host machine. Note that it is not able for the container to access files **outside of the mounted directory**.
>
> If you wish to manage a backup of directories on the machine without such restriction, you might probably want to consider to install Duplicati directly on the host machine. See [this page on the official documentation](https://docs.duplicati.com/getting-started/installation) for details.

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server
- (optional) [exim-relay](exim-relay.md) mailer

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# duplicati                                                            #
#                                                                      #
########################################################################

duplicati_enabled: true

duplicati_hostname: duplicati.example.com

########################################################################
#                                                                      #
# /duplicati                                                           #
#                                                                      #
########################################################################
```

**Note**: hosting Duplicati under a subpath (by configuring the `duplicati_path_prefix` variable) does not seem to be possible due to Duplicati's technical limitations.

### Set a random string

You also need to set a random string to the variable as below by adding the following configuration to your `vars.yml` file. The value can be generated with `pwgen -s 64 1` or in another way.

```yaml
duplicati_environment_variable_settings_encryption_key: YOUR_SECRET_KEY_HERE
```

### Mount a directory for files to backup

You can mount the directory by adding the following configuration to your `vars.yml` file:

```yaml
duplicati_source_path: /path/on/the/host
```

Make sure permissions and owner of the directory specified to `duplicati_source_path`.

For example, you can mount the default directory used by the playbook (`/mash`) by adding the following configuration:

```yaml
duplicati_source_path: /mash
```

### Set a password for the UI

You also need to set a log in password on the web UI by adding the following configuration to your `vars.yml` file:

```yaml
duplicati_environment_variable_duplicati__webservice_password: YOUR_WEBUI_PASSWORD_HERE
```

Replace `YOUR_WEBUI_PASSWORD_HERE` with your own value.

## Usage

After running the command for installation, the Duplicati instance becomes available at the URL specified with `duplicati_hostname`. With the configuration above, the service is hosted at `https://duplicati.example.com`.

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-duplicati/blob/main/docs/configuring-duplicati.md#usage) for details about setting up a backup task.

⚠️ When setting the Source Data option, **choose `source` or directories inside it** as the backup source.

### Configure the SMTP mailer (optional)

On Duplicati you can set up the mailer to have it send reports about backup status. If you enable the [exim-relay](exim-relay.md) service in your inventory configuration, the playbook will automatically configure it as a mailer for the service.

As the Duplicati instance does not support configuring the mailer with environment variables, you can add default options for it on its UI (and override them with options for each job). Refer to [this page](https://docs.duplicati.com/detailed-descriptions/sending-reports-via-email/sending-reports-with-email) on the official documentation as well about how to configure it.

To set the default options, open `https://duplicati.example.com/ngax/index.html#/settings` to add the following configuration to "Default options" area (adapt to your needs):

```txt
--send-mail-from=noreply@mash.example.com
--send-mail-to=RECIPIENT_ADDRESS_HERE
--send-mail-url=smtp://mash-exim-relay:8025
--send-mail-level=Warning,Error
```

Replace `noreply@mash.example.com` and `RECIPIENT_ADDRESS_HERE` with the email address which should send and receive reports, respectively. If the default Exim-relay is used, `noreply@mash.example.com` should be replaced with the one specified on your `vars.yml` file.

Since the default report message is fairly verbose, you might probably want to customize it with the `send-mail-body` option.

>[!WARNING]
> Without setting an authentication method such as DKIM, SPF, and DMARC for your hostname, emails are most likely to be quarantined as spam at recipient's mail servers. The worst scenario is that your server's IP address or hostname will be included in the spam list such as the one managed by [Spamhaus](https://www.spamhaus.org/), depending on the reputation. As the exim-relay service supports DKIM signing, refer to [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay/blob/main/docs/configuring-exim-relay.md#enable-dkim-support-optional) for details about how to set it up.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-duplicati/blob/main/docs/configuring-duplicati.md#troubleshooting) on the role's documentation for details.

## Related services

- [BorgBackup](backup-borg.md) — Deduplicating backup program with optional compression and encryption
- [Borg Web UI](borg-ui.md) — Unofficial web interface for BorgBackup
