<!--
SPDX-FileCopyrightText: 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2024 noah
SPDX-FileCopyrightText: 2024 - 2025 MASH project contributors
SPDX-FileCopyrightText: 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Calibre-Web

[Calibre-Web](https://github.com/janeczku/calibre-web) is a web app that offers a clean and intuitive interface for browsing, reading, and downloading eBooks using a valid [Calibre](https://calibre-ebook.com/) database.

> [!WARNING]
> Calibre-Web currently does not support running the container rootless, therefore the role has not the usual security features of other services provided by this playbook. This put your system more at higher risk as vulnerabilities can have a higher impact.

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

# By default, calibre_web will look at the /books directory for your Calibre database.
#
# You'd need to mount some book directory into the calibre_web container, like shown below.
# The "Syncthing integration" section below may be relevant.
# calibre_web_container_additional_volumes:
#   - type: bind
#     src: /on-host/path/to/books
#     dst: /books

#
#
#
# Enable this extension explicitly to add the Calibre ebook-convert binary (x64 only). Omit this variable for a lightweight image.
# The path to the binary is /usr/bin/ebook-convert (has to be specified in the web interface — also specify the path to Calibre binaries as well; usr/bin)
#calibre_web_environment_variables_extension: |
#  DOCKER_MODS=linuxserver/mods:universal-calibre

########################################################################
#                                                                      #
# /calibre-web                                                         #
#                                                                      #
########################################################################
```

### URL

In the example configuration above, we configure the service to be hosted at `https://mash.example.com/calibre-web`.

You can remove the `calibre_web_path_prefix` variable definition, to make it default to `/`, so that the service is served at `https://mash.example.com/`.

### Authentication

The default username is `admin` and the default password is `admin123`.
You'll be able to change the username and password, and add additional users in the web UI.

On the initial setup screen, enter /books as your calibre library location.
If you haven't placed a Calibre database in that directory on the host yet, it will error as an invalid location.

### Syncthing integration

If you've got a [Syncthing](syncthing.md) service running, you can use it to synchronize your books directory onto the server and then mount it as read-only into the calibre_web container.

We recommend that you make use of the [aux](auxiliary.md) role to create some shared directory like this:

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

You can then mount this `{{ mash_playbook_base_path }}/storage/books` directory into the Syncthing container and synchronize it with some other computer:

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

Finally, mount the `{{ mash_playbook_base_path }}/storage/books` directory into the calibre-web container as read-only:

```yaml
########################################################################
#                                                                      #
# calibre-web                                                          #
#                                                                      #
########################################################################

# Other calibre-web configuration..

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

After installation, you can go to the calibre-web URL, as defined in `calibre_web_hostname` and `calibre_web_path_prefix`.

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
