#!/usr/bin/env python3
# -* encoding: utf8 *-

# SPDX-FileCopyrightText: 2023 - 2024 Slavi Pantaleev
# SPDX-FileCopyrightText: 2025 Javier Pais
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import argparse
import os
import re
import sys

try:
    import yaml
except ImportError:
    sys.exit(
        "Optimizing the playbook requires the PyYAML Python library. "
        "Install it with your package manager (e.g. `python3-yaml` or `python-yaml`) or pip."
    )

parser = argparse.ArgumentParser(
    description="Optimizes the playbook based on enabled components found in the inventory's variable files"
)
parser.add_argument(
    "--inventory-path",
    help="Path to the inventory directory",
    required=True,
)
parser.add_argument(
    "--src-requirements-yml-path",
    help="Path to source requirements.yml file with all role definitions",
    required=True,
)
parser.add_argument(
    "--src-setup-yml-path", help="Path to source setup.yml file", required=True
)
parser.add_argument(
    "--src-group-vars-yml-path", help="Path to source group vars file", required=True
)
parser.add_argument(
    "--dst-requirements-yml-path",
    help="Path to destination requirements.yml file, where role definitions will be saved",
    required=True,
)
parser.add_argument(
    "--dst-setup-yml-path", help="Path to destination setup.yml file", required=True
)
parser.add_argument(
    "--dst-group-vars-yml-path",
    help="Path to destination group vars file",
    required=True,
)

args = parser.parse_args()


class VarsLoader(yaml.SafeLoader):
    """A YAML loader which accepts Ansible-specific tags (like `!vault`) and ignores their values."""


VarsLoader.add_multi_constructor("!", lambda loader, tag_suffix, node: None)


def load_variable_names_from_file(vars_path):
    with open(vars_path, "r") as file:
        contents = file.read()

    if contents.startswith("$ANSIBLE_VAULT;"):
        # We don't decrypt secrets. Variables which enable roles are not expected to be in such files.
        return set()

    try:
        yaml_data = yaml.load(contents, Loader=VarsLoader)
    except yaml.YAMLError as e:
        print(
            "Warning: skipping {0}, because it is not valid YAML: {1}".format(vars_path, e),
            file=sys.stderr,
        )
        return set()

    if yaml_data is None:
        # Empty file or one with comments only
        return set()

    if not isinstance(yaml_data, dict):
        print(
            "Warning: skipping {0}, because it does not contain a mapping of variables".format(vars_path),
            file=sys.stderr,
        )
        return set()

    return set(yaml_data.keys())


# Like Ansible's `yaml_valid_extensions` (files without an extension are loaded too)
VARS_FILE_EXTENSIONS = ("", ".yml", ".yaml", ".json")


def is_ignored_by_ansible(name):
    # Hidden files and backups
    return name.startswith(".") or name.endswith("~")


def find_vars_file_paths_in_directory(path):
    """Finds variable files in a host's or group's directory, like Ansible's host_group_vars plugin does."""
    found = []
    for name in sorted(os.listdir(path)):
        if is_ignored_by_ansible(name):
            continue
        entry_path = os.path.join(path, name)
        extension = os.path.splitext(name)[1]
        if os.path.isdir(entry_path):
            if extension == "":
                found.extend(find_vars_file_paths_in_directory(entry_path))
        elif extension in VARS_FILE_EXTENSIONS:
            found.append(entry_path)
    return found


def find_vars_file_paths(inventory_path):
    """Finds the variable files of all hosts and groups (host_vars/ and group_vars/) in the inventory."""
    found = []
    for vars_directory_name in ("host_vars", "group_vars"):
        vars_directory_path = os.path.join(inventory_path, vars_directory_name)
        if not os.path.isdir(vars_directory_path):
            continue
        for name in sorted(os.listdir(vars_directory_path)):
            if is_ignored_by_ansible(name):
                continue
            entry_path = os.path.join(vars_directory_path, name)
            if os.path.isdir(entry_path):
                found.extend(find_vars_file_paths_in_directory(entry_path))
            else:
                # Ansible picks these files by host or group name, which may contain dots (e.g. `host_vars/example.com`),
                # so their extension tells nothing.
                found.append(entry_path)
    return found


def load_combined_variable_names_from_files(vars_yml_file_paths):
    variable_names = set({})
    for vars_path in vars_yml_file_paths:
        variable_names = variable_names | load_variable_names_from_file(vars_path)
    return variable_names


def load_yaml_file(path):
    with open(path, "r") as file:
        return yaml.safe_load(file)


def is_role_definition_in_use(role_definition, used_variable_names):
    for variable_name in used_variable_names:
        if "activation_prefix" in role_definition:
            if role_definition["activation_prefix"] == "":
                # Special value indicating "always activate".
                # We don't really need this dedicated if, but it's more obvious with it.
                return True
            if variable_name.startswith(role_definition["activation_prefix"]):
                return True
    return False


def read_file(path):
    with open(path, "r") as file:
        return file.read()


def write_to_file(contents, path):
    # Write to a temporary file first, so that an interrupted write does not leave a partial file behind
    temporary_path = path + ".tmp"
    with open(temporary_path, "w") as file:
        file.write(contents)
    os.replace(temporary_path, path)


# Matches the beginning of role-specific blocks.
# Example: `# role-specific:playbook_help`
regex_role_specific_block_start = re.compile(
    "^\\s*#\\s*role-specific:\\s*([^\\s]+)$"
)

# Matches the end of role-specific blocks.
# Example: `# /role-specific:playbook_help`
regex_role_specific_block_end = re.compile("^\\s*#\\s*/role-specific:\\s*([^\\s]+)$")


def process_file_contents(file_name, enabled_role_names, known_role_names):
    contents = read_file(file_name)

    lines_preserved = []
    role_specific_stack = []

    for line_number, line in enumerate(contents.split("\n")):
        # Stage 1: looking for a role-specific starting block
        start_role_matches = regex_role_specific_block_start.match(line)
        if start_role_matches is not None:
            role_name = start_role_matches.group(1)
            if role_name not in known_role_names:
                raise Exception(
                    "Found start block for role {0} on line {1} in file {2}, but it is not a known role name found among: {3}".format(
                        role_name,
                        line_number,
                        file_name,
                        known_role_names,
                    )
                )
            role_specific_stack.append(role_name)
            continue

        # Stage 2: looking for role-specific closing blocks
        end_role_matches = regex_role_specific_block_end.match(line)
        if end_role_matches is not None:
            role_name = end_role_matches.group(1)
            if role_name not in known_role_names:
                raise Exception(
                    "Found end block for role {0} on line {1} in file {2}, but it is not a known role name found among: {3}".format(
                        role_name,
                        line_number,
                        file_name,
                        known_role_names,
                    )
                )

            if len(role_specific_stack) == 0:
                raise Exception(
                    "Found end block for role {0} on line {1} in file {2}, but there is no opening statement for it".format(
                        role_name,
                        line_number,
                        file_name,
                    )
                )

            last_role_name = role_specific_stack[len(role_specific_stack) - 1]
            if role_name != last_role_name:
                raise Exception(
                    "Found end block for role {0} on line {1} in file {2}, but the last starting block was for role {3}".format(
                        role_name,
                        line_number,
                        file_name,
                        last_role_name,
                    )
                )

            role_specific_stack.pop()

            continue

        # Stage 3: regular line
        all_roles_allowed = True
        for role_name in role_specific_stack:
            if role_name not in enabled_role_names:
                all_roles_allowed = False
                break

        if all_roles_allowed:
            lines_preserved.append(line)

    if len(role_specific_stack) != 0:
        raise Exception(
            "Expected one or more closing block for role-specific tags in file {0}: {1}".format(
                file_name, role_specific_stack
            )
        )

    lines_final = []
    sequential_blank_lines_count = 0
    for line in lines_preserved:
        if line != "":
            lines_final.append(line)
            sequential_blank_lines_count = 0
            continue

        if sequential_blank_lines_count <= 1:
            lines_final.append(line)
            sequential_blank_lines_count += 1
            continue

    return "\n".join(lines_final)


if not os.path.isdir(args.inventory_path):
    sys.exit(
        "Cannot optimize the playbook: the inventory directory ({0}) does not exist. "
        "If your inventory is elsewhere, point the `ANSIBLE_INVENTORY` environment variable to its hosts file.".format(
            args.inventory_path
        )
    )

vars_paths = find_vars_file_paths(args.inventory_path)
if len(vars_paths) == 0:
    sys.exit(
        "Cannot optimize the playbook: no variable files (in host_vars/ or group_vars/) found in the inventory directory ({0})".format(
            args.inventory_path
        )
    )

used_variable_names = load_combined_variable_names_from_files(vars_paths)

all_role_definitions = load_yaml_file(args.src_requirements_yml_path)

enabled_role_definitions = []
for role_definition in all_role_definitions:
    if "name" not in role_definition:
        raise Exception(
            "Role definition does not have a name and should be adjusted to have one: {0}".format(
                role_definition
            )
        )
    if is_role_definition_in_use(role_definition, used_variable_names):
        enabled_role_definitions.append(role_definition)

known_role_names = tuple(
    map(lambda definition: definition["name"], all_role_definitions)
)
enabled_role_names = tuple(
    map(lambda definition: definition["name"], enabled_role_definitions)
)

setup_yml_processed = process_file_contents(
    args.src_setup_yml_path, enabled_role_names, known_role_names
)
group_vars_yml_processed = process_file_contents(
    args.src_group_vars_yml_path, enabled_role_names, known_role_names
)

# Only write once everything has been processed successfully, so that the files always match each other
write_to_file(yaml.dump(enabled_role_definitions), args.dst_requirements_yml_path)
write_to_file(setup_yml_processed, args.dst_setup_yml_path)
write_to_file(group_vars_yml_processed, args.dst_group_vars_yml_path)
