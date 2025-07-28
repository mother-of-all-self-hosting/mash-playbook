<!--
SPDX-FileCopyrightText: 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2024 noah
SPDX-FileCopyrightText: 2024 - 2025 MASH project contributors
SPDX-FileCopyrightText: 2025 Suguru Hirahara

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

- a [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# calibre-web                                                          #
#                                                                      #
########################################################################

calibre_web_enabled: true

calibre_web_hostname: mash.example.com
calibre_web_path_prefix: /calibre-web

########################################################################
#                                                                      #
# /calibre-web                                                         #
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

### Syncthing integration (optional)

If you've got a [Syncthing](syncthing.md) service running, you can use it to synchronize your books directory with the server, and then mount it as read-only onto the Calibre-Web container.

We recommend that you make use of the [aux](auxiliary.md) role to create some shared directories as below:

```yaml
########################################################################
#                                                                      #
# aux                                                                  #
#                                                                      #
########################################################################

aux_directory_definitions:
  - dest: "{{ mash_playbook_base_path }}/storage"
  - dest: "{{ mash_playbook_base_path }}/storage/books"

########################################################################
#                                                                      #
# /aux                                                                 #
#                                                                      #
########################################################################
```

You can then mount this `{{ mash_playbook_base_path }}/storage/books` directory on the Syncthing container and synchronize it with other computers:

```yaml
########################################################################
#                                                                      #
# syncthing                                                            #
#                                                                      #
########################################################################

# Other Syncthing configuration..

syncthing_container_additional_volumes:
  - type: bind
    src: "{{ mash_playbook_base_path }}/storage/books"
    dst: /books

########################################################################
#                                                                      #
# /syncthing                                                           #
#                                                                      #
########################################################################
```

Finally, mount the `{{ mash_playbook_base_path }}/storage/books` directory on the Calibre-Web container as read-only:

```yaml
########################################################################
#                                                                      #
# calibre-web                                                          #
#                                                                      #
########################################################################

# Other Calibre-Web configuration..

calibre_web_container_additional_volumes:
  - type: bind
    src: "{{ mash_playbook_base_path }}/storage/books"
    dst: /books

########################################################################
#                                                                      #
# /calibre-web                                                         #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, Calibre-Web becomes available at the specified hostname with `calibre_web_hostname` and `calibre_web_path_prefix` like `https://mash.example.com/calibre-web`.

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-calibre-web/blob/master/docs/configuring-calibre-web.md#usage) for details about setting up the instance.

### Configure the SMTP server (optional)

On Calibre-Web you can set up the SMTP server to have the service send email to terminals like Kindle and Pocketbook. **You can use Exim-relay as the mailer, which is enabled on this playbook by default.** See [this page about Exim-relay configuration](exim-relay.md) for details about how to set it up.

As the Calibre-Web instance does not support configuring the mailer with environment variables, you can add default options for it on its UI. Refer to [this page](https://github.com/janeczku/calibre-web/wiki/Setup-Mailserver) on the official documentation as well about how to configure it.

To set up with the default Exim-relay settings, open `https://mash.example.com/calibre-web/admin/mailsettings` to add the following configuration:

- **Email Account Type**: Standard Email Account
- **SMTP Hostname**: `mash-exim-relay`
- **SMTP Port**: 8025
- **Encryption**: None
- **SMTP Login**: (Empty)
- **SMTP Password**: (Empty)
- **From Email**: (Input the email address specified to `exim_relay_sender_address` on your `vars.yml`)

After setting the configuration, you can have the Calibre-Web instance send a test mail to the mail address specified to your account.

## Recommended other services

- [Syncthing](syncthing.md) — a continuous file synchronization program which synchronizes files between two or more computers in real time. See [Syncthing integration](#syncthing-integration)
