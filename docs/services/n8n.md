<!--
SPDX-FileCopyrightText: 2023 kinduff

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# n8n

[n8n](https://n8n.io/) is a workflow automation tool for technical people.

## Dependencies

This service requires the following other services:

-   a [Postgres](postgres.md) database
-   a [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# n8n                                                                  #
#                                                                      #
########################################################################

n8n_enabled: true

n8n_hostname: mash.example.com
n8n_path_prefix: /n8n

########################################################################
#                                                                      #
# /n8n                                                                 #
#                                                                      #
########################################################################
```

In the example configuration above, we configure the service to be hosted at `https://mash.example.com/n8n`.

You can remove the `n8n_path_prefix` variable definition, to make it default to `/`, so that the service is served at `https://mash.example.com/`.

## Usage

You can create additional users (admin-privileged or not) after logging in.
