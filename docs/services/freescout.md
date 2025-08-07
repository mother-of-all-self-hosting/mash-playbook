<!--
SPDX-FileCopyrightText: 2024 Nikita Chernyi
SPDX-FileCopyrightText: 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# FreeScout

The playbook can install and configure [FreeScout](https://freescout.net/) for you.

FreeScout is a free open-source helpdesk and shared inbox solution.

See the project's [documentation](https://github.com/freescout-help-desk/freescout/wiki) to learn what FreeScout does and why it might be useful to you.

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

After running the command for installation, the FreeScout instance becomes available at the URL specified with `freescout_hostname`. With the configuration above, the service is hosted at `https://freescout.example.com`.

You can log in to the instance with the administrator email address (`freescout_admin_email`) and password (`freescout_admin_password`).
