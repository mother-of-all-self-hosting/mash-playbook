<!--
SPDX-FileCopyrightText: 2018 - 2023 Slavi Pantaleev
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Playbook tags

The Ansible playbook's tasks are tagged, so that certain parts of the Ansible
playbook can be run without running all other tasks.

The general command syntax is:
- (**recommended**) when using `just`: `just run-tags COMMA_SEPARATED_TAGS_GO_HERE`
- when not using `just`: `ansible-playbook -i inventory/hosts setup.yml --tags=COMMA_SEPARATED_TAGS_GO_HERE`

Here are some playbook tags that you should be familiar with:

- `setup-all` - runs all setup tasks (installation and uninstallation) for all
  components, but does not start/restart services

- `install-all` - like `setup-all`, but skips uninstallation tasks. Useful for
  maintaining your setup quickly when its components remain unchanged. If you
  adjust your `vars.yml` to remove components, you'd need to run `setup-all`,
  or these components will still remain installed

- `setup-SERVICE` (e.g. `setup-miniflux`) - runs setup tasks only for a given
  role, but does not start/restart services. You can discover these additional
  tags in each role (`roles/**/tasks/main.yml`). Running per-component setup
  tasks is usually not recommended, because components sometimes depend on each
  other. For example, setting up [Miniflux](services/miniflux.md), in addition
  to `setup-miniflux`, also requires database changes (`setup-postgres`).

- `install-SERVICE` (e.g. `install-miniflux`) - like `setup-SERVICE`, but
  skips uninstallation tasks. See `install-all` above for additional
  information.

- `start` - starts all systemd services and makes them start automatically in
  the future

- `stop` - stops all systemd services

**Notes**:
- `setup-*` tags and `install-*` tags do not start services automatically,
  because you may wish to do things before starting services, such as importing
  a database dump or restoring data from another server.
- Please be careful not to confuse playbook tags with `just` shortcut commands
  (recipes). For details, see [Running `just` commands](just.md).
- `just install-all` expands to `install-all,start`, and `just setup-all`
  expands to `setup-all,start`.
