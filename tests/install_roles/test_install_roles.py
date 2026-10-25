#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 MASH project contributors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# Tests for bin/install-roles.py.
#
# Fake `agru` and `ansible-galaxy` commands "install" roles like the real ones do
# (replacing the role's directory, and recording its version in meta/.galaxy_install_info)
# and log the roles they were asked to install.
#
# Run directly (`tests/install_roles/test_install_roles.py`) or via the `test-install-roles` pre-commit hook.

import ast
import os
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[2]
SCRIPT = REPO / "bin" / "install-roles.py"

# Each test's files go here (var/ is gitignored) and are removed afterwards.
TMP_ROOT = REPO / "var" / "tests" / "install_roles"

# Arguments: the requirements file (-r) and the roles path (-p), in any position
FAKE_INSTALLER = textwrap.dedent("""\
    #!/usr/bin/env python3
    import os, shutil, sys, yaml
    arguments = sys.argv[1:]
    requirements_path = arguments[arguments.index("-r") + 1]
    roles_path = arguments[arguments.index("-p") + 1]
    if os.environ.get("FAKE_INSTALLER_FAIL"):
        sys.exit(3)
    names = []
    for definition in yaml.safe_load(open(requirements_path)):
        role_path = os.path.join(roles_path, definition["name"])
        shutil.rmtree(role_path, ignore_errors=True)
        os.makedirs(os.path.join(role_path, "meta"))
        os.makedirs(os.path.join(role_path, "tasks"))
        open(os.path.join(role_path, "tasks", "main.yml"), "w").write("# {0}\\n".format(definition["version"]))
        open(os.path.join(role_path, "meta", ".galaxy_install_info"), "w").write("version: {0}\\n".format(definition["version"]))
        names.append(definition["name"])
    with open(os.environ["FAKE_INSTALLER_LOG"], "a") as log:
        log.write("{0} {1}\\n".format(os.path.basename(sys.argv[0]), ",".join(names)))
    """)


class InstallRolesTestCase(unittest.TestCase):
    def setUp(self):
        TMP_ROOT.mkdir(parents=True, exist_ok=True)
        tmp = tempfile.TemporaryDirectory(prefix="test-", dir=TMP_ROOT)
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.roles_path = self.root / "roles"
        self.state_path = self.root / "run" / "installed-roles.yml"
        self.log_path = self.root / "installer.log"

        bin_path = self.root / "bin"
        bin_path.mkdir()
        for name in ("agru", "ansible-galaxy"):
            (bin_path / name).write_text(FAKE_INSTALLER)
            (bin_path / name).chmod(0o755)
        self.env = {
            **os.environ,
            "PATH": "{0}:{1}".format(bin_path, os.environ["PATH"]),
            "FAKE_INSTALLER_LOG": str(self.log_path),
        }

    def requirements(self, roles, file_name="requirements.yml"):
        """Writes a requirements file with the given {name: version} roles."""
        path = self.root / file_name
        path.write_text(yaml.safe_dump([
            {"src": "git+https://example.com/{0}.git".format(name), "version": version, "name": name}
            for name, version in roles.items()
        ]))
        return path

    def run_script(self, *extra_args, all_roles=None, installer="agru", env=None):
        args = [
            str(SCRIPT),
            "--requirements-path", str(self.root / "requirements.yml"),
            "--roles-path", str(self.roles_path),
            "--state-path", str(self.state_path),
            "--installer", installer,
        ]
        if all_roles is not None:
            args += ["--all-requirements-path", str(self.requirements(all_roles, "all-requirements.yml"))]
        return subprocess.run(
            [*args, *extra_args],
            env={**self.env, **(env or {})},
            capture_output=True,
            text=True,
            timeout=60,
        )

    def install(self, roles, **kwargs):
        """Installs the given {name: version} roles through the script."""
        self.requirements(roles)
        result = self.run_script(**kwargs)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.log_path.unlink(missing_ok=True)
        return result

    def installer_calls(self):
        if not self.log_path.exists():
            return []
        return [tuple(line.split(" ")) for line in self.log_path.read_text().splitlines()]

    def version_of(self, name):
        return (self.roles_path / name / "tasks" / "main.yml").read_text().splitlines()[0].removeprefix("# ")

    def edit(self, name):
        with open(self.roles_path / name / "tasks" / "main.yml", "a") as file:
            file.write("# local edit\n")

    def assertEdited(self, name):
        self.assertIn("# local edit", (self.roles_path / name / "tasks" / "main.yml").read_text())

    def assertSucceeded(self, result):
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("Traceback", result.stdout + result.stderr)


class TestInstalling(InstallRolesTestCase):
    def test_installs_missing_roles(self):
        self.requirements({"a": "v1", "b": "v1"})
        result = self.run_script()
        self.assertSucceeded(result)
        self.assertEqual(self.installer_calls(), [("agru", "a,b")])
        self.assertEqual(self.version_of("a"), "v1")
        self.assertEqual(set(yaml.safe_load(self.state_path.read_text())["roles"]), {"a", "b"})

    def test_installs_only_missing_roles(self):
        self.install({"a": "v1"})
        self.requirements({"a": "v1", "b": "v1"})
        self.assertSucceeded(self.run_script())
        self.assertEqual(self.installer_calls(), [("agru", "b")])

    def test_up_to_date_roles_do_not_run_the_installer(self):
        self.install({"a": "v1"})
        result = self.run_script()
        self.assertSucceeded(result)
        self.assertEqual(self.installer_calls(), [])
        self.assertIn("up to date", result.stdout)

    def test_quiet_when_up_to_date(self):
        self.install({"a": "v1"})
        result = self.run_script("--quiet")
        self.assertSucceeded(result)
        self.assertEqual(result.stdout + result.stderr, "")

    def test_ansible_galaxy_only_gets_the_roles_to_install(self):
        self.install({"a": "v1", "b": "v1"}, installer="ansible-galaxy")
        self.edit("b")
        self.requirements({"a": "v2", "b": "v1", "c": "v1"})
        self.assertSucceeded(self.run_script(installer="ansible-galaxy"))
        self.assertEqual(self.installer_calls(), [("ansible-galaxy", "a,c")])
        self.assertEdited("b")

    def test_installer_failure(self):
        self.requirements({"a": "v1"})
        result = self.run_script(env={"FAKE_INSTALLER_FAIL": "1"})
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("Traceback", result.stderr)
        self.assertFalse(self.state_path.exists() and "a" in yaml.safe_load(self.state_path.read_text())["roles"])

    def test_other_files_in_the_roles_directory_are_ignored(self):
        self.roles_path.mkdir()
        (self.roles_path / ".gitkeep").write_text("")
        self.install({"a": "v1"})
        self.assertTrue((self.roles_path / ".gitkeep").exists())


class TestUpdating(InstallRolesTestCase):
    def test_replaces_outdated_roles(self):
        self.install({"a": "v1", "b": "v1"})
        self.requirements({"a": "v2", "b": "v1"})
        self.assertSucceeded(self.run_script())
        self.assertEqual(self.installer_calls(), [("agru", "a")])
        self.assertEqual(self.version_of("a"), "v2")

    def test_replaces_outdated_roles_installed_before(self):
        """Roles installed before this script recorded checksums are considered unchanged."""
        self.install({"a": "v1"})
        self.edit("a")
        self.state_path.unlink()
        self.requirements({"a": "v2"})
        self.assertSucceeded(self.run_script())
        self.assertEqual(self.version_of("a"), "v2")

    def test_keeps_outdated_roles_with_local_changes(self):
        self.install({"a": "v1"})
        self.edit("a")
        self.requirements({"a": "v2"})
        result = self.run_script()
        self.assertSucceeded(result)
        self.assertEqual(self.installer_calls(), [])
        self.assertEdited("a")
        self.assertIn("has local changes", result.stderr)
        self.assertIn("--force", result.stderr)

    def test_detects_added_and_removed_files(self):
        self.install({"a": "v1", "b": "v1"})
        (self.roles_path / "a" / "tasks" / "extra.yml").write_text("")
        (self.roles_path / "b" / "tasks" / "main.yml").unlink()
        self.requirements({"a": "v2", "b": "v2"})
        result = self.run_script()
        self.assertEqual(self.installer_calls(), [])
        self.assertEqual(result.stderr.count("has local changes"), 2)

    def test_detects_changed_executable_bit(self):
        self.install({"a": "v1"})
        (self.roles_path / "a" / "tasks" / "main.yml").chmod(0o755)
        self.requirements({"a": "v2"})
        self.assertIn("has local changes", self.run_script().stderr)

    def test_force_replaces_outdated_roles_with_local_changes(self):
        self.install({"a": "v1"})
        self.edit("a")
        self.requirements({"a": "v2"})
        self.assertSucceeded(self.run_script("--force"))
        self.assertEqual(self.version_of("a"), "v2")

    def test_keeps_up_to_date_roles_with_local_changes(self):
        self.install({"a": "v1"})
        self.edit("a")
        for extra_args in ((), ("--force",)):
            result = self.run_script(*extra_args)
            self.assertSucceeded(result)
            self.assertEqual(self.installer_calls(), [])
            self.assertEdited("a")
            self.assertEqual(result.stderr, "")

    def test_keeps_roles_not_installed_by_an_installer(self):
        """For example, a role copied there by hand."""
        (self.roles_path / "a" / "tasks").mkdir(parents=True)
        (self.roles_path / "a" / "tasks" / "main.yml").write_text("# local edit\n")
        self.requirements({"a": "v1"})
        result = self.run_script()
        self.assertSucceeded(result)
        self.assertEqual(self.installer_calls(), [])
        self.assertIn("was not installed by agru or ansible-galaxy", result.stderr)

        self.assertSucceeded(self.run_script("--force"))
        self.assertEqual(self.version_of("a"), "v1")


class TestDeveloperManagedRoles(InstallRolesTestCase):
    def test_symlinked_roles_are_never_touched(self):
        checkout_path = self.root / "ansible-role-a"
        (checkout_path / "tasks").mkdir(parents=True)
        (checkout_path / "tasks" / "main.yml").write_text("# work in progress\n")
        self.roles_path.mkdir()
        (self.roles_path / "a").symlink_to(checkout_path)
        self.requirements({"a": "v2"})

        for extra_args in ((), ("--force",)):
            result = self.run_script(*extra_args, all_roles={"a": "v2"})
            self.assertSucceeded(result)
            self.assertEqual(self.installer_calls(), [])
            self.assertTrue((self.roles_path / "a").is_symlink())
            self.assertEqual(result.stderr, "")

    def test_roles_with_a_git_directory_are_never_touched(self):
        self.install({"a": "v1"})
        (self.roles_path / "a" / ".git").mkdir()
        self.edit("a")
        self.requirements({"a": "v2"})
        result = self.run_script("--force")
        self.assertSucceeded(result)
        self.assertEqual(self.installer_calls(), [])
        self.assertEdited("a")


class TestDeleting(InstallRolesTestCase):
    def test_deletes_roles_no_longer_used(self):
        self.install({"a": "v1", "b": "v1"})
        self.requirements({"a": "v1"})
        result = self.run_script(all_roles={"a": "v1", "b": "v1"})
        self.assertSucceeded(result)
        self.assertFalse((self.roles_path / "b").exists())
        self.assertNotIn("b", yaml.safe_load(self.state_path.read_text())["roles"])

    def test_keeps_roles_no_longer_used_with_local_changes(self):
        self.install({"a": "v1", "b": "v1"})
        self.edit("b")
        self.requirements({"a": "v1"})
        result = self.run_script(all_roles={"a": "v1", "b": "v1"})
        self.assertSucceeded(result)
        self.assertEdited("b")
        self.assertIn("no longer used, but has local changes", result.stderr)

        self.assertSucceeded(self.run_script("--force", all_roles={"a": "v1", "b": "v1"}))
        self.assertFalse((self.roles_path / "b").exists())

    def test_never_deletes_unknown_roles(self):
        """For example, a new role being developed, which is not in the playbook yet."""
        self.install({"a": "v1", "new": "v1"})
        self.requirements({"a": "v1"})
        result = self.run_script("--force", all_roles={"a": "v1"})
        self.assertSucceeded(result)
        self.assertTrue((self.roles_path / "new").exists())
        self.assertEqual(result.stderr, "")

    def test_without_all_requirements_nothing_is_deleted(self):
        self.install({"a": "v1", "b": "v1"})
        self.requirements({"a": "v1"})
        self.assertSucceeded(self.run_script("--force"))
        self.assertTrue((self.roles_path / "b").exists())


class TestDependencies(unittest.TestCase):
    def test_only_standard_library_and_pyyaml(self):
        tree = ast.parse(SCRIPT.read_text())
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module.split(".")[0])
        third_party = imported - set(sys.stdlib_module_names) - {"yaml"}
        self.assertEqual(third_party, set())

if __name__ == "__main__":
    unittest.main()
