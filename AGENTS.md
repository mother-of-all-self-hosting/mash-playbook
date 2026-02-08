<!--
SPDX-FileCopyrightText: 2026 MASH project contributors

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# AGENTS.md - mash-playbook

## Purpose
This repository is usually operated by pulling upstream updates and maintaining local deployment configuration.

Default assumption:
- Work in operator mode unless the user explicitly asks for contribution/PR work.

## Modes
### Operator mode (default)
- Goal: maintain a local deployment.
- Editable paths:
- `inventory/**`
- Everything else is read-only unless explicitly requested by the user.

### Contributor mode (explicit opt-in)
- Goal: make upstream-facing playbook/docs/code changes.
- Upstream-tracked files may be edited, but branch and safety rules below apply.

## Planning protocol
- Use a structured plan for:
- multi-file or multi-repo changes
- any managed-node-impacting change
- any potentially destructive or retention-risk change
- any request with multiple deliverables
- Plan structure must explicitly separate:
- `Project goal` (final desired end state)
- `Milestones` (major outcomes required for the goal)
- `Tasks` (concrete units within each milestone)
- `Subtasks` (smallest actionable steps as needed)
- For each milestone, define:
- `Definition of done`
- `Validation` command(s) or check(s)
- key `Risks` / `Assumptions`
- Execution discipline:
- keep exactly one task/subtask `in_progress` at a time
- update statuses after each completed task/subtask
- if scope changes, publish a revised plan before continuing
- Completion reporting must state:
- whether the `Project goal` is complete
- which milestones are complete vs pending
- remaining tasks (if any)
- Do not execute destructive or broad remote-impact actions before prerequisite planning milestones are marked complete.

## Upstream ownership model
- MUST NOT use `origin` to decide whether a file is upstream-owned.
- MUST use the `upstream` remote as the source of truth.
- `upstream-tracked file` means a path that exists in `upstream/<default-branch>`.
- If `upstream` is unavailable, treat files outside operator-owned paths as upstream-tracked.

## Branch policy
- MUST NOT edit upstream-tracked files on the repository primary branch.
- If upstream-tracked edits are needed while on primary branch:
- create/switch to a dedicated branch first
- unless the user explicitly requests edits on primary branch
- Operator-owned paths can be edited on any branch.

## Non-editable or managed paths
MUST NOT edit these directly:
- `roles/galaxy/**` (vendor/fetched roles)
- `requirements.yml` (template-derived)
- `setup.yml` (template-derived)
- `group_vars/mash_servers` (template-derived)
- `run/**` (generated/state)

For contributor work that changes playbook wiring, edit source files under `templates/**`.

## Local filesystem impact policy
- Default writable scope is this repository working tree plus `/tmp` for transient files.
- MUST NOT write outside this repository or `/tmp` without explicit user confirmation in the same turn.
- MUST NOT modify controller system state unless explicitly requested:
- shell profiles
- SSH client/server config
- package installation/removal
- system services
- scheduled jobs (cron/systemd timers)
- Put transient artifacts under `/tmp/mash-playbook-agent-*`.
- Remove transient artifacts before finishing unless the user asks to keep them.
- Editing `inventory/**` is a latent remote change: managed-node state is unchanged until a playbook command is executed.

## Managed-node impact policy
- Classify each executed or proposed command as one of:
- `read-only`
- `state-changing`
- `disruptive`
- `destructive`
- MUST require explicit user confirmation before executing any `state-changing`, `disruptive`, or `destructive` managed-node action.
- Default to minimum blast radius:
- prefer `--limit`
- prefer specific tags/services/groups
- avoid broad all-services runs when narrower scope is feasible
- `destructive` actions MUST require explicit user request and a backup/rollback plan before execution.
- After managed-node changes, report:
- exact command executed
- target/scope
- concise result
- verification commands
- rollback command or path

## Data deletion, retention, and deactivation safety
- Treat the following as potential data-loss triggers:
- setting `*_enabled: false`
- removing a service/component block from `inventory/**`
- changing identifiers, base paths, database names/users, or storage paths
- changing host/group targeting in ways that detach services from previous data locations
- running `setup-all` / `setup-*` after disabling components (can run uninstallation tasks)
- running cleanup commands on managed hosts (`docker system prune`, volume/network removal, manual data-path deletion)
- If user intent is temporary deactivation, default to non-destructive stop/start workflows:
- prefer stop/start commands for the specific service/group
- do not propose uninstall-oriented apply paths unless user explicitly asks for uninstall behavior
- MUST NOT run `setup-all` or `setup-*` for temporary deactivation unless the user explicitly confirms uninstall intent in the same turn.
- Before proposing or executing any potentially destructive apply command:
- inspect relevant role uninstall tasks and retention-related variables
- if data-retention behavior is unclear, mark `UNKNOWN` and ask for explicit user decision before proceeding
- MUST require explicit deletion consent before destructive execution (for example: permanent deletion of `<service>` data is approved).
- MUST require backup and restore planning before destructive execution:
- backup target(s): database + service data paths/volumes
- restore path or command
- verification steps for backup presence
- After destructive or potentially destructive operations, verify and report data retention outcome explicitly.

## Command safety policy
Safe without extra confirmation:
- Local read/discovery commands (`rg`, `ls`, `cat`, `git status`, `git diff`, `just --list`)
- Local lint/syntax checks

MUST require explicit user confirmation in the same turn for:
- Any remote-impact Ansible run:
- `ansible-playbook ...` (except pure syntax-check)
- `just run*`
- `just install*`
- `just setup*`
- `just start*`
- `just stop*`
- Update/mutation commands:
- `just update`
- `git pull`
- `just roles`

Before confirmed remote-impact commands, state:
- target host/group
- tag/group/service scope
- expected service impact (start/stop/restart)

## Interactive credentials and execution limits
- Assume SSH authentication material, Vault password, and become password are user-supplied and unavailable to the agent by default.
- MUST NOT attempt to bypass credential prompts by creating/storing plaintext password files, modifying SSH/sudo configuration, or weakening security controls.
- For remote-impact commands that require user-supplied credentials, default to providing exact commands for the user to run instead of agent execution.
- Before any remote-impact execution attempt, confirm and report credential mode:
- SSH auth (`ssh-agent` key/passphrase, `--ask-pass`, or non-interactive configured method)
- Vault unlock (`--ask-vault-pass` or configured `vault_password_file`)
- Privilege escalation (`-K`/`--ask-become-pass`, passwordless sudo, or equivalent)
- If any required credential path is interactive and the user has not explicitly asked the agent to execute anyway, do not execute and provide a user-run command block.
- Suggested command defaults for this workspace:
- include `--ask-vault-pass -K` for `ansible-playbook` and `just` remote-impact runs unless the user confirms non-interactive alternatives are configured
- include `--ask-pass` when SSH password authentication (no key) is used
- If asked for workarounds, offer safe options:
- user runs commands interactively
- user configures non-interactive auth and explicitly confirms readiness

## Command suggestion safety
- Even when not executing commands, annotate suggested command blocks with:
- `Where` (controller vs managed node)
- `Impact` (`read-only` / `state-changing` / `disruptive` / `destructive`)
- `Data retention` (`keep` / `delete` / `unknown`)
- `Disruption` (yes/no and expected scope)
- `Verify` (how to confirm success)
- `Rollback` (how to revert)
- If commands are only suggestions and not executed, state that explicitly.

## Evidence rule
- MUST NOT guess variable names, tags, paths, identifiers, or service names.
- MUST cite exact repository file paths for behavior claims.
- If unresolved, mark `UNKNOWN` and provide exact `rg` commands to resolve.

## Secrets handling
Treat these as sensitive:
- `inventory/host_vars/**`
- `inventory/hosts`
- vault files and secret-bearing variables

Rules:
- MUST NOT print raw secrets in output by default.
- Redact tokens/passwords/keys in summaries and diffs unless user explicitly requests raw values.

## Validation and linting
- Always run at least one relevant local validation command before concluding work.
- Primary lint command for this repository: `bash ./bin/lint-playbook.sh` (run from repository root).
- If the script is unavailable, fall back to the most specific feasible check (for example `just lint`, or `ansible-playbook ... --syntax-check` when appropriate).
- If validation cannot be run, say so explicitly.

## Audit trail and commits
- Do not auto-commit by default.
- If the user requests an audit trail with commits, use small logical commits:
- one logical change per commit
- clear commit message
- no amend or force-push unless explicitly requested
- Always summarize what changed and what was validated.

## Multi-repo safety
If multiple related repos are present in the workspace:
- confirm target repo before edits or remote-impact commands.
- do not perform cross-repo edits unless explicitly requested.
