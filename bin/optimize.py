#!/usr/bin/env python3
# -* encoding: utf8 *-

# SPDX-FileCopyrightText: 2023 - 2026 Slavi Pantaleev
# SPDX-FileCopyrightText: 2025 Javier Pais
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# Generates requirements.yml, setup.yml and group_vars/mash_servers/ from the components in components/
# and in the inventory's own components/ directory (if any).
#
# Only the components in use by the inventory are included (see `activation_prefix` in each component.yml),
# unless all components are requested with --all-components. See docs/developer-documentation.md for the
# structure of components.
#
# With --check, all components are validated and nothing is written.

import argparse
import os
import sys

try:
    import yaml
except ImportError:
    sys.exit(
        "Optimizing the playbook requires the PyYAML Python library. "
        "Install it with your package manager (e.g. `python3-yaml` or `python-yaml`) or pip."
    )

parser = argparse.ArgumentParser(
    description="Generates the playbook's requirements.yml, setup.yml and group_vars/mash_servers/ from its components"
)
parser.add_argument("--components-path", help="Path to the components directory", required=True)
parser.add_argument("--inventory-path", help="Path to the inventory directory, whose own components/ are used too")
parser.add_argument(
    "--playbook-path",
    help="Path to the playbook directory, whose own host_vars/ and group_vars/ are read too",
)
parser.add_argument(
    "--all-components",
    action="store_true",
    help="Include all components, instead of only those in use by the inventory",
)
parser.add_argument(
    "--check",
    action="store_true",
    help="Only validate all components, without writing anything",
)
parser.add_argument("--dst-requirements-yml-path", help="Path to the requirements.yml file to generate")
parser.add_argument("--dst-setup-yml-path", help="Path to the setup.yml file to generate")
parser.add_argument("--dst-group-vars-path", help="Path to the group_vars/mash_servers directory to generate")

args = parser.parse_args()

if not args.check:
    for name in ("dst_requirements_yml_path", "dst_setup_yml_path", "dst_group_vars_path"):
        if getattr(args, name) is None:
            parser.error("--{0} is required (unless --check is used)".format(name.replace("_", "-")))
    if not args.all_components and (args.inventory_path is None or args.playbook_path is None):
        parser.error("--inventory-path and --playbook-path are required (unless --all-components or --check is used)")


class VarsLoader(yaml.SafeLoader):
    """A YAML loader which accepts Ansible-specific tags (like `!vault`) and ignores their values."""


VarsLoader.add_multi_constructor("!", lambda loader, tag_suffix, node: None)


def load_variable_names_from_file(vars_path):
    with open(vars_path, "rb") as file:
        raw_contents = file.read()

    try:
        contents = raw_contents.decode("utf-8")
    except UnicodeDecodeError:
        # Binary files are not variable files. If Ansible loads this one, it reports it itself.
        return set()

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


def list_directory(path):
    """Lists a directory, without hidden files and backups (e.g. `.DS_Store`, editor swap files)."""
    return [name for name in sorted(os.listdir(path)) if not is_ignored_by_ansible(name)]


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


def find_vars_file_paths(path, skipped_path=None):
    """Finds the variable files of all hosts and groups (host_vars/ and group_vars/) in an inventory or playbook directory.

    `skipped_path` (a file or directory) is left out.
    """
    found = []
    for vars_directory_name in ("host_vars", "group_vars"):
        vars_directory_path = os.path.join(path, vars_directory_name)
        if not os.path.isdir(vars_directory_path):
            continue
        for name in sorted(os.listdir(vars_directory_path)):
            if is_ignored_by_ansible(name):
                continue
            entry_path = os.path.join(vars_directory_path, name)
            if skipped_path is not None and os.path.realpath(entry_path) == os.path.realpath(skipped_path):
                continue
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


def parse_yaml(contents, path):
    try:
        return yaml.load(contents, Loader=VarsLoader)
    except yaml.YAMLError as e:
        fail("{0} is not valid YAML: {1}".format(path, e))


def load_yaml_file(path):
    return parse_yaml(read_file(path), path)


def read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as file:
            return file.read()
    except UnicodeDecodeError:
        fail("{0} is not a UTF-8 text file".format(path))


def write_to_file(contents, path):
    if os.path.isfile(path):
        with open(path, "rb") as file:
            if file.read() == contents.encode("utf-8"):
                return
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    # Write to a temporary file first, so that an interrupted write does not leave a partial file behind
    temporary_path = path + ".tmp"
    with open(temporary_path, "w", encoding="utf-8") as file:
        file.write(contents)
    os.replace(temporary_path, path)


def fail(message):
    sys.exit("Error: {0}".format(message))


# --- Loading and validating components ------------------------------------------------------------

COMPONENT_KEYS = {"activation_prefix", "setup", "accepts", "inject"}
SETUP_KEYS = {"priority", "entry"}
ACCEPTS_KEYS = {"description", "into", "required_keys"}
COMPONENT_FILES = {"component.yml", "README.md", "requirements.yml", "wiring.yml", "assets", "with", "roles"}

# Components without a `setup` priority run at this one, sorted by name
DEFAULT_PRIORITY = 1000


def load_components(components_paths):
    components = {}
    for components_path in components_paths:
        for name in sorted(os.listdir(components_path)):
            if is_ignored_by_ansible(name):
                continue
            path = os.path.join(components_path, name)
            if name in components:
                fail("{0} has the same name as {1}. Rename one of them".format(path, components[name]["path"]))
            components[name] = load_component(path)
    return components


def load_component(path):
    if not os.path.isdir(path):
        fail("{0} is not a component directory".format(path))
    manifest_path = os.path.join(path, "component.yml")
    if not os.path.isfile(manifest_path):
        fail("{0} has no component.yml".format(path))
    manifest = load_yaml_file(manifest_path) or {}
    if not isinstance(manifest, dict):
        fail("{0} does not contain a mapping".format(manifest_path))
    return {"path": path, "manifest": manifest}


def setup_placements(component):
    """Returns where a component runs in setup.yml: a list of {priority, entry} (a single one, unless `setup` is a list)."""
    setup = component["manifest"].get("setup")
    if setup is None:
        return [{}]
    return setup if isinstance(setup, list) else [setup]


def is_component_role(item):
    """Tells whether a setup.yml entry runs a role of the component itself (`./roles/<role>`)."""
    return isinstance(item.get("role"), str) and item["role"].startswith("./")


def validate_components(components):
    for name, component in components.items():
        path, manifest = component["path"], component["manifest"]
        manifest_path = os.path.join(path, "component.yml")

        unknown = sorted(set(list_directory(path)) - COMPONENT_FILES)
        if unknown:
            fail("{0} contains unknown files: {1}".format(path, ", ".join(unknown)))

        unknown = sorted(set(manifest) - COMPONENT_KEYS)
        if unknown:
            fail("{0} contains unknown keys: {1}".format(manifest_path, ", ".join(unknown)))
        if not isinstance(manifest.get("activation_prefix"), str):
            fail("{0} needs an `activation_prefix` (`''` for components which are always in use)".format(manifest_path))

        requirements_path = os.path.join(path, "requirements.yml")
        if os.path.exists(requirements_path):
            requirements = load_yaml_file(requirements_path)
            if (
                not isinstance(requirements, list)
                or len(requirements) != 1
                or not isinstance(requirements[0], dict)
                or requirements[0].get("name") != name
            ):
                fail("{0} must contain exactly one role, named {1}".format(requirements_path, name))
            component["requirement"] = requirements[0]

        for setup in setup_placements(component):
            if not isinstance(setup, dict) or set(setup) - SETUP_KEYS:
                fail("{0}: `setup` may only contain {1} (or be a list of such)".format(
                    manifest_path, ", ".join(sorted(SETUP_KEYS))))
            if not isinstance(setup.get("priority", DEFAULT_PRIORITY), int):
                fail("{0}: `setup.priority` must be a number".format(manifest_path))
            if "entry" not in setup:
                if "requirement" not in component:
                    fail("{0} has neither a requirements.yml nor a `setup.entry` to run "
                         "(`setup: []` for a component which runs nothing)".format(path))
                continue
            if not isinstance(setup["entry"], list) or not all(isinstance(item, dict) for item in setup["entry"]):
                fail("{0}: `setup.entry` must be a list of setup.yml role entries".format(manifest_path))
            for item in setup["entry"]:
                if is_component_role(item) and not os.path.isdir(os.path.join(path, item["role"])):
                    fail("{0}: the role {1} does not exist in {2}".format(manifest_path, item["role"], path))

        with_path = os.path.join(path, "with")
        if os.path.isdir(with_path):
            for file_name in list_directory(with_path):
                other, extension = os.path.splitext(file_name)
                if extension != ".yml" or other not in components or other == name:
                    fail("{0}: with/ may only contain <component>.yml files for other components".format(path))

        for field in ("accepts", "inject"):
            if not isinstance(manifest.get(field) or {}, dict):
                fail("{0}: `{1}` must be a mapping".format(manifest_path, field))

        for list_name, accepted in (manifest.get("accepts") or {}).items():
            if not isinstance(accepted, dict) or set(accepted) - ACCEPTS_KEYS or not isinstance(accepted.get("into"), str):
                fail("{0}: `accepts.{1}` needs an `into` variable (and optionally `description`, `required_keys`)".format(
                    manifest_path, list_name))

        for provider, lists in (manifest.get("inject") or {}).items():
            if provider not in components:
                fail("{0} injects into {1}, which is not a component".format(manifest_path, provider))
            accepts = components[provider]["manifest"].get("accepts") or {}
            if not isinstance(lists or {}, dict):
                fail("{0}: `inject.{1}` must be a mapping of lists".format(manifest_path, provider))
            for list_name, entries in (lists or {}).items():
                if list_name not in accepts:
                    fail("{0} injects into {1}.{2}, but {1} accepts {3}".format(
                        manifest_path, provider, list_name, ", ".join(sorted(accepts)) or "nothing"))
                if not isinstance(entries or [], list):
                    fail("{0}: `inject.{1}.{2}` must be a list".format(manifest_path, provider, list_name))
                for entry in entries or []:
                    if not isinstance(entry, dict):
                        fail("{0}: entries for {1}.{2} must be mappings".format(manifest_path, provider, list_name))
                    missing = set(accepts[list_name].get("required_keys") or []) - set(entry)
                    if missing:
                        fail("{0}: an entry for {1}.{2} lacks {3}".format(
                            manifest_path, provider, list_name, ", ".join(sorted(missing))))


def is_component_in_use(manifest, used_variable_names):
    prefix = manifest["activation_prefix"]
    # An empty prefix means "always in use"
    return prefix == "" or any(variable_name.startswith(prefix) for variable_name in used_variable_names)


# --- Generating files -----------------------------------------------------------------------------

SETUP_YML_HEADER = """---
# Generated from components/ (see `setup` in each component.yml). Do not edit.

- name: "Set up a self-hosted server"
  hosts: "{{ target if target is defined else 'mash_servers' }}"
  become: true

  roles:
"""


class Dumper(yaml.SafeDumper):
    """Dumps Jinja templates with double quotes, like the hand-written files."""


Dumper.add_representer(
    str,
    lambda dumper, value: dumper.represent_scalar("tag:yaml.org,2002:str", value, style='"' if "{{" in value else None),
)


def dump_yaml(data):
    return yaml.dump(data, Dumper=Dumper, sort_keys=False, width=1000, default_flow_style=False, allow_unicode=True)


def indent(text, prefix):
    return "".join(prefix + line if line.strip() else line for line in text.splitlines(True))


def generate_requirements_yml(components, names):
    return yaml.dump([components[name]["requirement"] for name in names if "requirement" in components[name]])


def generate_setup_yml(components, names, setup_yml_directory):
    placements = []
    for name in names:
        for index, setup in enumerate(setup_placements(components[name])):
            placements.append((setup.get("priority", DEFAULT_PRIORITY), name, index, setup))

    parts = [SETUP_YML_HEADER]
    for _, name, _, setup in sorted(placements, key=lambda placement: placement[:3]):
        entry = []
        for item in setup.get("entry") or [{"role": "galaxy/" + name}]:
            if is_component_role(item):
                # Its path is relative to the component's directory, while Ansible looks for it relative to setup.yml
                role_path = os.path.join(components[name]["path"], item["role"])
                item = dict(item, role=os.path.relpath(role_path, setup_yml_directory))
            entry.append(item)
        parts.append(indent(dump_yaml(entry), "    ") + "\n")
    return "".join(parts).rstrip("\n") + "\n"


def generate_injected_yml(components, names, provider):
    """Fills the variables the provider names in `accepts` with what the components in use inject into it."""
    lines = [
        "---",
        "# Generated from the `inject` entries of the components in use, into the variables named by",
        "# `accepts` in components/{0}/component.yml. Do not edit.".format(provider),
        "",
    ]
    for list_name, accepted in sorted(components[provider]["manifest"]["accepts"].items()):
        variable = accepted["into"]
        entries = []
        for name in names:
            for entry in ((components[name]["manifest"].get("inject") or {}).get(provider) or {}).get(list_name) or []:
                entries.append((name, dict(entry) if "when" in entry else dict(entry, when=True)))

        lines.append("{0}_unfiltered:{1}".format(variable, "" if entries else " []"))
        for name, entry in entries:
            lines.append("  # {0}".format(name))
            lines.append(indent(dump_yaml([entry]), "  ").rstrip("\n"))
        lines += [
            "",
            "# The entries above whose `when` is true, without `when`",
            "{0}: >-".format(variable),
            "  {{",
            "    {0}_unfiltered".format(variable),
            "    | selectattr('when')",
            "    | map('dict2items') | map('rejectattr', 'key', 'equalto', 'when') | map('items2dict')",
            "  }}",
            "",
        ]
    return "\n".join(lines)


def generate_group_vars(components, names):
    """Returns the group_vars/mash_servers/ files (relative path -> contents) for the components in use."""
    files = {}
    for name in names:
        path = components[name]["path"]
        if os.path.isfile(os.path.join(path, "wiring.yml")):
            files[os.path.join(name, "wiring.yml")] = read_file(os.path.join(path, "wiring.yml"))
        with_path = os.path.join(path, "with")
        if os.path.isdir(with_path):
            for file_name in list_directory(with_path):
                # Wiring with another component only applies when that one is in use too
                if os.path.splitext(file_name)[0] in names:
                    files[os.path.join(name, "with", file_name)] = read_file(os.path.join(with_path, file_name))
        if components[name]["manifest"].get("accepts"):
            files[os.path.join(name, "injected.yml")] = generate_injected_yml(components, names, name)
    return files


def check_duplicate_variables(files):
    # The same variable in two files would depend on the order in which Ansible loads them
    defined_in = {}
    for relative_path, contents in sorted(files.items()):
        variables = parse_yaml(contents, relative_path) or {}
        if not isinstance(variables, dict):
            fail("{0} must contain a mapping of variables".format(relative_path))
        for variable in variables:
            if variable in defined_in:
                fail("{0} is defined in both {1} and {2}".format(variable, defined_in[variable], relative_path))
            defined_in[variable] = relative_path


# Marks the generated group_vars directory, so that we never delete files from a directory we did not generate.
# Ansible ignores hidden files in group_vars.
GROUP_VARS_MARKER = ".generated"
GROUP_VARS_MARKER_CONTENTS = (
    "# This directory is generated by bin/optimize.py from components/ before every run.\n"
    "# Do not edit or add files here: they get replaced or deleted. Configure services in your inventory instead.\n"
)


def check_group_vars_destination(path):
    """Refuses to replace a directory which we did not generate (e.g. a mistyped --dst-group-vars-path)."""
    if os.path.isdir(path) and not os.path.islink(path) and os.listdir(path):
        if not os.path.isfile(os.path.join(path, GROUP_VARS_MARKER)):
            fail(
                "{0} exists, but was not generated by this script (it has no {1} file). "
                "Move it away, or pass another --dst-group-vars-path".format(path, GROUP_VARS_MARKER)
            )


def write_group_vars(files, path):
    """Makes the directory at `path` contain exactly these files, leaving unchanged ones as they are."""
    if os.path.isfile(path) or os.path.islink(path):
        # A file generated by older versions of the playbook
        os.unlink(path)
    files = dict(files, **{GROUP_VARS_MARKER: GROUP_VARS_MARKER_CONTENTS})
    for relative_path, contents in files.items():
        write_to_file(contents, os.path.join(path, relative_path))
    for root, directory_names, file_names in os.walk(path, topdown=False):
        for file_name in file_names:
            file_path = os.path.join(root, file_name)
            if os.path.relpath(file_path, path) not in files:
                os.unlink(file_path)
        if root != path and not os.listdir(root):
            os.rmdir(root)


components_paths = [args.components_path]
if args.inventory_path is not None:
    # Components of the inventory itself, to extend the playbook without changing it.
    # An inventory in the playbook's own directory has none: there, components/ are the playbook's.
    inventory_components_path = os.path.join(args.inventory_path, "components")
    if os.path.isdir(inventory_components_path) and os.path.realpath(inventory_components_path) != os.path.realpath(
        args.components_path
    ):
        components_paths.append(inventory_components_path)
components = load_components(components_paths)
validate_components(components)

if args.check:
    check_duplicate_variables(generate_group_vars(components, sorted(components)))
    print("{0} components are valid".format(len(components)))
    sys.exit(0)

# Without an inventory to optimize for (e.g. before it is created), all components are included
include_all = args.all_components
if not include_all:
    reason = None
    if not os.path.isdir(args.inventory_path):
        reason = "the inventory directory ({0}) does not exist".format(args.inventory_path)
    elif len(find_vars_file_paths(args.inventory_path)) == 0:
        reason = "no variable files (in host_vars/ or group_vars/) were found in the inventory directory ({0})".format(
            args.inventory_path
        )
    if reason is not None:
        include_all = True
        print(
            "Note: including all components, because {0}. "
            "If your inventory is elsewhere, point the `ANSIBLE_INVENTORY` environment variable to its hosts file.".format(reason),
            file=sys.stderr,
        )

if include_all:
    names = sorted(components)
else:
    vars_file_paths = find_vars_file_paths(args.inventory_path)
    # Ansible also reads the playbook's own host_vars/ and group_vars/. Unlike the inventory's group_vars,
    # the playbook's group_vars/<group> can override group_vars/mash_servers, so services may be enabled there.
    # group_vars/mash_servers itself is skipped, since we generate it.
    vars_file_paths += find_vars_file_paths(args.playbook_path, skipped_path=args.dst_group_vars_path)
    used_variable_names = load_combined_variable_names_from_files(vars_file_paths)
    names = [name for name in sorted(components) if is_component_in_use(components[name]["manifest"], used_variable_names)]

group_vars_files = generate_group_vars(components, names)
check_duplicate_variables(group_vars_files)
requirements_yml = generate_requirements_yml(components, names)
setup_yml = generate_setup_yml(components, names, os.path.dirname(os.path.abspath(args.dst_setup_yml_path)))

# Only write once everything has been generated successfully, so that the files match each other
check_group_vars_destination(args.dst_group_vars_path)
write_to_file(requirements_yml, args.dst_requirements_yml_path)
write_to_file(setup_yml, args.dst_setup_yml_path)
write_group_vars(group_vars_files, args.dst_group_vars_path)
