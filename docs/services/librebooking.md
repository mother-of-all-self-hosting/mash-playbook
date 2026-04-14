<!--
SPDX-FileCopyrightText: 2024 Mother-of-All-Self-Hosting contributors

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# LibreBooking

[LibreBooking](https://github.com/LibreBooking/app) is a simply powerful scheduling solution for any organization. It is an actively maintained FOSS fork of Booked Scheduler.

## Dependencies

This service requires:

- a [MariaDB](mariadb.md) database — LibreBooking does **not** support PostgreSQL

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# mariadb                                                              #
#                                                                      #
########################################################################

# If MariaDB is not already enabled for another service, enable it here.
mariadb_enabled: true

# Put a strong password below, generated with `pwgen -s 64 1` or another way
mariadb_root_password: ""

########################################################################
#                                                                      #
# /mariadb                                                             #
#                                                                      #
########################################################################


########################################################################
#                                                                      #
# librebooking                                                         #
#                                                                      #
########################################################################

librebooking_enabled: true

librebooking_hostname: booking.example.com

# To serve at a subpath instead of /, uncomment:
# librebooking_path_prefix: /booking

# Protects the /Web/install/ setup wizard. Use a strong password.
librebooking_install_password: "your-strong-install-password-here"

# Optional: set timezone
# librebooking_timezone: "Europe/Berlin"

# Optional: enable built-in cron for reminder emails, etc.
# librebooking_cron_enabled: 'true'

# Optional: pass additional LB_ environment variables.
# See: https://librebooking.readthedocs.io/en/stable/BASIC-CONFIGURATION.html
# librebooking_environment_variables_additional: |
#   LB_APP_TITLE=My Booking System
#   LB_COMPANY_NAME=Acme Corp

########################################################################
#                                                                      #
# /librebooking                                                        #
#                                                                      #
########################################################################
```

### Database

The playbook automatically provisions a MariaDB database and user for LibreBooking and wires up the connection. You do not need to set database credentials manually.

### First-time setup

After running the playbook for the first time, navigate to:

```
https://booking.example.com/Web/install/
```

Enter the `librebooking_install_password` you configured when prompted, then follow the wizard to initialize the database schema and create your administrator account.

Keep `librebooking_install_password` set to a strong value to prevent unauthorized access to the setup page.

## Usage

Log in at your configured URL using the administrator account created during setup.

## Upgrading

To upgrade, pin a new version and re-run the playbook:

```yaml
librebooking_version: "4.3.0"
```

After major version upgrades you may need to revisit the `/Web/install/` page to run pending database migrations.
