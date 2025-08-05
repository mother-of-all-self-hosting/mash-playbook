<!--
SPDX-FileCopyrightText: 2024 shukon

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# DokuWiki

The playbook can install and configure [DokuWiki](https://dokuwiki.org/) for you.

DokuWiki is a lightweight, file-based wiki engine with intuitive syntax and no database requirements.

## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# dokuwiki                                                             #
#                                                                      #
########################################################################

dokuwiki_enabled: true

dokuwiki_hostname: dokuwiki.example.com

########################################################################
#                                                                      #
# /dokuwiki                                                            #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, Dokuwiki becomes available at the specified hostname like `https://dokuwiki.example.com/`.

You can go to the URL `https://dokuwiki.example.com/install.php` with a web browser to complete installation on the server. The instruction is available at <https://www.dokuwiki.org/installer>.
