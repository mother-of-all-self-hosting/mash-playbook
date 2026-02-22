<!--
SPDX-FileCopyrightText: 2023 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Running `just` commands

This playbook supports running playbook commands via [`just`](https://github.com/casey/just) — a more modern command-runner alternative to `make`. It can be used to invoke `ansible-playbook` commands with less typing.

The `just` utility executes shortcut commands (called as "recipes"), which invoke `ansible-playbook`, [`ansible-galaxy`](https://docs.ansible.com/ansible/latest/cli/ansible-galaxy.html) or [`agru`](https://github.com/etkecc/agru) (depending on what is available in your system). The targets of the recipes are defined in [`justfile`](../justfile).

For some recipes such as `just update`, our `justfile` recommends installing `agru` (a faster alternative to `ansible-galaxy`) to speed up the process.

Here are some examples of shortcuts:

| Shortcut                                       | Result                                                                                                         |
|------------------------------------------------|----------------------------------------------------------------------------------------------------------------|
| `just roles`                                   | Install the necessary Ansible roles pinned in [`requirements.yml`](../templates/requirements.yml)              |
| `just update`                                  | Run `git pull` (to update the playbook) and install the Ansible roles                                          |
| `just install-all`                             | Run `ansible-playbook -i inventory/hosts setup.yml --tags=install-all,start`                                   |
| `just setup-all`                               | Run `ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start`                                     |
| `just install-all --ask-vault-pass`            | Run commands with additional arguments (`--ask-vault-pass` will be appended to the above installation command) |
| `just run-tags install-miniflux,start`         | Run specific playbook tags (here `install-miniflux` and `start`)                                               |
| `just install-service miniflux`                | Run `just run-tags install-miniflux,start` with even less typing                                               |
| `just start-all`                               | (Re-)starts all services                                                                                       |
| `just stop-group postgres`                     | Stop only the Postgres service                                                                                 |

When both vault and become credentials are required, pass both prompt flags
together. Example:
`just install-all --ask-vault-pass --ask-become-pass`

While [our documentation on prerequisites](prerequisites.md) lists `just` as one of the requirements for installation, using `just` is optional. If you find it difficult to install it, do not find it useful, or want to prefer raw `ansible-playbook` commands for some reason, feel free to run all commands manually. For example, you can run `ansible-galaxy` directly to install the Ansible roles: `rm -rf roles/galaxy; ansible-galaxy install -r requirements.yml -p roles/galaxy/ --force`.

## Difference between playbook tags and shortcuts

It is worth noting that `just` "recipes" are different from [playbook tags](playbook-tags.md). The recipes are shortcuts of commands defined in `justfile` and can be executed by the `just` program only, while the playbook tags are available for the raw `ansible-playbook` commands as well. Please be careful not to confuse them.

For example, these two commands are different:
- `just install-all`
- `ansible-playbook -i inventory/hosts setup.yml --tags=install-all`

The just recipe runs `start` tag after `install-all`, while the latter runs only `install-all` tag. The correct shortcut of the latter is `just run-tags install-all`.

Such kind of difference sometimes matters. For example, when you install a server into which you will import old data (see [here](installing.md#installing-a-server-into-which-youll-import-old-data)), you are not supposed to run `just install-all` or `just setup-all`, because these commands start services immediately after installing components, which may prevent you from importing the data.

## Conditional service restart

When running `install-all` or `install-service` (whether via `just` or raw `ansible-playbook`), only services whose configuration or container image actually changed during the playbook run will be restarted. Unchanged services are left running (or get started if they were stopped). This reduces unnecessary downtime.

When running with `setup-*` tags (e.g. `setup-all`, `setup-miniflux`), all services are unconditionally restarted regardless of whether changes were detected. This is appropriate for setup's thorough "full setup" semantics.

`start-all` and `start-group` always restart all targeted services, since no installation tasks run during these commands.

This behavior is automatically determined based on the playbook tags in use. It can be overridden with the `devture_systemd_service_manager_conditional_restart_enabled` variable. For example, to force unconditional restarts during installation: `just install-all --extra-vars='devture_systemd_service_manager_conditional_restart_enabled=false'`
