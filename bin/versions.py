#!/usr/bin/env python3

import os
import re
import yaml

ignored = [
    'matrix_synapse_default_room_version',
]
prefixes = [
    'matrix_',
    'custom_',
    'int_',
    'synapse_default_',
    'synapse_ext_',
    'mailer_container_',
    'bot_',
    'client_',
    'mautrix_',
    'devture_',
    'beeper_',
    'backup_borg_',
]
suffixes = [
    '_version',
]


def find_versions():
    matches = {}
    for root, dirs, files in os.walk('.'):
        if root.endswith('defaults'):
            for file in files:
                if file.endswith('main.yml'):
                    path = os.path.join(root, file)
                    with open(path, 'r') as f:
                        data = yaml.safe_load(f)
                        for key, value in data.items():
                            if key.endswith('_version') and value and not re.search(r'{{|master|main|""', str(value)) and key not in ignored:
                                sanitized_key = sanitize_key(key)
                                matches[sanitized_key] = value
    return matches


def sanitize_key(key):
    for prefix in prefixes:
        key = key.removeprefix(prefix)
    for suffix in suffixes:
        key = key.removesuffix(suffix)
    return key.replace('_', ' ').title()


def generate_versions():
    versions = find_versions()
    with open(os.path.join(os.getcwd(), 'VERSIONS.md'), 'w') as f:
        for key, value in sorted(versions.items()):
            f.write(f'* {key}: {value}\n')


if __name__ == "__main__":
    generate_versions()
