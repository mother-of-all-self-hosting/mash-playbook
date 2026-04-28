<!--
SPDX-FileCopyrightText: 2020 Aaron Raimist
SPDX-FileCopyrightText: 2020 Chris van Dijk
SPDX-FileCopyrightText: 2020 Dominik Zajac
SPDX-FileCopyrightText: 2020 Mickaël Cornière
SPDX-FileCopyrightText: 2020-2024 MDAD project contributors
SPDX-FileCopyrightText: 2020-2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2022 François Darveau
SPDX-FileCopyrightText: 2022 Julian Foad
SPDX-FileCopyrightText: 2022 Warren Bailey
SPDX-FileCopyrightText: 2023 Antonis Christofides
SPDX-FileCopyrightText: 2023 Felix Stupp
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 Mother-of-All-Self-Hosting contributors
SPDX-FileCopyrightText: 2024 Thomas Miceli
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara
SPDX-FileCopyrightText: 2026 shukon

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# LibreBooking

The playbook can install and configure [LibreBooking](https://github.com/LibreBooking/app) for you.

LibreBooking is a simply powerful scheduling solution for any organization. It is an actively maintained FOSS fork of Booked Scheduler.

See the project's [documentation](https://librebooking.readthedocs.io/) to learn what LibreBooking does and why it might be useful to you.

## Dependencies

This service requires the following other services:

- [MariaDB](mariadb.md) database
- [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# librebooking                                                         #
#                                                                      #
########################################################################

librebooking_enabled: true

librebooking_hostname: librebooking.example.com

# Protects the /Web/install/ setup wizard.
# Put a strong secret below, generated with `pwgen -s 64 1` or in another way
librebooking_environment_variables_lb_install_password: ""

# Optional: set the timezone
# librebooking_environment_variables_lb_default_timezone: "Europe/Berlin"

# Optional: enable background cron jobs (for reminder emails, etc.)
# librebooking_environment_variables_lb_cron_enabled: true

# Optional: allow users to self-register accounts (disabled by default).
# Enable temporarily if you need to register your admin account manually.
# librebooking_environment_variables_lb_registration_allow_self_registration: true

# Optional: pass extra LB_ environment variables to configure the application.
# See: https://librebooking.readthedocs.io/en/stable/BASIC-CONFIGURATION.html
# librebooking_environment_variables_additional_variables: |
#   LB_APP_TITLE='My Booking System'

########################################################################
#                                                                      #
# /librebooking                                                        #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the LibreBooking instance becomes available at the URL specified with `librebooking_hostname`. With the configuration above, the service is hosted at `https://librebooking.example.com`.

To get started, open the URL `https://librebooking.example.com/Web/install/` with a web browser, and follow the set up wizard. It is necessary to input the string specified to `librebooking_environment_variables_lb_install_password` as the installation password.

You can retrieve the database credentials by running the command below:

```bash
ansible-playbook -i inventory/hosts setup.yml --tags=print-db-credentials-librebooking
```

By checking "Import sample data" on the UI, the database schema and an initial `admin`/`password` account will be created.

>[!WARNING]
> Do **not** check "Create the database" or "Create the database user" — both already exist

After completing the set up wizard, you can log in to the instance with that account. Make sure to changed the password.

## Troubleshooting

After major version upgrades you may need to revisit the `/Web/install/` page to run pending database migrations.
