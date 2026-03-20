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

# Calibre-Web

The playbook can install and configure [Calibre-Web](https://github.com/janeczku/calibre-web) for you.

Calibre-Web is a web app that offers a clean and intuitive interface for browsing, reading, and downloading eBooks using a valid [Calibre](https://calibre-ebook.com/) database.

See the project's [documentation](https://github.com/janeczku/calibre-web/wiki) to learn what Calibre-Web does and why it might be useful to you.

For details about configuring the [Ansible role for Calibre-Web](https://github.com/mother-of-all-self-hosting/ansible-role-calibre-web), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-calibre-web/blob/master/docs/configuring-calibre-web.md) online
- 📁 `roles/galaxy/calibre_web/docs/configuring-calibre-web.md` locally, if you have [fetched the Ansible roles](../installing.md)

> [!WARNING]
> Calibre-Web currently does not support running the container rootless. While the role is configured to run with the MASH user and group specified to PUID and PGID on its [`env`](https://github.com/mother-of-all-self-hosting/ansible-role-calibre-web/blob/master/templates/env.j2) file, the common security features provided with other services of the playbook are not available. This puts your system at higher risk as vulnerabilities can have a higher impact.

## Prerequisites

The service requires you to have an existing Calibre database on `/books`. If you do not have one, you can download a sample database from the URL which can be found at <https://github.com/janeczku/calibre-web/blob/master/README.md#quick-start>.

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server
- (optional) [exim-relay](exim-relay.md) mailer

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# calibre_web                                                          #
#                                                                      #
########################################################################

calibre_web_enabled: true

calibre_web_hostname: mash.example.com
calibre_web_path_prefix: /calibre-web

########################################################################
#                                                                      #
# /calibre_web                                                         #
#                                                                      #
########################################################################
```

### Mount a directory for loading Calibre database (optional)

By default, Calibre-Web will search `/books` directory for your Calibre database.

You can mount a directory so that the instance loads the database. To mount it, prepare a local directory on the host machine and add the following configuration to your `vars.yml` file:

```yaml
calibre_web_books_path: /path/on/the/host
```

Make sure permissions and owner of the directory specified to `calibre_web_books_path`.

### Enable ebook conversion binary (optional)

You can add the Calibre ebook-convert binary (x64 only) by adding the following configuration to your `vars.yml` file:

```yaml
calibre_web_environment_variables_conversion_ability_enabled: true
```

The path to the binary is `/usr/bin/ebook-convert`. It needs to be specified in the web interface — as well as the path to Calibre binaries (`usr/bin`).

### File management

Since Calibre-Web is just a ebook browser and reader, you would need to prepare ebook files to be managed with it.

If your server runs a file management service along with Calibre-Web such as [File Browser](filebrowser.md), [FileBrowser Quantum](filebrowser-quantum.md), and [Syncthing](syncthing.md), it is possible to upload files to the server or synchronize your books directory with it to make them accessible on Calibre-Web.

#### Preparing directories

First, let's create a directory to be shared with the services. You can make use of the [aux](auxiliary.md) role by adding the following configuration to your `vars.yml` file. We create two directories here; the directory to be shared among Calibre-Web and other services, and its parent directory. If you are willing to have other services share directories, you can add another path by adding one to the list:

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

#### Mounting the directory into the Calibre-Web container

Next, mount the `{{ mash_playbook_base_path }}/storage/books` directory into the Calibre-Web container.

>[!NOTE]
> The directory may be mounted as read-only to prevent data inside the directory from accidentally being deleted or modified by Calibre-Web.

```yaml
########################################################################
#                                                                      #
# calibre_web                                                          #
#                                                                      #
########################################################################

# Other Calibre-Web configuration …

calibre_web_container_additional_volumes_custom:
  - type: bind
    src: "{{ mash_playbook_base_path }}/storage/books"
    dst: /books
    options: readonly

########################################################################
#                                                                      #
# /calibre_web                                                         #
#                                                                      #
########################################################################
```

#### Sharing the directory with other containers

You can then mount this `{{ mash_playbook_base_path }}/storage/books` directory on other service's container.

For example, adding the configuration below will let you to access to `/books` directory on the File Browser's UI, so that you can upload files to the server directly and make them accessible on Calibre-Web:

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

After running the command for installation, the Calibre-Web instance becomes available at the URL specified with `calibre_web_hostname` and `calibre_web_path_prefix`. With the configuration above, the service is hosted at `https://mash.example.com/calibre-web`.

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-calibre-web/blob/master/docs/configuring-calibre-web.md#usage) for details about setting up the instance.

### Configuring the mailer (optional)

On Calibre-Web you can add configuration settings of a SMTP server to let the service send email to terminals like Kindle and Pocketbook. If you enable the [exim-relay](exim-relay.md) service in your inventory configuration, the playbook will automatically configure it as a mailer for the service.

As the Calibre-Web instance does not support configuring the mailer with environment variables, you can add default options for it on its UI. Refer to [this page](https://github.com/janeczku/calibre-web/wiki/Setup-Mailserver) on the official documentation as well about how to configure it.

To set up with the default exim-relay settings, open `https://mash.example.com/calibre-web/admin/mailsettings` to add the following configuration:

- **Email Account Type**: Standard Email Account
- **SMTP Hostname**: `mash-exim-relay`
- **SMTP Port**: 8025
- **Encryption**: None
- **SMTP Login**: (Empty)
- **SMTP Password**: (Empty)
- **From Email**: (Input the email address specified to `exim_relay_sender_address` on your `vars.yml`)

After setting the configuration, you can have the Calibre-Web instance send a test mail to the mail address specified to your account.

>[!WARNING]
> Without setting an authentication method such as DKIM, SPF, and DMARC for your hostname, emails are most likely to be quarantined as spam at recipient's mail servers. The worst scenario is that your server's IP address or hostname will be included in the spam list such as the one managed by [Spamhaus](https://www.spamhaus.org/), depending on the reputation. As the exim-relay service supports DKIM signing, refer to [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay/blob/main/docs/configuring-exim-relay.md#enable-dkim-support-optional) for details about how to set it up.

## Related services

- [audiobookshelf](audiobookshelf.md) — Self-hosted audiobook and podcast server
- [Calibre-Web Automated](calibre-web-automated.md) — Web application based on Calibre-Web with additional features and automation
