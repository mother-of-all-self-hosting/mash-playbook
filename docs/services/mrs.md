<!--
SPDX-FileCopyrightText: 2023 Nikita Chernyi
SPDX-FileCopyrightText: 2023 Slavi Pantaleev
SPDX-FileCopyrightText: 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Matrix Rooms Search API

[Matrix Rooms Search](https://github.com/etkecc/mrs) is a fully-featured, standalone, [Matrix](https://matrix.org/) rooms search service.

## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# mrs                                                                  #
#                                                                      #
########################################################################

mrs_enabled: true
mrs_hostname: mrs.example.com

mrs_admin_login: admin
mrs_admin_password: changeme
mrs_admin_ips:
  - 123.123.123.123

mrs_servers:
  - matrix.org

########################################################################
#                                                                      #
# /mrs                                                                 #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the Matrix Rooms Search instance becomes available at the URL specified with `mrs_hostname`. With the configuration above, the service is hosted at `https://mrs.example.com`.

You can call the `https://mrs.example.com/-/full` endpoint using admin credentials (see the `mrs_admin_*` variables) to discover and parse content.

To see the list of supported public and private APIs, see the [API documentation](https://github.com/etkecc/mrs/blob/main/openapi.yml).

## Related services

- [Cinny](cinny.md) — Elegant web client for Matrix
