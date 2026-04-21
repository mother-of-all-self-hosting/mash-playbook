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
SPDX-FileCopyrightText: 2024 noah
SPDX-FileCopyrightText: 2024, 2025 MASH project contributors
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Calibre-Web Automated

The playbook can install and configure [Calibre-Web Automated](https://github.com/crocodilestick/Calibre-Web-Automated) for you.

Calibre-Web Automated is a web application based on [Calibre-Web](https://github.com/janeczku/calibre-web) with additional features and automation.

See the project's [documentation](https://github.com/crocodilestick/Calibre-Web-Automated/blob/main/README.md) to learn what Calibre-Web Automated does and why it might be useful to you.

For details about configuring the [Ansible role for Calibre-Web Automated](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3AzSfEaojv4NnFnivPm248Lx123CNe), you can check them via:

- 🌐 [the role's documentation](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3AzSfEaojv4NnFnivPm248Lx123CNe/tree/docs/configuring-calibre-web-automated.md) online
- 📁 `roles/galaxy/calibre_web_automated/docs/configuring-calibre-web-automated.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server
- (optional) [exim-relay](exim-relay.md) mailer

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# calibre_web_automated                                                #
#                                                                      #
########################################################################

calibre_web_automated_enabled: true

calibre_web_automated_hostname: cwa.example.com

########################################################################
#                                                                      #
# /calibre_web_automated                                               #
#                                                                      #
########################################################################
```

### Migration from Calibre-Web

It is possible to migrate from Calibre-Web to Calibre-Web Automated. Refer to [this section](https://github.com/crocodilestick/Calibre-Web-Automated/blob/main/README.md#users-migrating-from-stock-calibre-web) on the documentation for details.

### File management

If your server runs a file management service along with Calibre-Web Automated such as [File Browser](filebrowser.md), [FileBrowser Quantum](filebrowser-quantum.md), and [Syncthing](syncthing.md), it is possible to upload files to the server or synchronize your books directory with it to make them accessible on Calibre-Web Automated.

#### Preparing directories

First, let's create a directory to be shared with the services. You can make use of the [aux](auxiliary.md) role by adding the following configuration to your `vars.yml` file. We create two directories here; the directory to be shared among Calibre-Web Automated and other services, and its parent directory. If you are willing to have other services share directories, you can add another path by adding one to the list:

```yaml
########################################################################
#                                                                      #
# aux                                                                  #
#                                                                      #
########################################################################

aux_directory_definitions:
  - dest: "{{ mash_playbook_base_path }}/storage"
  - dest: "{{ mash_playbook_base_path }}/storage/books"
# - dest: another shared directory path …

########################################################################
#                                                                      #
# /aux                                                                 #
#                                                                      #
########################################################################
```

#### Mounting the directory into the Calibre-Web Automated container

Next, mount the `{{ mash_playbook_base_path }}/storage/books` directory into the Calibre-Web Automated container.

>[!NOTE]
> The directory is mounted as writable to enable data modification and deletion by Calibre-Web Automated.

```yaml
########################################################################
#                                                                      #
# calibre_web_automated                                                #
#                                                                      #
########################################################################

# Other Calibre-Web Automated configuration …

calibre_web_automated_container_additional_volumes_custom:
  - type: bind
    src: "{{ mash_playbook_base_path }}/storage/books"
    dst: /calibre-library

########################################################################
#                                                                      #
# /calibre_web_automated                                               #
#                                                                      #
########################################################################
```

#### Sharing the directory with other containers

You can then mount this `{{ mash_playbook_base_path }}/storage/books` directory on other service's container.

For example, adding the configuration below will let you to access to `/books` directory on the File Browser's UI, so that you can upload files to the server directly and make them accessible on Calibre-Web Automated:

```yaml
########################################################################
#                                                                      #
# filebrowser                                                          #
#                                                                      #
########################################################################

# Other File Browser configuration …

filebrowser_container_additional_volumes_custom:
  - type: bind
    src: "{{ mash_playbook_base_path }}/storage/books"
    dst: "/srv/books"

########################################################################
#                                                                      #
# /filebrowser                                                         #
#                                                                      #
########################################################################
```

Adding the configuration below makes it possible for the Syncthing service to synchronize the directory with other computers:

```yaml
########################################################################
#                                                                      #
# syncthing                                                            #
#                                                                      #
########################################################################

# Other Syncthing configuration …

syncthing_container_additional_volumes_custom:
  - type: bind
    src: "{{ mash_playbook_base_path }}/storage/books"
    dst: /books

########################################################################
#                                                                      #
# /syncthing                                                           #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the Calibre-Web Automated instance becomes available at the URL specified with `calibre_web_automated_hostname`. With the configuration above, the service is hosted at `https://cwa.example.com`.

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3AzSfEaojv4NnFnivPm248Lx123CNe/tree/docs/configuring-calibre-web-automated.md#usage) for details about setting up the instance.

### Configuring the mailer (optional)

On Calibre-Web Automated you can add configuration settings of a SMTP server to let the service send email to terminals like Kindle and Pocketbook. If you enable the [exim-relay](exim-relay.md) service in your inventory configuration, the playbook will automatically configure it as a mailer for the service.

As the Calibre-Web Automated instance does not support configuring the mailer with environment variables, you can add default options for it on its UI.

To set up with the default exim-relay settings, open `https://cwa.example.com/admin/mailsettings` to add the following configuration:

- **Email Account Type**: Standard Email Account
- **SMTP Hostname**: `mash-exim-relay`
- **SMTP Port**: 8025
- **Encryption**: None
- **SMTP Login**: (Empty)
- **SMTP Password**: (Empty)
- **From Email**: (Input the email address specified to `exim_relay_sender_address` on your `vars.yml`)

After setting the configuration, you can have the Calibre-Web Automated instance send a test mail to the mail address specified to your account.

>[!WARNING]
> Without setting an authentication method such as DKIM, SPF, and DMARC for your hostname, emails are most likely to be quarantined as spam at recipient's mail servers. The worst scenario is that your server's IP address or hostname will be included in the spam list such as the one managed by [Spamhaus](https://www.spamhaus.org/), depending on the reputation. As the exim-relay service supports DKIM signing, refer to [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay/blob/main/docs/configuring-exim-relay.md#enable-dkim-support-optional) for details about how to set it up.

## Troubleshooting

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3AzSfEaojv4NnFnivPm248Lx123CNe/tree/docs/configuring-calibre-web-automated.md#troubleshooting) on the role's documentation for details.

## Related services

- [audiobookshelf](audiobookshelf.md) — Self-hosted audiobook and podcast server
