<!--
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Mobilizon

The playbook can install and configure [Mobilizon](https://joinmobilizon.org/en/) for you.

Mobilizon is a ActivityPub/Fediverse server to create and share events. See the project's [documentation](https://docs.mobilizon.org/) to learn what it does and why it might be useful to you.

## Depedencies

This service requires the following other services:

- a [Postgis](postgis.md) database (postgres based database that supports geospatial data)
- a [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# mobilizon                                                            #
#                                                                      #
########################################################################

mobilizon_enabled: true

mobilizon_hostname: 'events.example.org'

########################################################################
#                                                                      #
# /mobilizon                                                           #
#                                                                      #
########################################################################
```

>[!WARNING]
> DO NOT change the hostname after the instance has already run once. If changed, the Mobilizon instance stop working properly!

### Enable Postgis

You also need to enable [Postgis](./postgis.md) for a database server by adding the following configuration:

```yaml
########################################################################
#                                                                      #
# postgis                                                              #
#                                                                      #
########################################################################

postgis_enabled: true

# Put a strong password below, generated with `pwgen -s 64 1` or in another way
postgis_connection_password: ''

########################################################################
#                                                                      #
# /postgis                                                             #
#                                                                      #
########################################################################
```

### Make registration open (optional)

To enable registration at the instance by anyone, add the following configuration to your `vars.yml` file:

```yaml
mobilizon_registrations_open: true
```

### Usage

After [installing](../installing.md), you can visit at the URL specified in `mobilizon_hostname` and should see your instance.

To create an admin account, run the following command:

```sh
just run-tags mobilizon-add-admin --extra-vars=password=<password> --extra-vars=email=<email>
```
