<!--
SPDX-FileCopyrightText: 2026 spatterlight

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Unpackerr

The playbook can install and configure [Unpackerr](https://unpackerr.zip/) for you.

Unpackerr is an archive extraction daemon, which extracts completed downloads so that [Sonarr](../sonarr/README.md), [Radarr](../radarr/README.md), [Lidarr](../lidarr/README.md) and other Starr apps can import them. It can also watch folders and extract whatever archives appear in them.

See the project's [documentation](https://unpackerr.zip/docs/introduction) to learn what Unpackerr does and why it might be useful to you.

For details about configuring the [Ansible role for Unpackerr](https://github.com/mother-of-all-self-hosting/ansible-role-unpackerr), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-unpackerr/blob/main/docs/configuring-unpackerr.md) online
- 📁 `roles/galaxy/unpackerr/docs/configuring-unpackerr.md` locally, if you have [fetched the Ansible roles](../../docs/installing.md)

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../../docs/installing.md) process:

```yaml
########################################################################
#                                                                      #
# unpackerr                                                            #
#                                                                      #
########################################################################

unpackerr_enabled: true

########################################################################
#                                                                      #
# /unpackerr                                                           #
#                                                                      #
########################################################################
```

Unpackerr does nothing until it is given access to the download directory and at least one Starr app or folder to watch. Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-unpackerr/blob/main/docs/configuring-unpackerr.md#mount-the-download-directory) on the role's documentation for how to mount the download directory into Unpackerr at the same path as the Starr apps see it at.

### Connecting to Sonarr, Radarr and Lidarr

If [Sonarr](../sonarr/README.md), [Radarr](../radarr/README.md) or [Lidarr](../lidarr/README.md) is enabled as well, the playbook wires Unpackerr to it automatically: Unpackerr joins its container network and starts along with it.

Unpackerr still needs the URL and the API key of each Starr app. Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-unpackerr/blob/main/docs/configuring-unpackerr.md#connecting-unpackerr-to-the-starr-apps) on the role's documentation for details.

## Usage

After running the command for installation, Unpackerr starts working in the background, as it has no web UI. Whenever a Starr app it is connected to lists a completed download containing archives, Unpackerr extracts them, so that the Starr app can import the extracted files.

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-unpackerr/blob/main/docs/configuring-unpackerr.md#usage) on the role's documentation for details about the usage.

## Troubleshooting

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-unpackerr/blob/main/docs/configuring-unpackerr.md#troubleshooting) on the role's documentation for details.

## Related services

- [Lidarr](../lidarr/README.md) — Music collection manager for Usenet and BitTorrent users
- [qBittorrent](../qbittorrent/README.md) — A BitTorrent client
- [Radarr](../radarr/README.md) — Movie organizer/manager for Usenet and BitTorrent users
- [Sonarr](../sonarr/README.md) — PVR for newsgroup and BitTorrent users
