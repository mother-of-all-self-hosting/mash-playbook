# Shows help
default:
    @just --list --justfile {{ justfile() }}

# Pulls external Ansible roles
roles: requirements-yml
    #!/usr/bin/env sh
    if [ -x "$(command -v agru)" ]; then
        agru -r {{ justfile_directory() }}/requirements.yml
    else
        rm -rf roles/galaxy
        ansible-galaxy install -r requirements.yml -p roles/galaxy/ --force
    fi

# Updates requirements.yml if there are any new tags available. Requires agru
update: && opml
    @agru -r {{ justfile_directory() }}/requirements.all.yml -u

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
run +extra_args: requirements-yml
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
requirements-yml:
    #!/usr/bin/env sh
    if [ ! -f "{{ justfile_directory() }}/requirements.yml" ]; then
        cp {{ justfile_directory() }}/requirements.all.yml {{ justfile_directory() }}/requirements.yml
    fi
