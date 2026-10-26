#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 MASH project contributors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# Checks that the wiring of components/ leaves the roles' variables meant for users to them.
#
# Roles keep some variables free for their users, recognizable by their names (e.g.
# `*_container_additional_networks_custom` next to the `*_auto` one which the playbook sets).
# When the wiring sets one of them, a user setting it too silently replaces the playbook's value.
# This script reads the variables which `wiring.yml` and `with/*.yml` files define, and prints
# those named like a variable meant for users. See the developer documentation (`wiring.yml` and
# `with/`) for what to do instead.
# It goes by names only: it does not know which variables the roles have.
#
# Usage: bin/check-components-user-variables.py components/*/wiring.yml components/*/with/*.yml

import re
import sys

import yaml

# Names of the variables which roles keep free for their users
USER_VARIABLE_PATTERN = re.compile(r"_(custom|additional_labels|additional_variables)$")


def main(paths):
    failed = False
    for path in paths:
        try:
            with open(path, encoding="utf-8") as file:
                document = yaml.compose(file, Loader=yaml.SafeLoader)
        except yaml.YAMLError as error:
            print(f"{path}: invalid YAML: {error}")
            failed = True
            continue
        if not isinstance(document, yaml.MappingNode):
            continue
        for key, _ in document.value:
            if USER_VARIABLE_PATTERN.search(key.value):
                line = key.start_mark.line + 1
                print(f"{path}:{line}: {key.value} is meant for users; set the role's `*_auto` variable (or add one to the role) instead")
                failed = True
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
