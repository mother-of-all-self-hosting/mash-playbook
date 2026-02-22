<!--
SPDX-FileCopyrightText: 2026 MASH project contributors

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Support Documentation Contract

This directory is the canonical support layer for agent/operator collaboration.

## Purpose

- Define execution and safety rules for automation-assisted maintenance.
- Provide runbooks that agents can reference without inventing workflow details.
- Keep cross-repo behavior consistent between MASH and MDAD where possible.

## Source of truth

- `AGENTS.md` - repository policy guardrails and allowed behavior.
- `docs/ai/agent_workflows.md` - implementation/reporting workflow details.
- `docs/ai/vault-operations.md` - human-run vault workflow and secret-safe output rules.

## Relation to top-level docs

Top-level docs remain user/operator product documentation (for example:
`docs/installing.md`, `docs/just.md`, `docs/playbook-tags.md`,
`docs/uninstalling.md`).

Use `docs/ai/*` for support-process behavior and command construction; use
top-level docs for service/playbook semantics.

## Maintenance rule

Non-repository-specific support rules should remain text-identical across MASH
and MDAD. Divergence should be limited to real structural differences.
