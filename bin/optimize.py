#!/usr/bin/env python3
# -* encoding: utf8 *-

import argparse
import regex
import sys
import yaml
import os


parser = argparse.ArgumentParser(description='Optimizes the playbook based on enabled components found in vars.yml files')
parser.add_argument('--vars-paths', help='Path to vars.yml configuration files to process', required=True)
parser.add_argument('--src-requirements-yml-path', help='Path to source requirements.yml file with all role definitions', required=True)
parser.add_argument('--src-setup-yml-path', help='Path to source setup.yml file', required=True)
parser.add_argument('--src-group-vars-yml-path', help='Path to source group vars file', required=True)
parser.add_argument('--dst-requirements-yml-path', help='Path to destination requirements.yml file, where role definitions will be saved', required=True)
parser.add_argument('--dst-setup-yml-path', help='Path to destination setup.yml file', required=True)
parser.add_argument('--dst-group-vars-yml-path', help='Path to destination group vars file', required=True)

args = parser.parse_args()

def load_combined_variable_names_from_files(vars_yml_file_paths):
    variable_names = set({})
    for vars_path in vars_yml_file_paths:
        with open(vars_path, 'r') as file:
            yaml_data = yaml.safe_load(file)

            variable_names = variable_names | set(yaml_data.keys())
    return variable_names

def load_yaml_file(path):
    with open(path, 'r') as file:
        return yaml.safe_load(file)

def is_role_definition_in_use(role_definition, used_variable_names):
    for variable_name in used_variable_names:
        if 'activation_prefix' in role_definition:
            if role_definition['activation_prefix'] == '':
                # Special value indicating "always activate".
                # We don't really need this dedicated if, but it's more obvious with it.
                return True
            if variable_name.startswith(role_definition['activation_prefix']):
                return True
    return False

def write_yaml_to_file(definitions, path):
    with open(path, 'w') as file:
        yaml.dump(definitions, file)

def read_file(path):
    with open(path, 'r') as file:
        return file.read()

def write_to_file(contents, path):
    with open(path, 'w') as file:
        file.write(contents)

# Matches the beginning of role-specific blocks.
# Example: `# role-specific:playbook_help`
regex_role_specific_block_start = regex.compile('^\\s*#\\s*role-specific:\\s*([^\\s]+)$')

# Matches the end of role-specific blocks.
# Example: `# /role-specific:playbook_help`
regex_role_specific_block_end = regex.compile('^\\s*#\\s*/role-specific:\\s*([^\\s]+)$')

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
                raise Exception('Found start block for role {0} on line {1} in file {2}, but it is not a known role name found among: {3}'.format(
                    role_name,
                    line_number,
                    file_name,
                    known_role_names,
                ))
            role_specific_stack.append(role_name)
            continue

        # Stage 2: looking for role-specific closing blocks
        end_role_matches = regex_role_specific_block_end.match(line)
        if end_role_matches is not None:
            role_name = end_role_matches.group(1)
            if role_name not in known_role_names:
                raise Exception('Found end block for role {0} on line {1} in file {2}, but it is not a known role name found among: {3}'.format(
                    role_name,
                    line_number,
                    file_name,
                    known_role_names,
                ))

            if len(role_specific_stack) == 0:
                raise Exception('Found end block for role {0} on line {1} in file {2}, but there is no opening statement for it'.format(
                    role_name,
                    line_number,
                    file_name,
                ))

            last_role_name = role_specific_stack[len(role_specific_stack) - 1]
            if role_name != last_role_name:
                raise Exception('Found end block for role {0} on line {1} in file {2}, but the last starting block was for role {3}'.format(
                    role_name,
                    line_number,
                    file_name,
                    last_role_name,
                ))

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
        raise Exception('Expected one or more closing block for role-specific tags in file {0}: {1}'.format(file_name, role_specific_stack))

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

vars_paths = args.vars_paths.split(' ')
used_variable_names = load_combined_variable_names_from_files(vars_paths)
all_role_definitions = load_yaml_file(args.src_requirements_yml_path)

def add_custom_roles_to_definitions(all_role_definitions):
    custom_roles_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'roles', 'custom')
    if os.path.isdir(custom_roles_dir):
        for entry in os.listdir(custom_roles_dir):
            entry_path = os.path.join(custom_roles_dir, entry)
            if os.path.isdir(entry_path) and not entry.startswith('.'):
                # Map directory name to role name and activation prefix
                role_name = entry
                activation_prefix = f"{role_name}_"
                # Only add if not already present in all_role_definitions
                if not any(r.get('name') == role_name for r in all_role_definitions):
                    all_role_definitions.append({
                        'name': role_name,
                        'activation_prefix': activation_prefix
                    })
    return all_role_definitions

all_role_definitions = add_custom_roles_to_definitions(all_role_definitions)

enabled_role_definitions = []
for role_definition in all_role_definitions:
    if 'name' not in role_definition:
        raise Exception('Role definition does not have a name and should be adjusted to have one: {0}'.format(role_definition))
    if is_role_definition_in_use(role_definition, used_variable_names):
        enabled_role_definitions.append(role_definition)

write_yaml_to_file(enabled_role_definitions, args.dst_requirements_yml_path)

known_role_names = tuple(map(lambda definition: definition['name'], all_role_definitions))
enabled_role_names = tuple(map(lambda definition: definition['name'], enabled_role_definitions))

setup_yml_processed = process_file_contents(args.src_setup_yml_path, enabled_role_names, known_role_names)
write_to_file(setup_yml_processed, args.dst_setup_yml_path)

group_vars_yml_processed = process_file_contents(args.src_group_vars_yml_path, enabled_role_names, known_role_names)
write_to_file(group_vars_yml_processed, args.dst_group_vars_yml_path)
