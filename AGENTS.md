<!--
SPDX-FileCopyrightText: 2026 Slavi Pantaleev

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Working on MASH

This playbook consumes separately maintained Ansible roles.
For playbook configuration, edit sources under `templates/`.
Follow [developer documentation](docs/developer-documentation.md) for generated files and checks.
Roles own their configuration validation in `tasks/validate_config.yml`.
For role bumps, check the affected wiring, especially `templates/group_vars_mash_servers`.
If the role handles its configuration changes, the playbook wiring and existing docs remain valid,
and no consequential manual migration is needed, the version pin alone is usually enough.
Keep `docs/services/` focused on current configuration and lasting procedures.
Do not use service pages as another changelog for role releases.
Correct stale playbook examples, but leave role-specific option details in the role's documentation.

## Changelog

Use `CHANGELOG.md` for new or removed services, shared playbook behavior changes,
or consequential role-specific changes users must plan for.
Examples include a manual data migration or disruptive behavior that validation cannot explain.
State who is affected and what they need to do.

Skip entries for routine role bumps and for one role's renamed or removed variables or formats
when the affected role's `tasks/validate_config.yml` gives users an actionable error.
Correct stale service docs or examples; explain narrower upgrade risks in the pull request.
An upstream “breaking change” label alone does not require a playbook changelog entry.
