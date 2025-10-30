<!--
SPDX-FileCopyrightText: 2020 - 2024 MDAD project contributors
SPDX-FileCopyrightText: 2020 - 2024 Slavi Pantaleev
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
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Cap Standalone

The playbook can install and configure [Cap Standalone](https://cap.com) for you.

Cap Standalone is a backup software that securely stores encrypted, incremental, compressed backups on local storage, cloud storage services and remote file servers. It works with standard protocols like FTP, SSH, WebDAV as well as popular services like Microsoft OneDrive, Amazon S3 (compatible) Object Storage, Google Drive, box.com, Mega, B2, and many others.

See the project's [documentation](https://docs.cap.com) to learn what Cap Standalone does and why it might be useful to you.

For details about configuring the [Ansible role for Cap Standalone](https://github.com/mother-of-all-self-hosting/ansible-role-cap), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-cap/blob/main/docs/configuring-cap.md) online
- 📁 `roles/galaxy/cap/docs/configuring-cap.md` locally, if you have [fetched the Ansible roles](../installing.md)

>[!NOTE]
> As the Cap Standalone instance runs as the Docker container, it is necessary to mount the directory which includes files to back up on the host machine. Note that it is not able for the container to access files **outside of the mounted directory**.
>
> If you wish to manage a backup of directories on the machine without such restriction, you might probably want to consider to install Cap Standalone directly on the host machine. See [this page on the official documentation](https://docs.cap.com/getting-started/installation) for details.

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# cap                                                                  #
#                                                                      #
########################################################################

cap_enabled: true

cap_hostname: cap.example.com

########################################################################
#                                                                      #
# /cap                                                                 #
#                                                                      #
########################################################################
```

**Note**: hosting Cap Standalone under a subpath (by configuring the `cap_path_prefix` variable) does not seem to be possible due to Cap Standalone's technical limitations.

### Mount a directory for files to backup

You can mount the directory by adding the following configuration to your `vars.yml` file:

```yaml
cap_source_path: /path/on/the/host
```

Make sure permissions and owner of the directory specified to `cap_source_path`.

For example, you can mount the default directory used by the playbook (`/mash`) by adding the following configuration:

```yaml
cap_source_path: /mash
```

### Set a password for the UI

You also need to set a log in password on the web UI by adding the following configuration to your `vars.yml` file:

```yaml
cap_environment_variable_cap__webservice_password: YOUR_WEBUI_PASSWORD_HERE
```

Replace `YOUR_WEBUI_PASSWORD_HERE` with your own value.

## Usage

After running the command for installation, the Cap Standalone instance becomes available at the URL specified with `cap_hostname`. With the configuration above, the service is hosted at `https://cap.example.com`.

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-cap/blob/main/docs/configuring-cap.md#usage) for details about setting up a backup task.

⚠️ When setting the Source Data option, **choose `source` or directories inside it** as the backup source.

### Configure the SMTP mailer (optional)

On Cap Standalone you can set up the mailer to have it send reports about backup status. If you enable the [exim-relay](exim-relay.md) service in your inventory configuration, the playbook will automatically configure it as a mailer for the service.

As the Cap Standalone instance does not support configuring the mailer with environment variables, you can add default options for it on its UI (and override them with options for each job). Refer to [this page](https://docs.cap.com/detailed-descriptions/sending-reports-via-email/sending-reports-with-email) on the official documentation as well about how to configure it.

To set the default options, open `https://cap.example.com/ngax/index.html#/settings` to add the following configuration to "Default options" area (adapt to your needs):

```txt
--send-mail-from=noreply@mash.example.com
--send-mail-to=RECIPIENT_ADDRESS_HERE
--send-mail-url=smtp://mash-exim-relay:8025
--send-mail-level=Warning,Error
```

Replace `noreply@mash.example.com` and `RECIPIENT_ADDRESS_HERE` with the email address which should send and receive reports, respectively. If the default Exim-relay is used, `noreply@mash.example.com` should be replaced with the one specified on your `vars.yml` file.

Since the default report message is fairly verbose, you might probably want to customize it with the `send-mail-body` option.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-cap/blob/main/docs/configuring-cap.md#troubleshooting) on the role's documentation for details.

## Related services

- [BorgBackup](backup-borg.md) — Decapng backup program with optional compression and encryption
