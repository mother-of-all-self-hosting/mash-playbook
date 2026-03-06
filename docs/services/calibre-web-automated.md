<!--
SPDX-FileCopyrightText: 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2024 noah
SPDX-FileCopyrightText: 2024, 2025 MASH project contributors
SPDX-FileCopyrightText: 2025, 2026 Suguru Hirahara

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

### Syncthing integration (optional)

If you've got a [Syncthing](syncthing.md) service running, you can use it to synchronize your books directory with the server, and then mount it as read-only onto the Calibre-Web Automated container.

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
    dst: /calibre-library

########################################################################
#                                                                      #
# /syncthing                                                           #
#                                                                      #
########################################################################
```

Finally, mount the `{{ mash_playbook_base_path }}/storage/books` directory on the Calibre-Web Automated container as read-only:

```yaml
########################################################################
#                                                                      #
# calibre_web_automated                                                #
#                                                                      #
########################################################################

# Other Calibre-Web Automated configuration..

calibre_web_automated_container_additional_volumes:
  - type: bind
    src: "{{ mash_playbook_base_path }}/storage/books"
    dst: /calibre-library

########################################################################
#                                                                      #
# /calibre_web_automated                                               #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the Calibre-Web Automated instance becomes available at the URL specified with `calibre_web_automated_hostname`. With the configuration above, the service is hosted at `https://cwa.example.com`.

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3AzSfEaojv4NnFnivPm248Lx123CNe/tree/docs/configuring-calibre-web-automated.md#usage) for details about setting up the instance.

### Configure the SMTP server (optional)

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

## Troubleshooting

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3AzSfEaojv4NnFnivPm248Lx123CNe/tree/docs/configuring-calibre-web-automated.md#troubleshooting) on the role's documentation for details.

## Related services

- [audiobookshelf](audiobookshelf.md) — Self-hosted audiobook and podcast server
- [Syncthing](syncthing.md) — a continuous file synchronization program which synchronizes files between two or more computers in real time. See [Syncthing integration](#syncthing-integration)
