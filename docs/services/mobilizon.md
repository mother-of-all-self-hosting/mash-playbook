<!--
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Mobilizon

[Mobilizon](https://joinmobilizon.org/en/) is a ActivityPub/Fediverse server to create and share events here powered by the [mother-of-all-self-hosting/ansible-role-mobilizon](https://github.com/mother-of-all-self-hosting/ansible-role-mobilizon) Ansible role.

## Depedencies


This service requires the following other services:

- a [Postgis](postgis.md) database (postgres based database that supports geospatial data)
- a [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file. Also you need to enable postgis which will serve as database for mobilizon.
After that you can re-run the [installation](../installing.md) process.

```yaml
########################################################################
#                                                                      #
# mobilizon                                                            #
#                                                                      #
########################################################################

mobilizon_enabled: true


# Hostname that this server will be reachable at.
# DO NOT change this after your server has already run once, or you will break things!
mobilizon_hostname: 'events.example.org'

# to open registrations uncomment the following line
# mobilizon_registrations_open: true

########################################################################
#                                                                      #
# /mobilizon                                                           #
#                                                                      #
########################################################################
```

After installation, you can use `just run-tags mobilizon-add-admin --extra-vars=password=<password> --extra-vars=email=<email>`
to create your an admin account.

### Usage

After [installing](../installing.md), you can visit at the URL specified in `mobilizon_hostname` and should see your instance.

Refer to the [great official documentation](https://docs.joinmobilizon.org/use/) for more information on Mobilizon.
