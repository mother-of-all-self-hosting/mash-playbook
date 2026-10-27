<!--
SPDX-FileCopyrightText: 2023 Nikita Chernyi
SPDX-FileCopyrightText: 2023 Slavi Pantaleev
SPDX-FileCopyrightText: 2023 aine-etke
SPDX-FileCopyrightText: 2025-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Cleanup

The playbook incorporates the [ansible-role-cleanup](https://github.com/mother-of-all-self-hosting/ansible-role-cleanup) Ansible role. It helps you to perform some housekeeping: cleaning up Docker leftovers, logs, paths, and (Debian only) packages and old kernels.

For details about configuring the role, you can check them via:

- 🌐 [the role's `defaults/main.yml`](https://github.com/mother-of-all-self-hosting/ansible-role-cleanup/blob/main/defaults/main.yml) online
- 📁 `roles/galaxy/cleanup/defaults/main.yml` locally, if you have [fetched the Ansible roles](../../docs/installing.md)

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../../docs/installing.md) process:

```yaml
########################################################################
#                                                                      #
# system                                                               #
#                                                                      #
########################################################################

# Removes stopped containers and Docker images which a newer image of the same repository superseded
# at least 3 days ago (and which no container uses). Unlike `docker image prune -a`, unused images
# without a newer version (of stopped services, timer-only containers, locally built images) are kept.
# Runs on runs with the `start` tag (e.g. `just setup-all`); to also run it daily via a systemd timer,
# enable `system_cleanup_docker_timer_enabled`.
system_cleanup_docker: true

# installs a systemd timer which runs `journalctl --vacuum-time=7d` daily
# (journald already limits the space logs take up on its own, so this is only needed for keeping logs for a shorter time)
system_cleanup_logs: false

# list of arbitrary absolute paths to remove on each invocation
system_cleanup_paths: []

# The following options are Debian only, will have no effect on any other distro family

# runs safe-upgrade, apt autoclean, aptautoremove, etc.
system_cleanup_apt: true

# WARNING: very dangerous! Purges old linux kernels, and their modules
system_cleanup_kernels: false

########################################################################
#                                                                      #
# /system                                                              #
#                                                                      #
########################################################################
```

Refer to the role's [`defaults/main.yml`](https://github.com/mother-of-all-self-hosting/ansible-role-cleanup/blob/main/defaults/main.yml) for more options (grace period, exclude patterns, dry run, anonymous volumes, the timer's schedule).

The Docker cleanup script (`/mash/system-cleanup/bin/cleanup-docker`) can also be run by hand, with `--dry-run` to only see what it would remove.

## Related services

Refer to [this section](../../docs/supported-services.md#system-related-components) for other system-related services.
