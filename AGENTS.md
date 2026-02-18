<!--
SPDX-FileCopyrightText: 2026 MASH project contributors

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# AGENTS.md - mash-playbook

## Purpose

This repository is usually operated by pulling upstream updates and maintaining
local deployment configuration.

Default assumption:

- Work in operator mode unless the user explicitly asks for contribution/PR
  work.

## Modes

### Operator mode (default)

- Goal: maintain a local deployment.
- Default editable paths are defined in `Operator-owned local paths`.

### Contributor mode (explicit opt-in)

- Goal: make upstream-facing playbook/docs/code changes.
- Upstream-tracked files may be edited, but branch and safety rules below apply.

### Contributor mode activation (explicit)

Contributor mode is enabled only when the user:

- explicitly asks for contributor mode, PR work, or upstream-facing changes
- or explicitly requests edits to upstream-tracked files and confirms upstream
  intent

If the user asks to edit a non-operator-owned path without this intent:

- ask one clarification question
- do not proceed with upstream-tracked edits until clarified

## Operator-owned local paths (default editable without extra permission)

Operator mode may edit these paths by default:

- `inventory/**`
- `docs/mash/**` (local operator documentation)
- `docs/ai/**` (agent workflow docs)
- `.codex/**` (Codex config/skills, if present)
- `plans/**` (execution plans, if used)
- `AGENTS.md`
- Operator mode may create missing files/directories under operator-owned local
  paths as needed.

All other paths are read-only in operator mode unless the user explicitly
requests edits or opts into contributor mode.

## Planning protocol

- Workflow contract: gather -> plan -> apply -> verify.
- Use structured planning only when required by `Planning threshold`.
- Planning templates and reporting format: `docs/ai/agent_workflows.md`.
- Do not execute destructive or broad remote-impact actions before prerequisite
  planning items are complete.

## Planning threshold

Structured plan REQUIRED for:

- managed-node-impacting actions (including proposed execution)
- destructive/disruptive/retention-risk changes
- edits outside operator-owned local paths
- changes touching multiple subsystems/services
- multi-deliverable requests

Mini-plan (brief bullets) is sufficient for:

- read-only analysis
- edits confined to operator-owned local paths
- small local edits with no managed-node impact or retention risk

## Upstream ownership model

- MUST NOT use `origin` to decide whether a file is upstream-owned.
- MUST use the `upstream` remote as the source of truth.
- `upstream-tracked file` means a path that exists in
  `upstream/<default-branch>`.
- If `upstream` is unavailable, treat files outside operator-owned paths as
  upstream-tracked.

## Upstream detection procedure (deterministic, offline-first)

- Prefer read-only discovery first; ask at most one clarification question only
  if blocked.

1. Determine upstream default branch (offline):
   - `git symbolic-ref --quiet --short refs/remotes/upstream/HEAD` (derive
     `<upstream_default_branch>` by stripping `upstream/`)
2. Check whether a path exists in upstream (offline):
   - `git cat-file -e "upstream/<upstream_default_branch>:<path>"`
3. If `refs/remotes/upstream/HEAD` is missing:
   - if user confirms network operations, run `git fetch --prune upstream` and
     retry
   - otherwise treat paths outside operator-owned local paths as
     upstream-tracked
4. For new paths:
   - treat new files outside operator-owned local paths as upstream-tracked
     unless contributor mode is active

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

For contributor work that changes playbook wiring, edit source files under
`templates/**`.

## Local filesystem impact policy

- Default writable scope is this repository working tree plus `/tmp` for
  transient files.
- `Writable scope` defines where the agent may write at all.
- `Operator-owned local paths` defines what may be edited by default in operator
  mode.
- MUST NOT write outside this repository or `/tmp` without explicit user
  confirmation in the same turn.
- MUST NOT modify controller system state unless explicitly requested:
- shell profiles
- SSH client/server config
- package installation/removal
- system services
- scheduled jobs (cron/systemd timers)
- Put transient artifacts under `/tmp/mash-playbook-agent-*`.
- Remove transient artifacts before finishing unless the user asks to keep them.
- Editing `inventory/**` is a latent remote change: managed-node state is
  unchanged until a playbook command is executed.

## Managed-node impact policy

- Classify each executed or proposed command as one of:
- `read-only`
- `state-changing`
- `disruptive`
- `destructive`
- MUST require explicit user confirmation before executing any `state-changing`,
  `disruptive`, or `destructive` managed-node action.
- Default to minimum blast radius:
- prefer `--limit`
- prefer specific tags/services/groups
- avoid broad all-services runs when narrower scope is feasible
- `destructive` actions MUST require explicit user request and a backup/rollback
  plan before execution.
- After managed-node changes, report:
- exact command executed
- target/scope
- concise result
- verification commands
- rollback command or path

## Data deletion, retention, and deactivation safety

- Retention guard: Do not run `setup-all`/`setup-*` for temporary deactivation;
  treat as potentially uninstalling. Only run with explicit uninstall intent
  plus backup/rollback plan.
- Treat disable/uninstall toggles, identifier/path changes, and cleanup/prune
  actions as retention-risky; consult `docs/mash/retention.md`.
- Any destructive operation requires explicit deletion consent and a
  backup/rollback plan before execution.
- If retention behavior is unclear, mark `UNKNOWN` and require explicit user
  decision before proceeding.
- Service-specific retention guidance: `docs/mash/retention.md`.

## Command safety policy

Safe without extra confirmation:

- local read/discovery commands and local lint/syntax checks
- local-only `ansible-playbook` inspection commands (for example
  `--syntax-check`, `--list-tags`, `--list-tasks`) only when they do not
  require remote host connection, Vault unlock, or become/sudo

MUST require explicit user confirmation in the same turn for:

- any managed-node `state-changing`, `disruptive`, or `destructive` action
- any remote-impact `ansible-playbook`/`just` execution (except pure
  syntax-check)
- local update/mutation commands that change repository state (`git pull`, role
  updates)

Before confirmed remote-impact commands, state target host/group, scope, and
expected service impact.

- Human-run-only operations (defined below) are never agent-executable, even if
  confirmation is given.
- If unsure, treat as managed-node-impacting and do read-only discovery first.
- Command catalogs and examples: `docs/ai/agent_workflows.md` and
  `docs/mash/service_enablement.md`.

## Human-run-only operations (non-overridable)

- Agents MUST NOT read, decrypt, diff, edit, or re-encrypt vault files (for
  example `inventory/**/vault.yml`, `*vault*.yml`) and MUST NOT run
  `ansible-vault` commands.
- Agents MUST NOT execute commands that rely on SSH or remote host access (for
  example `ssh`, `scp`, `rsync`, `ansible-playbook` remote runs, `just run*` /
  `just install*` / `just setup*` / `just start*` against managed hosts).
- Agents MUST NOT execute commands that require sudo/become privileges.
- For human-run-only operations, agents prepare command blocks with scope,
  impact, verification, and rollback guidance; the human operator executes them
  manually.
- Local-only `ansible-playbook` commands remain allowed for the agent only if
  they satisfy all of: no remote host connection, no Vault unlock, and no
  become/sudo.
- This section overrides less-restrictive guidance elsewhere in this repository.

## Interactive credentials and execution limits

- Assume SSH authentication material, Vault password, and become password are
  user-supplied and unavailable to the agent by default.
- MUST NOT bypass credential prompts by storing plaintext passwords, modifying
  SSH/sudo config, or weakening security controls.
- Credential-interactive and human-run-only operations must always be provided
  as user-run command blocks, never executed by the agent.
- Before remote-impact execution, report credential mode for SSH auth, Vault
  unlock, and privilege escalation.
- Workarounds: user runs commands interactively, or user configures
  non-interactive auth and confirms readiness.

## Command suggestion safety

- For suggested (non-executed) commands, include impact, data-retention
  expectation, verification, and rollback notes.
- Detailed annotation template: `docs/ai/agent_workflows.md`.

## Evidence rule

- MUST NOT guess variable names, tags, paths, identifiers, or service names.
- MUST cite exact repository file paths for behavior claims.
- If unresolved, mark `UNKNOWN` and provide exact `rg` commands to resolve.

## Secrets handling

Treat these as sensitive:

- `inventory/host_vars/**`
- `group_vars/**` (and `inventory/group_vars/**`, if present)
- `inventory/hosts`
- vault files and secret-bearing variables

Rules:

- MUST NOT print raw secrets in output by default.
- Redact tokens/passwords/keys in summaries and diffs unless user explicitly
  requests raw values.

### Secret-safe output policy

For secret-bearing files:

- default output must be summary plus `git diff --stat`
- MUST NOT print inline diff hunks by default
- if the user requests details, redact values as `<REDACTED>` unless the user
  explicitly requests raw values

## Validation and linting

- Always run at least one relevant local validation command before concluding
  work.
- Primary lint command for this repository: `bash ./bin/lint-playbook.sh` (run
  from repository root).
- If unavailable, use the most specific feasible fallback (`just lint` or
  `ansible-playbook ... --syntax-check`).
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

## Pointers (may be created as needed)

- `docs/mash/overview.md`
- `docs/mash/service_enablement.md`
- `docs/mash/authentik_patterns.md`
- `docs/mash/retention.md`
- `docs/ai/agent_workflows.md`
