#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 MASH project contributors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# Tests for bin/ansible-python.sh, which runs Python using the interpreter which runs Ansible.
#
# Each test puts a fake `ansible-playbook` (with a given shebang) and fake Python interpreters on a minimal PATH.
# The fake interpreters print their name and arguments, so the tests can tell which one was used.
#
# Run directly (`tests/ansible_python/test_ansible_python.py`) or via the `test-ansible-python` pre-commit hook.

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCRIPT = REPO / "bin" / "ansible-python.sh"

# Each test's files go here (var/ is gitignored) and are removed afterwards.
TMP_ROOT = REPO / "var" / "tests" / "ansible_python"


class AnsiblePythonTestCase(unittest.TestCase):
    def setUp(self):
        TMP_ROOT.mkdir(parents=True, exist_ok=True)
        tmp = tempfile.TemporaryDirectory(prefix="test-", dir=TMP_ROOT)
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)

        # A minimal PATH, so that the system's ansible-playbook and python3 are not found
        self.bin_path = self.root / "bin"
        self.bin_path.mkdir()
        for tool in ("sh", "head", "basename"):
            (self.bin_path / tool).symlink_to(shutil.which(tool))
        self.fake_python("python3")

    def fake_python(self, name, directory=None):
        """Creates a fake Python interpreter, which prints its name and arguments."""
        path = (directory or self.bin_path) / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('#!/bin/sh\necho "{0}"; for argument in "$@"; do echo "[$argument]"; done\n'.format(name))
        path.chmod(0o755)
        return path

    def fake_ansible_playbook(self, shebang):
        path = self.bin_path / "ansible-playbook"
        path.write_text(shebang + "\n# ansible-playbook\n")
        path.chmod(0o755)

    def run_script(self, *args):
        result = subprocess.run(
            [str(self.bin_path / "sh"), str(SCRIPT), *args],
            env={"PATH": str(self.bin_path)},
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout.splitlines()

    def test_uses_the_interpreter_in_the_shebang(self):
        pipx_python = self.fake_python("python3.12", self.root / "pipx" / "venvs" / "ansible" / "bin")
        self.fake_ansible_playbook("#!{0}".format(pipx_python))
        self.assertEqual(self.run_script("script.py", "an argument"), ["python3.12", "[script.py]", "[an argument]"])

    def test_uses_the_interpreter_named_through_env(self):
        self.fake_python("python3.13")
        self.fake_ansible_playbook("#!/usr/bin/env python3.13")
        self.assertEqual(self.run_script("script.py")[0], "python3.13")

    def test_keeps_shebang_options_out_of_the_arguments(self):
        system_python = self.fake_python("python3.11", self.root / "usr" / "bin")
        self.fake_ansible_playbook("#!{0} -E".format(system_python))
        self.assertEqual(self.run_script("script.py"), ["python3.11", "[script.py]"])

    def test_falls_back_to_python3_for_wrapper_scripts(self):
        self.fake_ansible_playbook("#!/bin/sh")
        self.assertEqual(self.run_script("script.py")[0], "python3")

    def test_falls_back_to_python3_for_missing_interpreters(self):
        self.fake_ansible_playbook("#!/nonexistent/python3.12")
        self.assertEqual(self.run_script("script.py")[0], "python3")

    def test_falls_back_to_python3_without_ansible(self):
        self.assertEqual(self.run_script("script.py")[0], "python3")


if __name__ == "__main__":
    unittest.main()
