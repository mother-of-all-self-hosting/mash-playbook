<!--
SPDX-FileCopyrightText: 2026 MASH project contributors

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Vault Operations

## Scope

This runbook defines how vault-backed variables are planned and validated while
keeping secret material human-operated.

## Non-overridable boundaries

- Agents must not read, decrypt, diff, edit, or re-encrypt vault files.
- Agents must not run `ansible-vault` commands.
- Vault editing and decryption are always operator-run actions.

## Variable naming rules

- Secret values referenced from `vars.yml` must use `vault_*` names.
- Keep booleans and non-secret control flags in `vars.yml`.
- Keep credentials, tokens, passwords, and private keys in vault files.

## Operator runbook template

1. Identify required vault keys from non-secret inventory files:
   `rg -n "vault_[a-zA-Z0-9_]+" inventory/host_vars/<host>/vars.yml`
2. Add/update values in the host vault file (operator-run):
   `ansible-vault edit inventory/host_vars/<host>/vault.yml`
3. Ensure non-secret files reference vault keys (no plaintext secret literals in
   `vars.yml`).
4. Run local validation:
   `bash ./bin/lint-playbook.sh`
5. If remote execution is intended, run operator commands with credential flags:
   `--ask-vault-pass --ask-become-pass` (or `-J -K` with `ansible-playbook`).

## Secret-safe reporting

- Default reporting for secret-bearing changes should use summary plus
  `git diff --stat`.
- Do not print inline secret values unless explicitly requested.
- If details are requested, redact values as `<REDACTED>` unless raw output is
  explicitly requested.
