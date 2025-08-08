<!--
SPDX-FileCopyrightText: 2023 Niels Bouma
SPDX-FileCopyrightText: 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Changedetection.io

The playbook can install and configure [Changedetection.io](https://github.com/dgtlmoon/changedetection.io) for you.

Changedetection.io is a simple website change detection and restock monitoring solution.

See the project's [documentation](https://github.com/dgtlmoon/changedetection.io/blob/master/README.md) to learn what Changedetection.io does and why it might be useful to you.

## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# Changedetection.io                                                   #
#                                                                      #
########################################################################

changedetection_enabled: true

changedetection_hostname: mash.example.com
changedetection_path_prefix: /changedetection

########################################################################
#                                                                      #
# /Changedetection.io                                                  #
#                                                                      #
########################################################################
```

### Enable Playwright webdriver for advanced options (optional)

Some advanced options like using Javascript or the Visual Selector tool require an additional Playwright webdriver.

You can enable it by adding the following configuration to your `vars.yml` file:

```yaml
changedetection_playwright_driver_enabled: true
```

## Usage

After running the command for installation, Changedetection.io becomes available at the specified hostname like `https://mash.example.com/changedetection`.
