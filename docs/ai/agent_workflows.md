# Agent Workflows

## Grounding Before Proposing Changes

- Do not propose editing a specific inventory file until read-only search confirms variable location.
- If location is unresolved, mark `UNKNOWN` and propose a conditional plan (locate -> then edit).
- Use conditional language until confirmed (for example: "If found in X, edit X; else search Y").

## Grounding Just Commands

- Before suggesting `just` with flags, verify recipe interface in `justfile`.
- Use `just --list` and inspect recipe definitions/arg forwarding.
- Do not assume `--ask-vault-pass -K --limit` passthrough.
- If uncertain, suggest explicit `ansible-playbook` user-run command with required flags.

## Verification Grounding

- Prefer repo-defined status/verify commands first.
- If service identifiers are unknown, discover them first.
- Use `docker`/`systemctl` checks only when evidence supports that runtime path.

### Read-Only Discovery Primitives

- `just --list`
- `rg -n "<service>" justfile docs inventory roles templates`
- `rg -n "<varname>" inventory/host_vars inventory/group_vars group_vars`
- `rg -n "stop-group|start-group|status" justfile`

## Secrets and Vault Grounding

- Variables loaded from vault must be referenced with names prefixed by `vault_` (for example: `some_secret: "{{ vault_some_secret }}"`).
- Before proposing vault-backed variables, verify existing naming patterns in `inventory/host_vars/**/vars.yml`.
- For cross-host secrets (for example, service + dependency host), explicitly note when the same vault value must be reused.

## Multi-Host Dependency Pattern Grounding

- When a service is modeled with a dedicated dependency host (for example `*-immich-deps`), verify:
- inventory host entry exists in `inventory/hosts`
- supplementary host vars path exists in `inventory/host_vars/<host>/vars.yml`
- main host wiring variables point to dependency host identifiers/networks/services
- If any of the above is unresolved, mark `UNKNOWN` and provide exact `rg` commands.

## Retention and Uninstall Grounding

- Distinguish temporary deactivation from uninstall intent:
- temporary deactivation: prefer `stop-group` / `start-group` flow
- uninstall/cleanup intent: use service-scoped `setup-<service>` path when evidence shows uninstall tasks are wired there
- Do not default to broad `setup-all` for single-service uninstall unless explicitly requested.
- For services with data directories or migrations, cite uninstall tasks and data-path behavior (delete vs keep vs unknown).

## Remote-Impact Command Annotation

- For any suggested remote-impact command, mark it as `user-run only` unless the user explicitly asks the agent to execute it.
- Always include:
- target host/limit scope
- expected impact (`state-changing` / `disruptive` / `destructive`)
- retention expectation (`keep` / `delete` / `unknown`)
- verification command(s)
- rollback direction

## Markdown Linting

- Markdown files should be linted locally after edits.
- Use the repository lint script: `bash ./bin/lint-playbook.sh`
- To include markdown files explicitly, pass them via `EXTRA_LINT_PATHS`.
- Example: `EXTRA_LINT_PATHS="docs/ai/agent_workflows.md" bash ./bin/lint-playbook.sh`
