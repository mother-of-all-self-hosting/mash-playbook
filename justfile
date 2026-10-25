# SPDX-FileCopyrightText: 2023 - 2024 Aine
# SPDX-FileCopyrightText: 2023 - 2026 Slavi Pantaleev
# SPDX-FileCopyrightText: 2025 Guillaume MASSON
# SPDX-FileCopyrightText: 2025 Suguru Hirahara
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# Set inventory from $ANSIBLE_INVENTORY if set, otherwise set the default
inventory := env("ANSIBLE_INVENTORY", "inventory/hosts")

# mise (dev tool version manager)
mise_data_dir := env("MISE_DATA_DIR", justfile_directory() / "var/mise")
mise_trusted_config_paths := justfile_directory() / "mise.toml"
prek_home := env("PREK_HOME", justfile_directory() / "var/prek")

# Shows help
default:
    @{{ just_executable() }} --list --justfile {{ justfile() }}

# Adds a new host to the inventory, creating the inventory files if necessary (e.g. `just add-inventory-host mash.example.com 1.2.3.4`)
add-inventory-host host server_address:
    @{{ justfile_directory() }}/bin/add-inventory-host.sh {{ quote(host) }} {{ quote(server_address) }}

run_directory_path := justfile_directory() + "/run"
components_directory_path := justfile_directory() + "/components"
# Optimization is enabled, unless this file exists
optimization_disabled_file_path := run_directory_path + "/optimization-disabled"
# Versions and checksums of the roles installed into roles/galaxy, for detecting local changes to them
installed_roles_file_path := run_directory_path + "/installed-roles.yml"

# Pulls external Ansible roles (--force also replaces roles with local changes)
roles *flags: _prepare-files
    @echo "[NOTE] This command just updates the roles, but if you want to update everything at once (playbook, roles, etc.) - use 'just update'"
    @{{ just_executable() }} --justfile {{ justfile() }} _install-roles {{ flags }}

# Makes the playbook include only the roles of enabled services (the default)
optimize-enable:
    #!/usr/bin/env sh
    set -eu
    rm -f {{ quote(optimization_disabled_file_path) }}
    {{ just_executable() }} --justfile {{ justfile() }} _prepare-files

# Makes the playbook include all roles
optimize-disable:
    #!/usr/bin/env sh
    set -eu
    mkdir -p {{ quote(run_directory_path) }}
    touch {{ quote(optimization_disabled_file_path) }}
    {{ just_executable() }} --justfile {{ justfile() }} _prepare-files

# Updates the playbook and installs the necessary Ansible roles pinned in requirements.yml. If a -u flag is passed, also updates the requirements.yml file with new role versions (if available)
update *flags:
    #!/usr/bin/env sh
    set -eu
    if [ -n "{{ flags }}" ] && [ "{{ flags }}" != "-u" ]; then
        echo "Unknown flags passed: {{ flags }}" >&2
        exit 1
    fi
    if [ "{{ flags }}" = "-u" ]; then
        # Older versions of agru only take one requirements file (-r), and would ignore all others
        agru_version=$(agru -v 2>/dev/null | sed 's/^v//' || true)
        if [ "$(printf '%s\n' 0.3.0 "$agru_version" | sort -V | head -n 1)" != "0.3.0" ]; then
            echo "Updating role versions (-u) requires the agru tool, version 0.3.0 or newer: https://github.com/etkecc/agru#where-to-get" >&2
            exit 1
        fi
    fi

    {{ just_executable() }} --justfile {{ justfile() }} update-playbook-only

    if [ "{{ flags }}" = "-u" ]; then
        # Only updates the versions pinned in each component's requirements.yml. The roles are installed below.
        echo "Pinning new role versions in components/*/requirements.yml..."
        set --
        for requirements_path in {{ components_directory_path }}/*/requirements.yml; do
            set -- "$@" -r "$requirements_path"
        done
        agru "$@" -p roles/galaxy/ -no-tui -i=false -u
        {{ just_executable() }} --justfile {{ justfile() }} versions
        {{ just_executable() }} --justfile {{ justfile() }} opml
    fi

    # Run these now, after the playbook update, so they use its new components (and justfile)
    {{ just_executable() }} --justfile {{ justfile() }} _prepare-files
    {{ just_executable() }} --justfile {{ justfile() }} _install-roles

# Updates the playbook without installing/updating Ansible roles
update-playbook-only:
    @echo "Updating playbook..."
    @git pull -q --ff-only

# Invokes mise with the project-local data directory
mise *args: _ensure_mise_data_directory
    #!/bin/sh
    export MISE_DATA_DIR="{{ mise_data_dir }}"
    export MISE_TRUSTED_CONFIG_PATHS="{{ mise_trusted_config_paths }}"
    export MISE_YES=1
    export PREK_HOME="{{ prek_home }}"
    mise {{ args }}

# Runs prek (pre-commit hooks manager) with the given arguments
prek *args: _ensure_mise_tools_installed
    @{{ just_executable() }} --justfile {{ justfile() }} mise exec -- prek {{ args }}

# Runs pre-commit hooks on staged files
prek-run-on-staged *args: _ensure_mise_tools_installed
    @{{ just_executable() }} --justfile {{ justfile() }} prek run {{ args }}

# Runs pre-commit hooks on all files
prek-run-on-all *args: _ensure_mise_tools_installed
    @{{ just_executable() }} --justfile {{ justfile() }} prek run --all-files {{ args }}

# Installs the git pre-commit hook
prek-install-git-pre-commit-hook: _ensure_mise_tools_installed
    #!/usr/bin/env sh
    set -eu
    {{ just_executable() }} --justfile {{ justfile() }} mise exec -- prek install
    # The installed git hooks run later under Git, outside this just/mise environment,
    # so they need to be told how to find their tooling:
    #
    # - PREK_HOME keeps prek's cache under var/prek instead of a global home dir.
    # - MISE_DATA_DIR / MISE_TRUSTED_CONFIG_PATHS make mise resolve against this project's
    #   own data directory. Without them mise falls back to the global one and silently
    #   installs a second copy of the tool there.
    # - prek bakes the full path of the currently installed version into the hook
    #   (var/mise/installs/prek/<version>/...), which stops working as soon as the pinned
    #   version changes or old versions are pruned. Pointing at mise's shim instead makes
    #   the hook resolve whatever mise.toml pins, at the time it runs.
    #
    # Which hook files prek installs depends on `default_install_hook_types` in
    # .pre-commit-config.yaml, so patch every hook file that prek generated.
    for hook in "{{ justfile_directory() }}"/.git/hooks/*; do
        [ -f "$hook" ] || continue
        grep -q 'generated by prek' "$hook" || continue
        grep -q '^export PREK_HOME=' "$hook" || sed -i '2iexport PREK_HOME="{{ prek_home }}"' "$hook"
        grep -q '^export MISE_DATA_DIR=' "$hook" || sed -i '3iexport MISE_DATA_DIR="{{ mise_data_dir }}"' "$hook"
        grep -q '^export MISE_TRUSTED_CONFIG_PATHS=' "$hook" || sed -i '4iexport MISE_TRUSTED_CONFIG_PATHS="{{ mise_trusted_config_paths }}"' "$hook"
        sed -i 's#^PREK=".*"$#PREK="{{ mise_data_dir }}/shims/prek"#' "$hook"
    done

# dumps an OPML file with extracted git feeds for roles
opml:
    @echo "generating opml..."
    @{{ justfile_directory() }}/bin/ansible-python.sh bin/feeds.py . dump

# dumps versions of the components found in the roles to the VERSIONS.md file
versions:
    @echo "generating versions..."
    @{{ justfile_directory() }}/bin/ansible-python.sh bin/versions.py

# Runs the playbook with --tags=install-all,start and optional arguments
install-all *extra_args: (run-tags "install-all,start" extra_args)

# Runs installation tasks for a single service
install-service service *extra_args:
    {{ just_executable() }} --justfile {{ justfile() }} run \
    --tags=install-{{ service }},start-group \
    --extra-vars=group={{ service }} {{ extra_args }}

# Runs the playbook with --tags=setup-all,start and optional arguments
setup-all *extra_args: (run-tags "setup-all,start" extra_args)

# Runs setup tasks for a single service
setup-service service *extra_args:
    {{ just_executable() }} --justfile {{ justfile() }} run \
    --tags=setup-{{ service }},start-group \
    --extra-vars=group={{ service }} {{ extra_args }}

# Runs the playbook with the given list of arguments
run +extra_args: _prepare-files (_install-roles "--quiet")
    #!/usr/bin/env sh
    set -eu
    if ! [ -x "$(command -v etkepass)" ]; then
        ansible-playbook -i {{ inventory }} setup.yml {{ extra_args }}
        exit $?
    fi
    export SSH_ASKPASS="$(command -v etkepass)"
    export SSH_ASKPASS_REQUIRE=force
    _tmpdir="$(mktemp -d)"
    chmod 700 "$_tmpdir"
    trap 'rm -rf "$_tmpdir"' EXIT INT TERM HUP
    _limit=""
    set -- {{ extra_args }}
    while [ $# -gt 0 ]; do
        case "$1" in
            -l|--limit) _limit="${2:-}" ;;
            -l=*|--limit=*) _limit="${1#*=}" ;;
            -l?*) _limit="${1#-l}" ;;
        esac
        shift
    done
    _dhosts=""
    _oldifs=$IFS; IFS=,
    for _h in $_limit; do
        [ -e "inventory/host_vars/$_h" ] && _dhosts="${_dhosts:+$_dhosts,}$_h"
    done
    IFS=$_oldifs
    if [ -n "$_dhosts" ]; then
        (cd inventory && etkepass -l "$_dhosts" --decrypt-inv-to "$_tmpdir")
    fi
    ansible-playbook -i {{ inventory }} -i "$_tmpdir" setup.yml {{ extra_args }}

# Runs the playbook with the given list of comma-separated tags and optional arguments
run-tags tags *extra_args:
    {{ just_executable() }} --justfile {{ justfile() }} run --tags={{ tags }} {{ extra_args }}

# Starts all services
start-all *extra_args: (run-tags "start-all" extra_args)

# Starts a specific service group
start-group group *extra_args:
    @{{ just_executable() }} --justfile {{ justfile() }} run-tags start-group --extra-vars="group={{ group }}" {{ extra_args }}

# Stops all services
stop-all *extra_args: (run-tags "stop-all" extra_args)

# Stops a specific service group
stop-group group *extra_args:
    @{{ just_executable() }} --justfile {{ justfile() }} run-tags stop-group --extra-vars="group={{ group }}" {{ extra_args }}

# Installs the roles in requirements.yml and deletes unused ones, keeping roles with local changes
_install-roles *flags:
    #!/usr/bin/env sh
    set -eu
    # The inventory may be a directory or a hosts file inside it
    inventory_path={{ quote(inventory) }}
    if [ ! -d "$inventory_path" ]; then
        inventory_path=$(dirname "$inventory_path")
    fi

    # All roles the playbook and the inventory's components know about: installed ones which are no longer in use get deleted
    set --
    for requirements_path in {{ components_directory_path }}/*/requirements.yml "$inventory_path"/components/*/requirements.yml; do
        if [ -f "$requirements_path" ]; then
            set -- "$@" --all-requirements-path="$requirements_path"
        fi
    done
    {{ justfile_directory() }}/bin/ansible-python.sh {{ justfile_directory() }}/bin/install-roles.py \
    --requirements-path={{ justfile_directory() }}/requirements.yml \
    "$@" \
    --roles-path={{ justfile_directory() }}/roles/galaxy \
    --state-path={{ quote(installed_roles_file_path) }} \
    {{ flags }}

# Generates requirements.yml, setup.yml and group_vars/mash_servers/ from components/ (optimized, unless optimization is disabled).
# This runs before every playbook run, so they always match the components and the inventory. Unchanged files are left as they are.
_prepare-files:
    #!/usr/bin/env sh
    set -eu
    # Left over from older versions, which only regenerated these files when the templates changed,
    # and only optimized when enabled with these markers
    rm -f {{ run_directory_path }}/*.srchash
    rm -f {{ quote(run_directory_path / "optimization-enabled") }} {{ quote(run_directory_path / "optimization-vars-files.state") }}

    if [ -f {{ quote(optimization_disabled_file_path) }} ]; then
        {{ just_executable() }} --justfile {{ justfile() }} _optimize-files --all-components
    else
        {{ just_executable() }} --justfile {{ justfile() }} _optimize-files
    fi

# Generates requirements.yml, setup.yml and group_vars/mash_servers/ with the components in use by the inventory
# (or all of them, with --all-components). If this fails, none of them is changed.
_optimize-files *flags:
    #!/usr/bin/env sh
    set -eu
    # The inventory may be a directory or a hosts file inside it
    inventory_path={{ quote(inventory) }}
    if [ ! -d "$inventory_path" ]; then
        inventory_path=$(dirname "$inventory_path")
    fi

    {{ justfile_directory() }}/bin/ansible-python.sh {{ justfile_directory() }}/bin/optimize.py \
    --components-path={{ components_directory_path }} \
    --inventory-path="$inventory_path" \
    --playbook-path={{ justfile_directory() }} \
    --dst-requirements-yml-path={{ justfile_directory() }}/requirements.yml \
    --dst-setup-yml-path={{ justfile_directory() }}/setup.yml \
    --dst-group-vars-path={{ justfile_directory() }}/group_vars/mash_servers \
    {{ flags }}

# Internal - ensures var/mise and var/prek directories exist
_ensure_mise_data_directory:
    @mkdir -p "{{ mise_data_dir }}"
    @mkdir -p "{{ prek_home }}"

# Internal - ensures mise tools are installed
_ensure_mise_tools_installed: _ensure_mise_data_directory
    @{{ just_executable() }} --justfile {{ justfile() }} mise install --quiet
