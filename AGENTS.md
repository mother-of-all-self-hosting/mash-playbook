<!--
SPDX-FileCopyrightText: 2026 Slavi Pantaleev

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Working on MASH

This playbook consumes separately maintained Ansible roles.
For playbook configuration, edit the components under `components/` (one directory per role).
Follow [developer documentation](docs/developer-documentation.md) for generated files and checks.
Roles own their configuration validation in `tasks/validate_config.yml`.
For role bumps, check the affected wiring, especially the role's component (`components/<role>/`)
and the `with/<role>.yml` files of other components: setting a variable the role renamed or removed
has no effect, and nothing reports it.
If the role handles its configuration changes, the playbook wiring and existing docs remain valid,
and none of the changelog criteria below apply, the version pin alone is usually enough.
Defer a role bump when a supported installation path needs an upstream ref or artifact that is
missing or broken, such as a Git tag that a self-build checks out or an image architecture.
Do not keep release-specific fallbacks (commit pins, `if version == '...'` conditionals, temporary
overrides) in component wiring, unless the update fixes a security issue users should not wait for.
Keep service docs (`components/<role>/README.md`) focused on current configuration and lasting procedures.
Do not use service pages as another changelog for role releases.
Correct stale playbook examples, but leave role-specific option details in the role's documentation.

## Changelog

Use `CHANGELOG.md` for removed services, shared playbook behavior changes, or role bumps where
rerunning the playbook would break a service, lose data or weaken security in a default or documented
setup, and the role neither handles it nor fails with an actionable error.
Upstream's own upgrade steps (extension updates, reindexing, changes to user-created data or queries)
do not qualify by themselves. They belong in upstream's or the role's docs.
For a role bump, upstream application behavior alone does not warrant a playbook entry, even
when disruptive or absent from role validation. Missing validation alone is not a reason for
an entry. Explain narrower upstream risks and link release notes in the pull request instead.
State who is affected and what they need to do when adding an entry, and explain why it meets
this scope. For a role bump, say whether role validation already gives affected users an
actionable error.

Skip entries for routine service additions: document them in `docs/supported-services.md` and
the component's `README.md` instead. Adding a service alone does not warrant a changelog entry.
Skip entries for routine role bumps and for one role's renamed or removed variables or formats
when the affected role's `tasks/validate_config.yml` gives users an actionable error.
Correct stale service docs or examples. An upstream “breaking change” label alone does not
require a playbook changelog entry.
