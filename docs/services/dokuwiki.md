<!--
SPDX-FileCopyrightText: 2024 shukon
SPDX-FileCopyrightText: 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# DokuWiki

The playbook can install and configure [DokuWiki](https://www.dokuwiki.org/dokuwiki) for you.

DokuWiki is a lightweight, file-based wiki engine with intuitive syntax and no database requirements.

See the project's [documentation](https://www.dokuwiki.org/manual) to learn what DokuWiki does and why it might be useful to you.

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

After running the command for installation, the Dokuwiki instance becomes available at the URL specified with `dokuwiki_hostname`. With the configuration above, the service is hosted at `https://dokuwiki.example.com`.

To get started, open the URL `https://dokuwiki.example.com/install.php` with a web browser to complete installation on the server. The instruction is available at <https://www.dokuwiki.org/installer>.

## Related services

- [An Otter Wiki](otterwiki.md) — Minimalistic wiki powered by Python, Markdown and Git
- [MediaWiki](mediawiki.md) — Popular free and open-source wiki software
