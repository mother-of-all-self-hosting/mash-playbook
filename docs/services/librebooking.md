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
# librebooking                                                         #
#                                                                      #
########################################################################

librebooking_enabled: true

librebooking_hostname: booking.example.com

# Protects the /Web/install/ setup wizard. Use a strong password.
librebooking_environment_variables_lb_install_password: "your-strong-install-password-here"

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

### First-time setup

LibreBooking does **not** initialize its database schema automatically. You must run the web-based install wizard on first install.

After running the playbook for the first time, retrieve your database credentials:

```bash
ansible-playbook -i inventory/hosts setup.yml --tags=print-db-credentials-librebooking
```

Then navigate to the install wizard:

```text
https://booking.example.com/Web/install/
```

You will be prompted for the **installation password** you set above. On the next page:

- Enter the database credentials printed above as the **MySQL User** and **Password**
- **Check "Import sample data"** — this creates the database schema and an initial `admin`/`password` account
- Do **not** check "Create the database" or "Create the database user" — both already exist
- Afterwards, log in with `admin`/`password` (and change the password)

## Usage

Log in at your configured URL using the administrator account created during setup.

## Upgrading

To upgrade, pin a new version and re-run the playbook:

```yaml
librebooking_version: "4.3.0"
```

After major version upgrades you may need to revisit the `/Web/install/` page to run pending database migrations.
