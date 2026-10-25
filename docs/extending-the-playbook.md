<!--
SPDX-FileCopyrightText: 2026 MASH project contributors

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Extending the playbook with your own components

The playbook wires in each role it supports with a *component* (see [`components/`](../components)). You can add components of your own to your inventory, without changing the playbook. Use them to:

- run your own tasks at a given point of the playbook run (e.g. before services are set up, or after all of them are)
- install a service with a role which the playbook does not support (yet)
- register your own systemd services with the playbook's service manager, or have Postgres create a database for them

Put each component in a directory of its own under `components/` in your inventory directory (e.g. `inventory/components/YOUR-COMPONENT/`). Your components have the same structure as the playbook's (described in the [developer documentation](developer-documentation.md#3-update-the-mash-playbook-to-support-your-created-ansible-role)), and the playbook includes them in the same way: only while your inventory uses them (see `activation_prefix`).

If your component would be useful to others, consider adding it to the playbook instead.

## Example: your own tasks

This component runs a role of its own (in `roles/`, next to `component.yml`) after all services are set up:

```txt
inventory/
├── hosts
├── host_vars/
│   └── mash.example.com/
│       └── vars.yml  ← Contains `hooks_enabled: true`
└── components/
    └── hooks/
        ├── component.yml
        ├── wiring.yml
        └── roles/
            └── after_services/
                └── tasks/
                    └── main.yml
```

```yaml
# component.yml
activation_prefix: hooks_

setup:
  priority: 9050
  entry:
    - role: ./roles/after_services
      when: hooks_enabled | bool
      tags:
        - setup-all
        - install-all
        - setup-hooks
        - install-hooks
```

```yaml
# wiring.yml
hooks_enabled: false
```

Role paths starting with `./` are relative to the component's directory. Without tags, the role does not run when you run the playbook with tags, as `just install-all` does (see [Playbook tags](playbook-tags.md)).

A component can run in several places: make `setup` a list, with a `priority` and an `entry` each. A component which only adds configuration (e.g. `inject` entries for the systemd service manager) and runs nothing has `setup: []`.

## Example: a role which the playbook does not support

Add the role to the component's `requirements.yml`, named like the component's directory. The playbook installs it to `roles/galaxy/` along with its own roles, and runs it at the default priority:

```yaml
# requirements.yml
- src: git+https://github.com/YOUR-USERNAME/ansible-role-notes.git
  version: v1.0.0-0
  name: notes
```

Wire it in with `wiring.yml`, `with/` and `inject` as described in the [developer documentation](developer-documentation.md#3-update-the-mash-playbook-to-support-your-created-ansible-role). The playbook does not update the version of your role on `just update`: change it in `requirements.yml` yourself.

## Where your components run

`setup.yml` runs components by `priority` (lower runs earlier), and then by name. The playbook's components use these priorities:

| Priority | Components |
| --- | --- |
| 100 – 190 | The playbook itself, the base system and Docker (e.g. `playbook_base` 110, `systemd_docker_base` 130, `docker` 140) |
| 200 – 230 | Shared services: `container_socket_proxy` 200, `exim_relay` 210, `postgres` 220, `traefik` 230 |
| 1000 | All other services (the default) |
| 9000 – 9040 | Finishing steps: `auxiliary` 9000, `systemd_service_manager` 9010 (starts services), `cleanup` 9020, `playbook_state_preserver` 9030, `playbook_runtime_messages` 9040 |

The `priority` of each component is in its `component.yml`.

## Rules

- A component's name must differ from those of the playbook's components. If the playbook later adds a component with the name of yours, it stops with an error, and you need to rename yours.
- A variable may only be set by one component. To change the playbook's configuration, set the variable in your inventory (e.g. `vars.yml`), not in a component.
- The playbook checks your components before each run, and tells you what is wrong with them.
