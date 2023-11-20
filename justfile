# Shows help
default:
    @just --list --justfile {{ justfile() }}

run_directory_path := justfile_directory() + "/run"
templates_directory_path := justfile_directory() + "/templates"
optimization_vars_files_file_path := run_directory_path + "/optimization-vars-files.state"

# Pulls external Ansible roles
roles: _requirements-yml
    #!/usr/bin/env sh
    if [ -x "$(command -v agru)" ]; then
        agru -r {{ justfile_directory() }}/requirements.yml
    else
        rm -rf roles/galaxy
        ansible-galaxy install -r {{ justfile_directory() }}/requirements.yml -p roles/galaxy/ --force
    fi

# Optimizes the playbook based on stored configuration (vars.yml paths)
optimize-restore:
    #!/usr/bin/env sh
    if [ -f "$optimization_vars_files_file_path" ]; then
        just --justfile {{ justfile() }} \
        _optimize-for-var-paths \
        $(cat $optimization_vars_files_file_path)
    else
        echo "Cannot restore optimization state from a file ($optimization_vars_files_file_path), because it doesn't exist"
        exit 1
    fi

# Clears optimizations and resets the playbook to a non-optimized state
optimize-reset: && _clean_template_derived_files
    #!/usr/bin/env sh
    rm -f {{ run_directory_path }}/*.srchash
    rm -f {{ optimization_vars_files_file_path }}

# Optimizes the playbook based on the enabled components for all hosts in the inventory
optimize inventory_path='inventory': _reconfigure-for-all-hosts

_reconfigure-for-all-hosts inventory_path='inventory':
    #!/usr/bin/env sh
    just --justfile {{ justfile() }} \
    _optimize-for-var-paths \
    $(find {{ inventory_path }}/host_vars/ -maxdepth 2 -name '*.yml' -exec readlink -f {} \;)

# Optimizes the playbook based on the enabled components for a single host
optimize-for-host hostname inventory_path='inventory':
    #!/usr/bin/env sh
    just --justfile {{ justfile() }} \
    _optimize-for-var-paths \
    $(find {{ inventory_path }}/host_vars/{{ hostname }} -maxdepth 1 -name '*.yml' -exec readlink -f {} \;)

# Optimizes the playbook based on the enabled components found in the given vars.yml files
_optimize-for-var-paths +PATHS:
    #!/usr/bin/env sh
    echo '{{ PATHS }}' > {{ optimization_vars_files_file_path }}

    just --justfile {{ justfile() }} _save_hash_for_file {{ templates_directory_path }}/requirements.yml {{ justfile_directory() }}/requirements.yml
    just --justfile {{ justfile() }} _save_hash_for_file {{ templates_directory_path }}/setup.yml {{ justfile_directory() }}/setup.yml
    just --justfile {{ justfile() }} _save_hash_for_file {{ templates_directory_path }}/group_vars_mash_servers {{ justfile_directory() }}/group_vars/mash_servers

    /usr/bin/env python {{ justfile_directory() }}/bin/optimize.py \
    --vars-paths='{{ PATHS }}' \
    --src-requirements-yml-path={{ templates_directory_path }}/requirements.yml \
    --dst-requirements-yml-path={{ justfile_directory() }}/requirements.yml \
    --src-setup-yml-path={{ templates_directory_path }}/setup.yml \
    --dst-setup-yml-path={{ justfile_directory() }}/setup.yml \
    --src-group-vars-yml-path={{ templates_directory_path }}/group_vars_mash_servers \
    --dst-group-vars-yml-path={{ justfile_directory() }}/group_vars/mash_servers

# Updates requirements.yml if there are any new tags available. Requires agru
update: && opml
    @agru -r {{ templates_directory_path }}/requirements.yml -u

# Runs ansible-lint against all roles in the playbook
lint:
    ansible-lint

# dumps an OPML file with extracted git feeds for roles
opml:
    @echo "generating opml..."
    @python bin/feeds.py . dump

# Runs the playbook with --tags=install-all,start and optional arguments
install-all *extra_args: (run-tags "install-all,start" extra_args)

# Runs installation tasks for a single service
install-service service *extra_args:
    just --justfile {{ justfile() }} run \
    --tags=install-{{ service }},start-group \
    --extra-vars=group={{ service }} \
    --extra-vars=devture_systemd_service_manager_service_restart_mode=one-by-one {{ extra_args }}

# Runs the playbook with --tags=setup-all,start and optional arguments
setup-all *extra_args: (run-tags "setup-all,start" extra_args)

# Runs the playbook with the given list of arguments
run +extra_args: _requirements-yml _setup-yml _group-vars-mash-servers
    ansible-playbook -i inventory/hosts setup.yml {{ extra_args }}

# Runs the playbook with the given list of comma-separated tags and optional arguments
run-tags tags *extra_args:
    just --justfile {{ justfile() }} run --tags={{ tags }} {{ extra_args }}

# Starts all services
start-all *extra_args: (run-tags "start-all" extra_args)

# Starts a specific service group
start-group group *extra_args:
    @just --justfile {{ justfile() }} run-tags start-group --extra-vars="group={{ group }}" {{ extra_args }}

# Stops all services
stop-all *extra_args: (run-tags "stop-all" extra_args)

# Stops a specific service group
stop-group group *extra_args:
    @just --justfile {{ justfile() }} run-tags stop-group --extra-vars="group={{ group }}" {{ extra_args }}

# Prepares the requirements.yml file
_requirements-yml:
    @just --justfile {{ justfile() }} _ensure_file_prepared {{ templates_directory_path }}/requirements.yml {{ justfile_directory() }}/requirements.yml

# Prepares the setup.yml file
_setup-yml:
    @just --justfile {{ justfile() }} _ensure_file_prepared {{ templates_directory_path }}/setup.yml {{ justfile_directory() }}/setup.yml

# Prepares the group_vars/mash_servers file
_group-vars-mash-servers:
    @just --justfile {{ justfile() }} _ensure_file_prepared {{ templates_directory_path }}/group_vars_mash_servers {{ justfile_directory() }}/group_vars/mash_servers

_ensure_file_prepared src_path dst_path:
    #!/usr/bin/env sh
    dst_file_name=$(basename "{{ dst_path }}")
    hash_path={{ run_directory_path }}"/"$dst_file_name".srchash"
    src_hash=$(md5sum {{ src_path }} | cut -d ' ' -f 1)

    if [ ! -f "{{ dst_path }}" ] || [ ! -f "$hash_path" ]; then
        cp {{ src_path }} {{ dst_path }}
        echo $src_hash > $hash_path
    else
        current_hash=$(cat $hash_path)

        if [ "$current_hash" != "$src_hash" ]; then
            cp {{ src_path }} {{ dst_path }}
            echo $src_hash > $hash_path

            if [ -f "$optimization_vars_files_file_path" ]; then
                just --justfile {{ justfile() }} \
                _optimize-for-var-paths \
                $(cat $optimization_vars_files_file_path)
            fi
        fi
    fi

_save_hash_for_file src_path dst_path:
    #!/usr/bin/env sh
    dst_file_name=$(basename "{{ dst_path }}")
    hash_path={{ run_directory_path }}"/"$dst_file_name".srchash"
    src_hash=$(md5sum {{ src_path }} | cut -d ' ' -f 1)
    echo $src_hash > $hash_path

_clean_template_derived_files:
    #!/usr/bin/env sh
    if [ -f "{{ justfile_directory() }}/requirements.yml" ]; then
        rm {{ justfile_directory() }}/requirements.yml
    fi

    if [ -f "{{ justfile_directory() }}/setup.yml" ]; then
        rm {{ justfile_directory() }}/setup.yml
    fi

    if [ -f "{{ justfile_directory() }}/group_vars/mash_servers" ]; then
        rm {{ justfile_directory() }}/group_vars/mash_servers
    fi
