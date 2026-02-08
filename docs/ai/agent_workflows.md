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
