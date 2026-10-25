#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 MASH project contributors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# Tests for playbook optimization (bin/optimize.py and the justfile recipes around it).
#
# Each test copies the justfile, bin/optimize.py and the real templates into a temporary
# playbook directory under var/tests/optimize/, builds an inventory there and runs the actual `just` recipes.
# Using the real templates also checks their `role-specific` markers.
#
# Requires `just` (also found as `rust-just`, or set via the `JUST` environment variable) and PyYAML.
# Run directly (`tests/optimize/test_optimize.py`) or via the `test-optimize` pre-commit hook.

import ast
import os
import shutil
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[2]

# Each test's temporary playbook goes here (var/ is gitignored) and is removed afterwards.
TMP_ROOT = REPO / "var" / "tests" / "optimize"


def find_just(path=None):
    """Finds `just`, which some package managers (e.g. pip and npm) install as `rust-just`."""
    return os.environ.get("JUST") or shutil.which("just", path=path) or shutil.which("rust-just", path=path)


JUST = find_just()
if JUST is None:
    sys.exit("These tests require `just` (or `rust-just`) on PATH, or its path in the `JUST` environment variable")

FULLY_ENCRYPTED = "$ANSIBLE_VAULT;1.1;AES256\n3138353063616561616264653633353761\n"

INLINE_VAULT = textwrap.dedent("""\
    some_secret: !vault |
      $ANSIBLE_VAULT;1.1;AES256
      3138353063616561616264653633353761
    """)


class Playbook:
    """A throwaway playbook directory with an inventory under `inventory/`."""

    def __init__(self, root):
        self.root = root
        (root / "bin").mkdir(parents=True)
        (root / "run").mkdir()
        (root / "group_vars").mkdir()
        shutil.copy(REPO / "justfile", root / "justfile")
        shutil.copy(REPO / "bin" / "optimize.py", root / "bin" / "optimize.py")
        shutil.copy(REPO / "bin" / "install-roles.py", root / "bin" / "install-roles.py")
        shutil.copy(REPO / "bin" / "ansible-python.sh", root / "bin" / "ansible-python.sh")
        shutil.copytree(REPO / "templates", root / "templates")
        self.inventory = root / "inventory"

    def write(self, relative_path, content, base=None):
        path = (base or self.inventory) / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        return path

    def hosts(self, content):
        self.write("hosts", textwrap.dedent(content))

    def just(self, *args, env=None):
        full_env = {k: v for k, v in os.environ.items() if k != "ANSIBLE_INVENTORY"}
        full_env.update(env or {})
        return subprocess.run(
            [JUST, "--justfile", str(self.root / "justfile"), *args],
            cwd=self.root,
            env=full_env,
            capture_output=True,
            text=True,
            timeout=120,
        )

    def touch_template(self, name="setup.yml"):
        """Simulates a playbook update changing a template (outside of any `role-specific` block)."""
        with open(self.root / "templates" / name, "a") as file:
            file.write("\n# changed by an update\n")

    def requirements_roles(self):
        definitions = yaml.safe_load((self.root / "requirements.yml").read_text())
        return {definition["name"] for definition in definitions}

    def setup_roles(self):
        plays = yaml.safe_load((self.root / "setup.yml").read_text())
        roles = set()
        for play in plays:
            for entry in play.get("roles", []):
                role = entry["role"]
                if role.startswith("galaxy/"):
                    roles.add(role.removeprefix("galaxy/"))
        return roles


class OptimizeTestCase(unittest.TestCase):
    def setUp(self):
        TMP_ROOT.mkdir(parents=True, exist_ok=True)
        tmp = tempfile.TemporaryDirectory(prefix="test-", dir=TMP_ROOT)
        self.addCleanup(tmp.cleanup)
        self.pb = Playbook(Path(tmp.name))

    def standard_inventory(self):
        """Two hosts: `a` runs Miniflux, `b` runs Gitea."""
        self.pb.hosts("""\
            [mash_servers]
            a
            b
            """)
        self.pb.write("host_vars/a/vars.yml", "mash_playbook_generic_secret_key: x\nminiflux_enabled: true\n")
        self.pb.write("host_vars/b/vars.yml", "mash_playbook_generic_secret_key: x\ngitea_enabled: true\n")

    def assertSucceeded(self, result):
        self.assertEqual(
            result.returncode, 0,
            "command failed:\n--- stdout\n{0}\n--- stderr\n{1}".format(result.stdout, result.stderr),
        )
        self.assertNotIn("Traceback", result.stdout + result.stderr)

    def assertFailedCleanly(self, result):
        self.assertNotEqual(result.returncode, 0, "command unexpectedly succeeded:\n" + result.stdout)
        self.assertNotIn("Traceback", result.stdout + result.stderr)

    def assertConsistent(self):
        """Every role that setup.yml uses must be among the roles that requirements.yml installs."""
        missing = self.pb.setup_roles() - self.pb.requirements_roles()
        self.assertEqual(missing, set(), "setup.yml uses roles missing from requirements.yml")

    def assertEnabled(self, *roles):
        self.assertConsistent()
        enabled = self.pb.requirements_roles()
        for role in roles:
            self.assertIn(role, enabled)

    def assertNotEnabled(self, *roles):
        enabled = self.pb.requirements_roles()
        for role in roles:
            self.assertNotIn(role, enabled)


class TestInventoryLocation(OptimizeTestCase):
    def test_default_inventory(self):
        self.standard_inventory()
        self.assertSucceeded(self.pb.just("optimize-enable"))
        self.assertEnabled("miniflux", "gitea")
        self.assertNotEnabled("nextcloud")

    def other_inventory(self, name="other-inventory"):
        """An inventory outside the playbook directory, which only enables Nextcloud."""
        self.pb.hosts("[mash_servers]\n")
        other = self.pb.root / name
        self.pb.write("hosts", "[mash_servers]\nc\n", base=other)
        self.pb.write("host_vars/c/vars.yml", "nextcloud_enabled: true\n", base=other)
        return other

    def test_ansible_inventory_hosts_file(self):
        other = self.other_inventory()
        self.assertSucceeded(self.pb.just("optimize-enable", env={"ANSIBLE_INVENTORY": str(other / "hosts")}))
        self.assertEnabled("nextcloud")

    def test_ansible_inventory_directory(self):
        other = self.other_inventory()
        self.assertSucceeded(self.pb.just("optimize-enable", env={"ANSIBLE_INVENTORY": str(other)}))
        self.assertEnabled("nextcloud")

    def test_inventory_path_with_space(self):
        other = self.other_inventory("my inventory")
        self.assertSucceeded(self.pb.just("optimize-enable", env={"ANSIBLE_INVENTORY": str(other / "hosts")}))
        self.assertEnabled("nextcloud")

    def test_reoptimization_follows_ansible_inventory(self):
        """One playbook used with several inventories is re-optimized for the one being used."""
        self.standard_inventory()
        self.assertSucceeded(self.pb.just("optimize-enable"))

        other = self.pb.root / "other-inventory"
        self.pb.write("hosts", "[mash_servers]\nc\n", base=other)
        self.pb.write("host_vars/c/vars.yml", "nextcloud_enabled: true\n", base=other)

        self.assertSucceeded(self.pb.just("_prepare-files", env={"ANSIBLE_INVENTORY": str(other / "hosts")}))
        self.assertEnabled("nextcloud")
        self.assertNotEnabled("miniflux", "gitea")

    def test_no_variable_files_includes_all_roles(self):
        self.pb.hosts("[mash_servers]\na\n")
        result = self.pb.just("_prepare-files")
        self.assertSucceeded(result)
        self.assertIn("including all roles", result.stderr)
        self.assertEnabled("miniflux", "gitea", "nextcloud")

    def test_missing_inventory_includes_all_roles(self):
        """For example, before the inventory is created."""
        result = self.pb.just("_prepare-files", env={"ANSIBLE_INVENTORY": str(self.pb.root / "no-such-inventory" / "hosts")})
        self.assertSucceeded(result)
        self.assertIn("ANSIBLE_INVENTORY", result.stderr)
        self.assertEnabled("miniflux", "gitea", "nextcloud")

    def test_optimized_by_default(self):
        self.standard_inventory()
        result = self.pb.just("_prepare-files")
        self.assertSucceeded(result)
        self.assertEqual(result.stderr, "")
        self.assertEnabled("miniflux", "gitea")
        self.assertNotEnabled("nextcloud")


class TestInventoryChanges(OptimizeTestCase):
    def test_removed_host_on_next_run(self):
        self.standard_inventory()
        self.assertSucceeded(self.pb.just("optimize-enable"))

        shutil.rmtree(self.pb.inventory / "host_vars" / "b")
        self.pb.hosts("[mash_servers]\na\n")

        self.assertSucceeded(self.pb.just("_prepare-files"))
        self.assertEnabled("miniflux")
        self.assertNotEnabled("gitea")

    def test_added_host_on_next_run(self):
        self.standard_inventory()
        self.assertSucceeded(self.pb.just("optimize-enable"))

        self.pb.hosts("[mash_servers]\na\nb\nc\n")
        self.pb.write("host_vars/c/vars.yml", "nextcloud_enabled: true\n")

        self.assertSucceeded(self.pb.just("_prepare-files"))
        self.assertEnabled("miniflux", "gitea", "nextcloud")

    def test_enabled_service_on_next_run(self):
        self.standard_inventory()
        self.assertSucceeded(self.pb.just("optimize-enable"))

        with open(self.pb.inventory / "host_vars" / "a" / "vars.yml", "a") as file:
            file.write("nextcloud_enabled: true\n")

        self.assertSucceeded(self.pb.just("_prepare-files"))
        self.assertEnabled("miniflux", "gitea", "nextcloud")
        self.assertIn("nextcloud", self.pb.setup_roles())

    def test_template_change_on_next_run(self):
        self.standard_inventory()
        self.assertSucceeded(self.pb.just("optimize-enable"))
        self.pb.touch_template()

        self.assertSucceeded(self.pb.just("_prepare-files"))
        self.assertIn("# changed by an update", (self.pb.root / "setup.yml").read_text())
        self.assertNotEnabled("nextcloud")

    def test_unchanged_files_are_not_rewritten(self):
        self.standard_inventory()
        self.assertSucceeded(self.pb.just("optimize-enable"))
        generated = [self.pb.root / "requirements.yml", self.pb.root / "setup.yml", self.pb.root / "group_vars" / "mash_servers"]
        modification_times = [path.stat().st_mtime_ns for path in generated]

        self.assertSucceeded(self.pb.just("_prepare-files"))
        self.assertEqual([path.stat().st_mtime_ns for path in generated], modification_times)

    def test_leftover_markers_are_removed(self):
        """Older versions marked optimization as enabled. It is now enabled unless disabled."""
        self.standard_inventory()
        run = self.pb.root / "run"
        (run / "optimization-enabled").write_text("")
        (run / "optimization-vars-files.state").write_text("/no/longer/existing/host_vars/x/vars.yml\n")

        self.assertSucceeded(self.pb.just("_prepare-files"))
        self.assertEnabled("miniflux", "gitea")
        self.assertNotEnabled("nextcloud")
        self.assertFalse((run / "optimization-enabled").exists())
        self.assertFalse((run / "optimization-vars-files.state").exists())

    def test_deleted_generated_file_is_regenerated_optimized(self):
        self.standard_inventory()
        self.assertSucceeded(self.pb.just("optimize-enable"))
        (self.pb.root / "setup.yml").unlink()

        self.assertSucceeded(self.pb.just("_prepare-files"))
        self.assertEnabled("miniflux", "gitea")
        self.assertNotIn("nextcloud", self.pb.setup_roles())

    def test_failed_reoptimization_does_not_leave_mismatched_files(self):
        self.standard_inventory()
        self.assertSucceeded(self.pb.just("optimize-enable"))

        # An unknown role name in a marker makes the optimization fail.
        with open(self.pb.root / "templates" / "setup.yml", "a") as file:
            file.write("\n    # role-specific:no_such_role\n    # /role-specific:no_such_role\n")
        self.assertNotEqual(self.pb.just("_prepare-files").returncode, 0)

        # Running again must retry (and fail again), not continue with an unoptimized setup.yml
        # and an optimized requirements.yml.
        self.assertNotEqual(self.pb.just("_prepare-files").returncode, 0)
        self.assertConsistent()

    def test_optimize_disable_and_enable(self):
        self.standard_inventory()
        self.assertSucceeded(self.pb.just("optimize-disable"))
        self.assertTrue((self.pb.root / "run" / "optimization-disabled").exists())
        self.assertEqual(
            (self.pb.root / "setup.yml").read_text(),
            (self.pb.root / "templates" / "setup.yml").read_text(),
        )

        # It stays disabled on the next runs
        self.assertSucceeded(self.pb.just("_prepare-files"))
        self.assertIn("nextcloud", self.pb.setup_roles())

        self.assertSucceeded(self.pb.just("optimize-enable"))
        self.assertFalse((self.pb.root / "run" / "optimization-disabled").exists())
        self.assertNotEnabled("nextcloud")

    def test_templates_are_used_as_they_are_without_optimization(self):
        self.standard_inventory()
        self.assertSucceeded(self.pb.just("optimize-disable"))
        self.pb.touch_template()

        self.assertSucceeded(self.pb.just("_prepare-files"))
        for template_name, generated_path in (
            ("requirements.yml", "requirements.yml"),
            ("setup.yml", "setup.yml"),
            ("group_vars_mash_servers", "group_vars/mash_servers"),
        ):
            self.assertEqual(
                (self.pb.root / generated_path).read_text(),
                (self.pb.root / "templates" / template_name).read_text(),
            )

    def test_leftover_hash_files_are_removed(self):
        self.standard_inventory()
        (self.pb.root / "run" / "setup.yml.srchash").write_text("0123\n")
        self.assertSucceeded(self.pb.just("_prepare-files"))
        self.assertEqual(list((self.pb.root / "run").glob("*.srchash")), [])


class TestVariableFileContents(OptimizeTestCase):
    def test_empty_file(self):
        self.standard_inventory()
        self.pb.write("host_vars/b/vars.yml", "")
        self.assertSucceeded(self.pb.just("optimize-enable"))
        self.assertEnabled("miniflux")

    def test_comments_only_file(self):
        self.standard_inventory()
        self.pb.write("host_vars/b/vars.yml", "---\n# gitea_enabled: true\n")
        self.assertSucceeded(self.pb.just("optimize-enable"))
        self.assertEnabled("miniflux")
        self.assertNotEnabled("gitea")

    def test_non_mapping_file(self):
        self.standard_inventory()
        self.pb.write("host_vars/b/vars.yml", "- gitea_enabled\n")
        self.assertSucceeded(self.pb.just("optimize-enable"))
        self.assertEnabled("miniflux")

    def test_inline_vault_value(self):
        self.standard_inventory()
        self.pb.write("host_vars/a/vars.yml", "miniflux_enabled: true\n" + INLINE_VAULT)
        self.assertSucceeded(self.pb.just("optimize-enable"))
        self.assertEnabled("miniflux", "gitea")

    def test_invalid_yaml_is_skipped_with_warning(self):
        self.standard_inventory()
        self.pb.write("host_vars/b/broken.yml", "nextcloud_enabled: [\n")
        result = self.pb.just("optimize-enable")
        self.assertSucceeded(result)
        self.assertIn("broken.yml", result.stderr)
        self.assertEnabled("miniflux", "gitea")

    def test_fully_encrypted_file_is_skipped_silently(self):
        self.standard_inventory()
        self.pb.write("host_vars/b/vault.yml", FULLY_ENCRYPTED)
        result = self.pb.just("optimize-enable")
        self.assertSucceeded(result)
        self.assertNotIn("vault.yml", result.stdout + result.stderr)
        self.assertEnabled("miniflux", "gitea")


class TestVariableFileLayouts(OptimizeTestCase):
    def test_flat_host_vars_file(self):
        self.standard_inventory()
        shutil.rmtree(self.pb.inventory / "host_vars" / "b")
        self.pb.write("host_vars/b.yml", "gitea_enabled: true\n")
        self.assertSucceeded(self.pb.just("optimize-enable"))
        self.assertEnabled("miniflux", "gitea")

    def test_flat_host_vars_file_named_after_a_domain(self):
        """Ansible picks flat files by host name, so `example.com` is a variable file despite its "extension"."""
        self.standard_inventory()
        shutil.rmtree(self.pb.inventory / "host_vars" / "b")
        self.pb.write("host_vars/b.example.com", "gitea_enabled: true\n")
        self.assertSucceeded(self.pb.just("optimize-enable"))
        self.assertEnabled("miniflux", "gitea")

    def test_additional_files_in_host_vars_directory(self):
        self.standard_inventory()
        self.pb.write("host_vars/a/nextcloud.yml", "nextcloud_enabled: true\n")
        self.pb.write("host_vars/a/services/syncthing.yaml", "syncthing_enabled: true\n")
        self.assertSucceeded(self.pb.just("optimize-enable"))
        self.assertEnabled("miniflux", "gitea", "nextcloud", "syncthing")

    def test_group_vars_layouts(self):
        self.pb.hosts("""\
            [mash_servers:children]
            web
            db

            [web]
            a

            [db]
            b
            """)
        self.pb.write("host_vars/a/vars.yml", "mash_playbook_generic_secret_key: x\n")
        self.pb.write("group_vars/all.yml", "miniflux_enabled: true\n")
        self.pb.write("group_vars/mash_servers/vars.yml", "aux_file_definitions_custom: []\n")
        self.pb.write("group_vars/web", "nextcloud_enabled: true\n")
        self.pb.write("group_vars/db.yaml", "gitea_enabled: true\n")
        self.assertSucceeded(self.pb.just("optimize-enable"))
        self.assertEnabled("miniflux", "auxiliary", "nextcloud", "gitea")

    def test_group_vars_without_host_vars(self):
        self.pb.hosts("[mash_servers]\na\n")
        self.pb.write("group_vars/mash_servers.yml", "miniflux_enabled: true\n")
        self.assertSucceeded(self.pb.just("optimize-enable"))
        self.assertEnabled("miniflux")

    def test_playbook_group_vars_and_host_vars(self):
        """Ansible reads the playbook's own group_vars/ and host_vars/ too (and its group_vars/<group> overrides mash_servers)."""
        self.standard_inventory()
        self.pb.write("group_vars/web.yml", "nextcloud_enabled: true\n", base=self.pb.root)
        self.pb.write("host_vars/a.yml", "syncthing_enabled: true\n", base=self.pb.root)
        self.assertSucceeded(self.pb.just("optimize-enable"))
        self.assertEnabled("miniflux", "gitea", "nextcloud", "syncthing")

    def test_generated_group_vars_file_is_ignored(self):
        """Variables in the generated group_vars/mash_servers do not count, so roles dropped from it stay dropped."""
        self.standard_inventory()
        self.assertSucceeded(self.pb.just("optimize-disable"))
        self.assertSucceeded(self.pb.just("optimize-enable"))
        self.assertEnabled("miniflux", "gitea")
        self.assertNotEnabled("nextcloud", "syncthing")

    def test_files_ansible_does_not_load_are_ignored(self):
        self.standard_inventory()
        self.pb.write("host_vars/a/notes.txt", "nextcloud_enabled: true\n")
        self.pb.write("host_vars/a/vars.yml~", "syncthing_enabled: true\n")
        self.pb.write("host_vars/a/.vars.yml.swp", "vaultwarden_enabled: true\n")
        # Like Ansible, do not descend into directories with an extension
        self.pb.write("host_vars/a/etc/nginx/conf.d/uptime.yml", "uptime_kuma_enabled: true\n")
        self.assertSucceeded(self.pb.just("optimize-enable"))
        self.assertEnabled("miniflux", "gitea")
        self.assertNotEnabled("nextcloud", "syncthing", "vaultwarden", "uptime_kuma")

    def test_asset_files_are_ignored_quietly(self):
        """Inventories often keep templates and other files for their own tasks in host_vars/<host>/."""
        self.standard_inventory()
        self.pb.write("host_vars/a/etc/systemd/system/backup.service.j2", "[Unit]\nDescription={{ x }}\n")
        self.pb.write("host_vars/a/root/bin/backup.sh", "#!/bin/sh\necho 'nextcloud_enabled: true'\n")
        self.pb.write("host_vars/a/docs/README.md", "# Notes\n")
        self.pb.write("host_vars/a/root/ssh/id_ed25519", "")
        result = self.pb.just("optimize-enable")
        self.assertSucceeded(result)
        self.assertEqual(result.stderr, "")
        self.assertEnabled("miniflux", "gitea")
        self.assertNotEnabled("nextcloud")


class TestTemplates(OptimizeTestCase):
    """Checks the real templates, so that broken `role-specific` markers are caught when they change."""

    def all_prefixes(self):
        definitions = yaml.safe_load((REPO / "templates" / "requirements.yml").read_text())
        return {definition["activation_prefix"] for definition in definitions} - {""}

    def assertGeneratedFilesParse(self):
        yaml.safe_load((self.pb.root / "setup.yml").read_text())
        yaml.safe_load((self.pb.root / "group_vars" / "mash_servers").read_text())

    def test_all_roles(self):
        self.pb.hosts("[mash_servers]\na\n")
        self.pb.write(
            "host_vars/a/vars.yml",
            "".join("{0}optimize_test: true\n".format(prefix) for prefix in sorted(self.all_prefixes())),
        )
        self.assertSucceeded(self.pb.just("optimize-enable"))
        self.assertConsistent()
        self.assertGeneratedFilesParse()

        definitions = yaml.safe_load((REPO / "templates" / "requirements.yml").read_text())
        self.assertEqual(self.pb.requirements_roles(), {definition["name"] for definition in definitions})

    def test_minimal_roles(self):
        self.pb.hosts("[mash_servers]\na\n")
        self.pb.write("host_vars/a/vars.yml", "mash_playbook_generic_secret_key: x\n")
        self.assertSucceeded(self.pb.just("optimize-enable"))
        self.assertConsistent()
        self.assertGeneratedFilesParse()


class TestRoleInstallation(OptimizeTestCase):
    """Runs `just roles` and `just update` with a fake `agru`, which records how it was called."""

    GIT_ENV = {
        "GIT_AUTHOR_NAME": "Test",
        "GIT_AUTHOR_EMAIL": "test@example.com",
        "GIT_COMMITTER_NAME": "Test",
        "GIT_COMMITTER_EMAIL": "test@example.com",
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_CONFIG_NOSYSTEM": "1",
    }

    def setUp(self):
        super().setUp()
        self.standard_inventory()
        self.assertSucceeded(self.pb.just("optimize-enable"))

        bin_path = self.pb.root.parent / (self.pb.root.name + "-bin")
        bin_path.mkdir()
        self.addCleanup(shutil.rmtree, bin_path)
        self.agru_log_path = bin_path / "agru.log"
        agru_path = bin_path / "agru"
        agru_path.write_text(textwrap.dedent("""\
            #!/usr/bin/env python3
            # Records the arguments and the role names in the file passed via -r,
            # and "installs" them like agru does (with their version in meta/.galaxy_install_info)
            import os, sys, yaml
            arguments = sys.argv[1:]
            definitions = []
            if "-r" in arguments:
                definitions = yaml.safe_load(open(arguments[arguments.index("-r") + 1]))
            with open({log!r}, "a") as log:
                log.write("args: " + " ".join(arguments) + "\\n")
                log.write(" ".join("name: " + definition["name"] for definition in definitions) + "\\n")
            if "-i=false" not in arguments and "-p" in arguments:
                roles_path = arguments[arguments.index("-p") + 1]
                for definition in definitions:
                    meta_path = os.path.join(roles_path, definition["name"], "meta")
                    os.makedirs(meta_path, exist_ok=True)
                    with open(os.path.join(meta_path, ".galaxy_install_info"), "w") as file:
                        file.write("version: {{0}}\\n".format(definition["version"]))
            """).format(log=str(self.agru_log_path)))
        agru_path.chmod(0o755)
        self.ansible_playbook_log_path = bin_path / "ansible-playbook.log"
        ansible_playbook_path = bin_path / "ansible-playbook"
        ansible_playbook_path.write_text(textwrap.dedent("""\
            #!/bin/sh
            # bin/ansible-python.sh asks wrapper scripts like this one for their interpreter. Do not record that.
            if [ "${{1:-}}" = "--version" ]; then
                exit 0
            fi
            # Records that it ran, and how many roles were installed at that point
            echo "roles installed: $(ls roles/galaxy | wc -l)" >> {log}
            """).format(log=self.ansible_playbook_log_path))
        ansible_playbook_path.chmod(0o755)
        self.env = {"PATH": "{0}:{1}".format(bin_path, os.environ["PATH"]), **self.GIT_ENV}

    def git(self, *args, cwd):
        subprocess.run(["git", *args], cwd=cwd, env={**os.environ, **self.GIT_ENV}, check=True, capture_output=True)

    def agru_calls(self):
        """Returns (arguments, role names) for each call of the fake agru."""
        lines = self.agru_log_path.read_text().splitlines()
        return [(lines[i].removeprefix("args: "), lines[i + 1]) for i in range(0, len(lines), 2)]

    def test_roles_installs_optimized_roles(self):
        self.assertSucceeded(self.pb.just("roles", env=self.env))
        [(args, roles)] = self.agru_calls()
        self.assertIn("name: miniflux", roles)
        self.assertNotIn("name: nextcloud", roles)

    def test_run_installs_missing_roles_first(self):
        self.assertSucceeded(self.pb.just("run", "--tags=setup-all", env=self.env))
        [(args, roles)] = self.agru_calls()
        self.assertIn("name: miniflux", roles)
        self.assertNotIn("name: nextcloud", roles)
        self.assertNotIn("roles installed: 0", self.ansible_playbook_log_path.read_text())

        # Nothing is installed again, and nothing is reported
        result = self.pb.just("run", "--tags=setup-all", env=self.env)
        self.assertSucceeded(result)
        self.assertEqual(len(self.agru_calls()), 1)
        self.assertEqual(result.stderr, "")

    def make_clone_with_upstream_change(self):
        """Turns the playbook into a clone of an upstream repository, which then gets a template change."""
        upstream_path = self.pb.root.parent / (self.pb.root.name + "-upstream.git")
        work_path = self.pb.root.parent / (self.pb.root.name + "-work")
        self.addCleanup(shutil.rmtree, upstream_path)
        self.addCleanup(shutil.rmtree, work_path)
        (self.pb.root / ".gitignore").write_text("/inventory\n/run/\n/requirements.yml\n/setup.yml\n/group_vars/mash_servers\n")
        self.git("init", "-q", "-b", "main", cwd=self.pb.root)
        self.git("add", ".", cwd=self.pb.root)
        self.git("commit", "-q", "-m", "Initial", cwd=self.pb.root)
        self.git("clone", "-q", "--bare", str(self.pb.root), str(upstream_path), cwd=self.pb.root)
        self.git("remote", "add", "origin", str(upstream_path), cwd=self.pb.root)
        self.git("fetch", "-q", "origin", cwd=self.pb.root)
        self.git("branch", "-q", "--set-upstream-to=origin/main", cwd=self.pb.root)
        self.git("clone", "-q", str(upstream_path), str(work_path), cwd=self.pb.root)
        with open(work_path / "templates" / "setup.yml", "a") as file:
            file.write("\n# changed upstream\n")
        self.git("commit", "-q", "-am", "Change", cwd=work_path)
        self.git("push", "-q", "origin", "main", cwd=work_path)

    def test_update_prepares_files_after_pulling(self):
        self.make_clone_with_upstream_change()
        self.assertSucceeded(self.pb.just("update", env=self.env))
        self.assertIn("# changed upstream", (self.pb.root / "setup.yml").read_text())
        [(args, roles)] = self.agru_calls()
        self.assertIn("name: miniflux", roles)
        self.assertNotIn("name: nextcloud", roles)

    def test_update_with_unknown_flags_fails_before_pulling(self):
        self.make_clone_with_upstream_change()
        result = self.pb.just("update", "--bogus", env=self.env)
        self.assertFailedCleanly(result)
        self.assertNotIn("# changed upstream", (self.pb.root / "templates" / "setup.yml").read_text())
        self.assertFalse(self.agru_log_path.exists())


class TestDependencies(unittest.TestCase):
    def test_only_standard_library_and_pyyaml(self):
        tree = ast.parse((REPO / "bin" / "optimize.py").read_text())
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
