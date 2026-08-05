#!/usr/bin/env python3
# -* encoding: utf8 *-

# SPDX-FileCopyrightText: 2026 2026 Oliver Lorenz
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import re
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
WORKFLOWS_DIR = REPO_ROOT / ".github" / "workflows"


def get_ready_hosts():
    hosts_path = REPO_ROOT / "inventory" / "hosts"
    if not hosts_path.is_file():
        return None

    hosts = []
    in_group = False
    for line in hosts_path.read_text().splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("["):
            in_group = stripped == "[mash_servers]"
            continue
        if in_group:
            hosts.append(stripped.split()[0])

    return sorted(
        host
        for host in hosts
        if (REPO_ROOT / "inventory" / "host_vars" / host / "secrets.yml").is_file()
    )


def get_role_specific_names_by_path():
    name_by_path = {}
    current_name = None
    for line in (REPO_ROOT / "templates" / "setup.yml").read_text().splitlines():
        match = re.match(r"\s*#\s*role-specific:(\S+)\s*$", line)
        if match:
            current_name = match.group(1)
            continue
        if re.match(r"\s*#\s*/role-specific:", line):
            current_name = None
            continue
        match = re.search(r"\brole:\s*(\S+)", line)
        if match and current_name:
            name_by_path[match.group(1)] = current_name
    return name_by_path


def get_enabled_services():
    vars_paths = sorted(
        str(path) for path in (REPO_ROOT / "inventory" / "host_vars").glob("*/vars.yml")
    )
    if not vars_paths:
        return []

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp = Path(tmp_dir)
        dst_setup_yml_path = tmp / "setup.yml"

        subprocess.run(
            [
                sys.executable,
                str(REPO_ROOT / "bin" / "optimize.py"),
                "--vars-paths",
                " ".join(vars_paths),
                "--src-requirements-yml-path",
                str(REPO_ROOT / "templates" / "requirements.yml"),
                "--dst-requirements-yml-path",
                str(tmp / "requirements.yml"),
                "--src-setup-yml-path",
                str(REPO_ROOT / "templates" / "setup.yml"),
                "--dst-setup-yml-path",
                str(dst_setup_yml_path),
                "--src-group-vars-yml-path",
                str(REPO_ROOT / "templates" / "group_vars_mash_servers"),
                "--dst-group-vars-yml-path",
                str(tmp / "group_vars_mash_servers"),
            ],
            check=True,
            cwd=REPO_ROOT,
        )

        name_by_path = get_role_specific_names_by_path()
        services = set()
        for line in dst_setup_yml_path.read_text().splitlines():
            match = re.search(r"\brole:\s*(\S+)", line)
            if match and match.group(1) in name_by_path:
                services.add(name_by_path[match.group(1)])

        return sorted(services)


def replace_generated_block(text, marker, items):
    begin = f"# BEGIN GENERATED: {marker}"
    end = f"# END GENERATED: {marker}"
    pattern = re.compile(
        r"^( *)" + re.escape(begin) + r"\n(?:.*\n)*?( *)" + re.escape(end) + r"\n",
        re.MULTILINE,
    )

    def _sub(match):
        indent = match.group(1)
        body = "".join(f"{indent}- {item}\n" for item in items)
        return f"{indent}{begin}\n{body}{indent}{end}\n"

    return pattern.subn(_sub, text)


def main():
    hosts = get_ready_hosts()

    if hosts is None:
        print(
            "inventory/hosts not found -- skipping "
            "(this check requires a local checkout of the private inventory submodule).",
        )
        return 0

    services = get_enabled_services()

    if not hosts:
        print(
            "::error::No hosts with inventory/host_vars/<host>/secrets.yml found -- refusing to generate an empty choice list.",
            file=sys.stderr,
        )
        return 1

    changed_files = []
    for path in sorted(WORKFLOWS_DIR.glob("*.yml")):
        text = path.read_text()
        original = text

        text, host_replacements = replace_generated_block(text, "hosts", hosts)
        text, service_replacements = replace_generated_block(text, "services", services)

        if service_replacements and not services:
            print(
                f"::error::{path}: no services found to populate the 'services' choice list.",
                file=sys.stderr,
            )
            return 1

        if text != original:
            path.write_text(text)
            changed_files.append(path.relative_to(REPO_ROOT))

    if changed_files:
        print("Updated generated options in:")
        for path in changed_files:
            print(f"  {path}")
        return 1

    print("Generated workflow options are already up to date.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
