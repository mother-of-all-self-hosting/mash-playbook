#!/usr/bin/env bash
set -euo pipefail

log() {
  echo "[lint-playbook] $*"
}

repo_root=$(git -C "${PWD}" rev-parse --show-toplevel 2>/dev/null || true)
if [[ -z "${repo_root}" ]]; then
  log "error: run this script inside a git repository."
  exit 1
fi

cd "${repo_root}"

if [[ -f group_vars/mash_servers ]]; then
  playbook="mash"
elif [[ -f group_vars/matrix_servers ]]; then
  playbook="matrix"
else
  log "error: unable to detect playbook type (expected group_vars/mash_servers or group_vars/matrix_servers)."
  exit 1
fi

log "detected ${playbook^^} playbook at ${repo_root}"

git_branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || true)
git_commit=$(git rev-parse --short HEAD 2>/dev/null || true)
if [[ -n "${git_branch}" && -n "${git_commit}" ]]; then
  log "git branch: ${git_branch} (${git_commit})"
else
  log "warning: unable to determine git branch/commit."
fi

lint_scope="${LINT_PLAYBOOK_SCOPE:-scoped}"
case "${lint_scope}" in
  scoped|full)
    ;;
  *)
    log "error: invalid LINT_PLAYBOOK_SCOPE='${lint_scope}'. Use 'scoped' or 'full'."
    exit 1
    ;;
esac
log "lint scope: ${lint_scope}"

python_bin="${PYTHON:-python3}"
venv_path="${LINT_PLAYBOOK_VENV:-${repo_root}/.venv}"

log "using Python interpreter: ${python_bin}"
log "desired virtualenv location: ${venv_path}"

python_cmd=$(command -v "${python_bin}" || true)
if [[ -z "${python_cmd}" ]]; then
  log "error: ${python_bin} is not available in PATH."
  exit 1
fi

if [[ ! -d "${venv_path}" ]]; then
  log "virtualenv missing, creating a new one..."
  "${python_cmd}" -m venv "${venv_path}"
else
  log "virtualenv already exists, reusing current installation."
fi

# If the venv is corrupted (missing activate), rebuild it.
if [[ ! -f "${venv_path}/bin/activate" ]]; then
  log "virtualenv missing activation script; rebuilding..."
  "${python_cmd}" -m venv --clear "${venv_path}"
fi

# shellcheck disable=SC1090,SC1091
source "${venv_path}/bin/activate"
log "virtualenv activated: ${venv_path}"

venv_python="${venv_path}/bin/python"

if ! "${venv_python}" - <<'PY' >/dev/null 2>&1; then
import pip  # noqa: F401
PY
  log "pip missing inside virtualenv; bootstrapping with ensurepip..."
  if ! "${venv_python}" -m ensurepip --upgrade >/dev/null 2>&1; then
    log "ensurepip unavailable in virtualenv; rebuilding virtualenv..."
    deactivate || true
    "${python_cmd}" -m venv --clear "${venv_path}"
    # shellcheck disable=SC1090,SC1091
    source "${venv_path}/bin/activate"
    venv_python="${venv_path}/bin/python"
    if ! "${venv_python}" - <<'PY' >/dev/null 2>&1; then
import pip  # noqa: F401
PY
      log "error: pip still unavailable. Install Python ensurepip/venv support and re-run."
      deactivate || true
      exit 1
    fi
  fi
fi

log "updating pip/setuptools/wheel..."
"${venv_python}" -m pip install --upgrade pip setuptools wheel >/dev/null

log "ensuring ansible-core, ansible-lint, and pre-commit are current..."
"${venv_python}" -m pip install --upgrade ansible-core ansible-lint pre-commit >/dev/null

gather_targets() {
  local mode=$1
  local -a paths=()

  if [[ -d inventory/host_vars ]]; then
    while IFS= read -r file; do
      paths+=("${file}")
    done < <(find inventory/host_vars -maxdepth 2 -type f \
      \( -name 'vars.yml' -o -name 'vars.yaml' \) \
      ! -name '*.bak' ! -path '*_bak/*' \
      ! -name 'vault*.yml' ! -name 'vault*.yaml' \
      | sort)
  fi
  if [[ -d inventory/host_vars/domain-nextcloud-deps ]]; then
    while IFS= read -r file; do
      paths+=("${file}")
    done < <(find inventory/host_vars/domain-nextcloud-deps -maxdepth 1 -type f \
      ! -name '*.bak' ! -path '*_bak/*' \
      ! -name 'vault*.yml' ! -name 'vault*.yaml' \
      | sort)
  fi

  case "${mode}" in
    mash)
      [[ -f inventory/hosts ]] && paths+=("inventory/hosts")
      [[ -f group_vars/mash_servers ]] && paths+=("group_vars/mash_servers")
      ;;
    matrix)
      [[ -f inventory/hosts ]] && paths+=("inventory/hosts")
      [[ -f group_vars/matrix_servers ]] && paths+=("group_vars/matrix_servers")
      if [[ "${lint_scope}" == "full" ]]; then
        [[ -f group_vars/jitsi_jvb_servers ]] && paths+=("group_vars/jitsi_jvb_servers")
        [[ -f jitsi_jvb.yml ]] && paths+=("jitsi_jvb.yml")
      fi
      ;;
  esac

  if [[ -n "${EXTRA_LINT_PATHS:-}" ]]; then
    for extra in ${EXTRA_LINT_PATHS}; do
      if [[ -e "${extra}" ]]; then
        paths+=("${extra}")
      else
        log "note: EXTRA_LINT_PATH ${extra} skipped (not found)."
      fi
    done
  fi

  printf '%s\n' "${paths[@]}" | sort -u | grep -Ev '(^|/)(\.venv|venv)(/|$)' || true
}

mapfile -t relevant_files < <(gather_targets "${playbook}")

if [[ ${#relevant_files[@]} -eq 0 ]]; then
  log "no relevant files detected; nothing to lint."
  deactivate
  exit 0
fi

log "lint target list (${#relevant_files[@]} files):"
printf '  - %s\n' "${relevant_files[@]}"

log "running pre-commit on filtered list..."
pre-commit run --files "${relevant_files[@]}"

mapfile -t ansible_targets < <(printf '%s\n' "${relevant_files[@]}" | grep -E '\.(yml|yaml)$' || true)
if [[ ${#ansible_targets[@]} -gt 0 ]]; then
  log "running ansible-lint on YAML files..."
  ansible-lint "${ansible_targets[@]}"
else
  log "skipping ansible-lint (no YAML files in target list)."
fi

role_targets=()
if [[ "${lint_scope}" == "full" && -d roles/custom ]]; then
  role_targets+=("roles/custom")
fi
if [[ -n "${LINT_PLAYBOOK_ROLE_PATHS:-}" ]]; then
  for role_path in ${LINT_PLAYBOOK_ROLE_PATHS}; do
    if [[ -e "${role_path}" ]]; then
      role_targets+=("${role_path}")
    else
      log "note: LINT_PLAYBOOK_ROLE_PATH ${role_path} skipped (not found)."
    fi
  done
fi
if [[ ${#role_targets[@]} -gt 0 ]]; then
  mapfile -t unique_role_targets < <(printf '%s\n' "${role_targets[@]}" | sort -u)
  log "running ansible-lint on role paths: ${unique_role_targets[*]}"
  ansible-lint "${unique_role_targets[@]}"
else
  log "no additional role directories selected for linting."
fi

if [[ "${LINT_PLAYBOOK_RUN_JUST:-0}" == "1" ]]; then
  if command -v just >/dev/null 2>&1; then
    log "running 'just lint' per request (this scans the entire repo)."
    just lint
  else
    log "skipping 'just lint'; executable not found."
  fi
else
  log "skipping 'just lint' (set LINT_PLAYBOOK_RUN_JUST=1 to enable)."
fi

deactivate
log "virtualenv deactivated."
