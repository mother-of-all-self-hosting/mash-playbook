<!--
SPDX-FileCopyrightText: 2024 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Wordpress

The playbook can install and configure [WordPress](https://wordpress.org/) for you.

Wordpress is a web content management system.

See the project's [documentation](https://codex.wordpress.org/Main_Page/) to learn what Wordpress does and why it might be useful to you.

## Dependencies

This service requires the following other services:

- [MariaDB](mariadb.md) database
- [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# wordpress                                                            #
#                                                                      #
########################################################################

wordpress_enabled: true

wordpress_hostname: wordpress.example.com

########################################################################
#                                                                      #
# /wordpress                                                           #
#                                                                      #
########################################################################
```

### Adjusting upload size limit

By default the size limit of uploaded files is set to `64M`. It is possible to adjust it by adding the following configuration to your `vars.yml` file:

```yaml
wordpress_max_upload_size: UPLOAD_SIZE_LIMIT_HERE
```

## Usage

After running the command for installation, the Wordpress instance becomes available at the URL specified with `wordpress_hostname`. With the configuration above, the service is hosted at `https://wordpress.example.com`.

To get started, open the URL with a web browser, and follow the set up wizard.

## Troubleshooting

FAQ is available on [this page](https://codex.wordpress.org/FAQ).
