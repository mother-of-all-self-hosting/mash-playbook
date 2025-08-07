<!--
SPDX-FileCopyrightText: 2024 MASH project contributors
SPDX-FileCopyrightText: 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Tandoor

[Tandoor](https://docs.tandoor.dev/) is a self-hosted recipe manager, that this playbook can install, powered by the [ansible-role-tandoor](https://github.com/IUCCA/ansible-role-tandoor) Ansible role.


## Dependencies

This service requires the following other services:
- a [Postgres](postgres.md) database
- a [Traefik](traefik.md) reverse-proxy server


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# tandoor                                                              #
#                                                                      #
########################################################################

tandoor_enabled: true

tandoor_hostname: mash.example.com
tandoor_path_prefix: /tandoor

########################################################################
#                                                                      #
# /tandoor                                                             #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the Tandoor instance becomes available at the URL specified with `tandoor_hostname` and `tandoor_path_prefix`. With the configuration above, the service is hosted at `https://mash.example.com/tandoor`.

As mentioned in [Authentication](#authentication) above, you'll be asked to create the first administrator user the first time you open the web UI.
