<!--
SPDX-FileCopyrightText: 2024 Nikita Chernyi

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Freescout

The playbook can install and configure [Freescout](https://freescout.net/) for you.

Freescout is a free open-source helpdesk and shared inbox solution.

## Dependencies

This service requires the following other services:

- a [Postgres](postgres.md) database
- a [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# freescout                                                            #
#                                                                      #
########################################################################

freescout_enabled: true

freescout_hostname: freescout.example.com

freescout_admin_email: your-email-here
freescout_admin_password: a-strong-password-here

########################################################################
#                                                                      #
# /freescout                                                           #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, Freescout becomes available at the specified hostname like `https://freescout.example.com`.

You can log in to the instance with the administrator email address (`freescout_admin_email`) and password (`freescout_admin_password`).
