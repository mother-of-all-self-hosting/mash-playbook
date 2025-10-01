<!--
SPDX-FileCopyrightText: 2023 Nikita Chernyi
SPDX-FileCopyrightText: 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Redmine

[Redmine](https://redmine.org/) is a flexible project management web application. Written using the Ruby on Rails framework, it is cross-platform and cross-database.

## Dependencies

This service requires the following other services:

- a [Postgres](postgres.md) database
- a [Traefik](traefik.md) reverse-proxy server


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# redmine                                                              #
#                                                                      #
########################################################################

redmine_enabled: true

redmine_hostname: redmine.example.com

# If you'll be installing Redmine plugins which pull Ruby gems,
# which need to compile native code, consider installing build tools in the container image,
# by uncommenting the line below.
# redmine_container_image_customizations_build_tools_installation_enabled: true

########################################################################
#                                                                      #
# /redmine                                                             #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the Redmine instance becomes available at the URL specified with `redmine_hostname`. With the configuration above, the service is hosted at `https://redmine.example.com`.

To get started, open the URL with a web browser, log in with the admin account created automatically on the initial run. Its credentials can be found at <https://hub.docker.com/_/redmine#accessing-the-application>. When logging in, you are required to reset the default password.
