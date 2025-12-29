<!--
SPDX-FileCopyrightText: 2018 Aaron Raimist
SPDX-FileCopyrightText: 2019 - 2020 MDAD project contributors
SPDX-FileCopyrightText: 2019 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2019 Noah Fleischmann
SPDX-FileCopyrightText: 2020 Marcel Partap
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Maintenance and Troubleshooting

## Maintenance

### Remove unused Docker data

You can free some disk space from Docker by running `docker system prune -a` on the server.

### Consider disabling unused services

To reduce attack surfaces like zero-day vulnerabilities it might be worth considering to disable services if they are not actively used. If a certain service for mission critical software like databases (such as [pgAdmin](services/pgadmin.md) and [phpMyAdmin](services/phpmyadmin.md)) does not have to be always online, you can safely get one run only when necessary, since the data in the container to be persistent is stored in its bind mount or a Docker volume. It will also help you to avoid running outdated services as unattended.

### MariaDB

See the dedicated [MariaDB Maintenance](https://github.com/mother-of-all-self-hosting/ansible-role-mariadb/blob/main/docs/configuring-mariadb.md#upgrading-mariadb) documentation page.

### Postgres

See the dedicated [PostgreSQL Maintenance](services/postgres.md#maintenance) documentation page.

## Troubleshooting

### How to see the current status of your services

You can check the status of your services by using `systemctl status`. Example:
```
sudo systemctl status mash-miniflux

● mash-miniflux.service - Miniflux (mash-miniflux)
   Loaded: loaded (/etc/systemd/system/mash-miniflux.service; enabled; vendor preset: disabled)
   Active: active (running) since Tue 2023-03-14 17:41:59 EET; 15h ago
```

### How to see the logs

Docker containers that the playbook configures are supervised by [systemd](https://wiki.archlinux.org/title/Systemd) and their logs are configured to go to [systemd-journald](https://wiki.archlinux.org/title/Systemd/Journal).

For example, you can find the logs of `mash-miniflux` in `systemd-journald` by logging in to the server with SSH and running the command as below:

```sh
sudo journalctl -fu mash-miniflux
```

#### Enable systemd/journald logs persistence

On some distros, the journald logs are just in-memory and not persisted to disk. Consult (and feel free to adjust) your distro's journald logging configuration in `/etc/systemd/journald.conf`.

To enable persistence and put some limits on how large the journal log files can become, adjust your configuration like this:

```ini
[Journal]
RuntimeMaxUse=200M
SystemMaxUse=1G
RateLimitInterval=0
RateLimitBurst=0
Storage=persistent
```

### Increasing logging

Various Ansible roles for various services supported by this playbook support a `*_log_level` variable or some debug mode which you can enable in your configuration and get extended logs. To activate the option, it is necessary to [re-run the playbook](installing.md) after making such configuration changes.
