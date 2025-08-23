<!--
SPDX-FileCopyrightText: 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2024 noah
SPDX-FileCopyrightText: 2024 - 2025 MASH project contributors
SPDX-FileCopyrightText: 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Readeck

The playbook can install and configure [Readeck](https://readeck.org) for you.

Readeck is a simple web application that lets you save the precious readable content of web pages you like and want to keep forever.

See the project's [documentation](https://readeck.org/en/docs/) to learn what Readeck does and why it might be useful to you.

## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# readeck                                                              #
#                                                                      #
########################################################################

readeck_enabled: true

readeck_hostname: readeck.example.com

########################################################################
#                                                                      #
# /readeck                                                             #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the Readeck instance becomes available at the URL specified with `readeck_hostname`. With the configuration above, the service is hosted at `https://readeck.example.com`.

To get started, open the URL with a web browser, and create a user.
