#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 MASH project contributors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# Tests for playbook optimization (bin/optimize.py and the justfile recipes around it).
#
# Each test copies the justfile, bin/optimize.py and the real components into a temporary
# playbook directory under var/tests/optimize/, builds an inventory there and runs the actual `just` recipes.
# Using the real components also checks that they are valid.
#
# Requires `just` (also found as `rust-just`, or set via the `JUST` environment variable) and PyYAML.
# Run directly (`tests/optimize/test_optimize.py`) or via the `test-optimize` pre-commit hook.

import ast
import gzip
import os
import re
import shlex
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


def clean_environment():
    """The environment without variables that point git at another repository.

    Git hooks (e.g. pre-commit, which runs these tests) export GIT_DIR, GIT_INDEX_FILE and others.
    Inherited, they would make the git commands of the tests (and of `just update`) act on the
    playbook's own repository instead of the temporary ones.
    """
    return {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}


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
        shutil.copytree(REPO / "components", root / "components")
        self.inventory = root / "inventory"

    def write(self, relative_path, content, base=None):
        path = (base or self.inventory) / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        return path

    def hosts(self, content):
        self.write("hosts", textwrap.dedent(content))

    def just(self, *args, env=None):
        full_env = {k: v for k, v in clean_environment().items() if k != "ANSIBLE_INVENTORY"}
        full_env.update(env or {})
        return subprocess.run(
            [JUST, "--justfile", str(self.root / "justfile"), *args],
            cwd=self.root,
            env=full_env,
            capture_output=True,
            text=True,
            timeout=120,
        )

    def touch_component(self, relative_path="miniflux/wiring.yml"):
        """Simulates a playbook update changing a component."""
        with open(self.root / "components" / relative_path, "a") as file:
            file.write("\n# changed by an update\n")

    def group_vars_files(self):
        """The generated group_vars/mash_servers/ files, relative to it."""
        path = self.root / "group_vars" / "mash_servers"
        return {str(file.relative_to(path)) for file in path.rglob("*") if file.is_file()}

    def component_requirements(self):
        """The names of all roles the components require."""
        return {
            definition["name"]
            for path in (self.root / "components").glob("*/requirements.yml")
            for definition in yaml.safe_load(path.read_text())
        }

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
        self.assertIn("including all components", result.stderr)
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

    def test_component_change_on_next_run(self):
        self.standard_inventory()
        self.assertSucceeded(self.pb.just("optimize-enable"))
        self.pb.touch_component()

        self.assertSucceeded(self.pb.just("_prepare-files"))
        self.assertIn("# changed by an update", (self.pb.root / "group_vars" / "mash_servers" / "miniflux" / "wiring.yml").read_text())
        self.assertNotEnabled("nextcloud")

    def test_unchanged_files_are_not_rewritten(self):
        self.standard_inventory()
        self.assertSucceeded(self.pb.just("optimize-enable"))
        group_vars_path = self.pb.root / "group_vars" / "mash_servers"
        generated = [self.pb.root / "requirements.yml", self.pb.root / "setup.yml"]
        generated += [group_vars_path / relative_path for relative_path in sorted(self.pb.group_vars_files())]
        modification_times = [path.stat().st_mtime_ns for path in generated]

        self.assertSucceeded(self.pb.just("_prepare-files"))
        self.assertEqual([path.stat().st_mtime_ns for path in generated], modification_times)

    def test_files_of_components_no_longer_in_use_are_removed(self):
        self.standard_inventory()
        with open(self.pb.inventory / "host_vars" / "a" / "vars.yml", "a") as file:
            file.write("nextcloud_enabled: true\n")
        self.assertSucceeded(self.pb.just("optimize-enable"))
        self.assertIn("nextcloud/wiring.yml", self.pb.group_vars_files())

        self.pb.write("host_vars/a/vars.yml", "mash_playbook_generic_secret_key: x\nminiflux_enabled: true\n")
        self.assertSucceeded(self.pb.just("_prepare-files"))
        self.assertFalse((self.pb.root / "group_vars" / "mash_servers" / "nextcloud").exists())
        self.assertIn("miniflux/wiring.yml", self.pb.group_vars_files())

    def test_group_vars_file_of_older_versions_is_replaced(self):
        """Older versions generated group_vars/mash_servers as a single file."""
        self.standard_inventory()
        (self.pb.root / "group_vars" / "mash_servers").write_text("miniflux_enabled: false\n")
        self.assertSucceeded(self.pb.just("_prepare-files"))
        self.assertIn("miniflux/wiring.yml", self.pb.group_vars_files())

    def test_directory_not_generated_by_us_is_kept(self):
        """A directory without our marker (e.g. a mistyped destination) is never cleaned up."""
        self.standard_inventory()
        user_file = self.pb.root / "group_vars" / "mash_servers" / "mine.yml"
        user_file.parent.mkdir()
        user_file.write_text("x: 1\n")
        result = self.pb.just("_prepare-files")
        self.assertFailedCleanly(result)
        self.assertIn("was not generated by this script", result.stderr)
        self.assertTrue(user_file.exists())
        self.assertFalse((self.pb.root / "setup.yml").exists())

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

        # An invalid component makes the optimization fail.
        with open(self.pb.root / "components" / "miniflux" / "component.yml", "a") as file:
            file.write("\nno_such_field: true\n")
        self.assertNotEqual(self.pb.just("_prepare-files").returncode, 0)

        # Running again must retry (and fail again), not continue with an unoptimized setup.yml
        # and an optimized requirements.yml.
        self.assertNotEqual(self.pb.just("_prepare-files").returncode, 0)
        self.assertConsistent()

    def test_optimize_disable_and_enable(self):
        self.standard_inventory()
        self.assertSucceeded(self.pb.just("optimize-disable"))
        self.assertTrue((self.pb.root / "run" / "optimization-disabled").exists())
        self.assertEqual(self.pb.requirements_roles(), self.pb.component_requirements())

        # It stays disabled on the next runs
        self.assertSucceeded(self.pb.just("_prepare-files"))
        self.assertIn("nextcloud", self.pb.setup_roles())

        self.assertSucceeded(self.pb.just("optimize-enable"))
        self.assertFalse((self.pb.root / "run" / "optimization-disabled").exists())
        self.assertNotEnabled("nextcloud")

    def test_all_components_are_used_without_optimization(self):
        self.standard_inventory()
        self.assertSucceeded(self.pb.just("optimize-disable"))
        self.pb.touch_component("nextcloud/wiring.yml")

        self.assertSucceeded(self.pb.just("_prepare-files"))
        self.assertConsistent()
        self.assertEqual(self.pb.requirements_roles(), self.pb.component_requirements())
        self.assertIn("# changed by an update", (self.pb.root / "group_vars" / "mash_servers" / "nextcloud" / "wiring.yml").read_text())

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

    def test_binary_file_is_skipped_silently(self):
        """E.g. a gzip-compressed file without an extension, left in the directory of a host which is gone."""
        self.standard_inventory()
        path = self.pb.inventory / "host_vars" / "gone" / "files" / "backup"
        path.parent.mkdir(parents=True)
        path.write_bytes(gzip.compress(b"nextcloud_enabled: true\n"))
        result = self.pb.just("optimize-enable")
        self.assertSucceeded(result)
        self.assertEqual(result.stderr, "")
        self.assertEnabled("miniflux", "gitea")

    def test_non_ascii_text_with_any_locale(self):
        self.standard_inventory()
        self.pb.write("host_vars/a/nextcloud.yml", "# Nextcloud für die Familie\nnextcloud_enabled: true\n")
        self.assertSucceeded(self.pb.just("optimize-enable", env={"LC_ALL": "C", "LANG": "C", "PYTHONUTF8": "0"}))
        self.assertEnabled("nextcloud")


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


class TestComponents(OptimizeTestCase):
    """Checks the real components, and how components are put together."""

    def all_prefixes(self):
        manifests = [yaml.safe_load(path.read_text()) for path in (REPO / "components").glob("*/component.yml")]
        return {manifest["activation_prefix"] for manifest in manifests} - {""}

    def assertGeneratedFilesParse(self):
        yaml.safe_load((self.pb.root / "setup.yml").read_text())
        for relative_path in self.pb.group_vars_files():
            yaml.safe_load((self.pb.root / "group_vars" / "mash_servers" / relative_path).read_text())

    def test_all_roles(self):
        self.pb.hosts("[mash_servers]\na\n")
        self.pb.write(
            "host_vars/a/vars.yml",
            "".join("{0}optimize_test: true\n".format(prefix) for prefix in sorted(self.all_prefixes())),
        )
        self.assertSucceeded(self.pb.just("optimize-enable"))
        self.assertConsistent()
        self.assertGeneratedFilesParse()

        self.assertEqual(self.pb.requirements_roles(), self.pb.component_requirements())

    def test_minimal_roles(self):
        self.pb.hosts("[mash_servers]\na\n")
        self.pb.write("host_vars/a/vars.yml", "mash_playbook_generic_secret_key: x\n")
        self.assertSucceeded(self.pb.just("optimize-enable"))
        self.assertConsistent()
        self.assertGeneratedFilesParse()

    def test_with_files_apply_only_while_the_other_component_is_in_use(self):
        self.standard_inventory()
        self.assertSucceeded(self.pb.just("optimize-enable"))
        self.assertNotIn("miniflux/with/postgres.yml", self.pb.group_vars_files())

        with open(self.pb.inventory / "host_vars" / "a" / "vars.yml", "a") as file:
            file.write("postgres_enabled: true\n")
        self.assertSucceeded(self.pb.just("_prepare-files"))
        self.assertIn("miniflux/with/postgres.yml", self.pb.group_vars_files())

    def test_injected_entries_of_components_in_use(self):
        self.standard_inventory()
        with open(self.pb.inventory / "host_vars" / "a" / "vars.yml", "a") as file:
            file.write("postgres_enabled: true\n")
        self.assertSucceeded(self.pb.just("optimize-enable"))
        injected = yaml.safe_load((self.pb.root / "group_vars" / "mash_servers" / "postgres" / "injected.yml").read_text())
        self.assertIn("postgres_managed_databases_auto", injected)
        names = {entry["name"] for entry in injected["postgres_managed_databases_auto_unfiltered"]}
        self.assertIn("{{ miniflux_database_name }}", names)
        self.assertNotIn("{{ nextcloud_database_name }}", names)

    def test_documented_command_without_just(self):
        # docs/installing.md tells people who don't use `just` to run this, from the playbook directory
        # (with bin/ansible-python.sh, which only picks the Python interpreter)
        [command] = re.findall(r"`(?:bin/ansible-python\.sh )?(bin/optimize\.py [^`]+)`", (REPO / "docs" / "installing.md").read_text())
        result = subprocess.run([sys.executable, *shlex.split(command)], cwd=self.pb.root, capture_output=True, text=True)
        self.assertSucceeded(result)
        self.assertEqual(self.pb.requirements_roles(), self.pb.component_requirements())
        self.assertGeneratedFilesParse()

    def edit_yaml(self, relative_path, edit):
        """Changes a component file with `edit`, which gets its parsed contents to change."""
        path = self.pb.root / "components" / relative_path
        data = yaml.safe_load(path.read_text())
        edit(data)
        path.write_text(yaml.safe_dump(data, sort_keys=False))

    def write_component_file(self, relative_path, content):
        path = self.pb.root / "components" / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)

    def check(self):
        """Runs `bin/optimize.py --check` on the components."""
        return subprocess.run(
            [sys.executable, str(self.pb.root / "bin" / "optimize.py"), "--components-path", str(self.pb.root / "components"), "--check"],
            capture_output=True,
            text=True,
        )

    def test_check_passes(self):
        result = self.check()
        self.assertSucceeded(result)

    def test_check_finds_mistakes(self):
        manifest = "miniflux/component.yml"
        cases = {
            "unknown key": lambda: self.edit_yaml(manifest, lambda data: data.update(no_such_field=True)),
            "is not a component": lambda: self.edit_yaml(
                manifest, lambda data: data["inject"].update(no_such_component={"services": []})
            ),
            "but systemd_service_manager accepts services": lambda: self.edit_yaml(
                manifest, lambda data: data["inject"]["systemd_service_manager"].update(service=[])
            ),
            "lacks priority": lambda: self.edit_yaml(
                manifest, lambda data: data["inject"]["systemd_service_manager"]["services"][0].pop("priority")
            ),
            "`accepts` must be a mapping": lambda: self.edit_yaml(manifest, lambda data: data.update(accepts=["x"])),
            "`inject.postgres` must be a mapping of lists": lambda: self.edit_yaml(
                manifest, lambda data: data["inject"].update(postgres=["x"])
            ),
            "must contain exactly one role": lambda: self.write_component_file("miniflux/requirements.yml", "- miniflux\n"),
            "is not valid YAML": lambda: self.write_component_file(manifest, "activation_prefix: [\n"),
            "is defined in both": lambda: self.write_component_file("ntfy/with/miniflux.yml", "miniflux_enabled: true\n"),
            "must contain a mapping of variables": lambda: self.write_component_file("miniflux/with/ntfy.yml", "- x\n"),
            "may only contain <component>.yml": lambda: self.write_component_file("miniflux/with/no_such_component.yml", "---\n"),
            "contains unknown files": lambda: self.write_component_file("miniflux/notes.txt", ""),
        }
        for expected, make_mistake in cases.items():
            with self.subTest(expected):
                self.setUp()
                make_mistake()
                result = self.check()
                self.assertFailedCleanly(result)
                self.assertIn(expected, result.stderr)

    def test_hidden_files_and_backups_are_ignored(self):
        # E.g. left by file managers (.DS_Store) and editors (swap files, backups), like Ansible ignores them
        self.write_component_file("miniflux/.DS_Store", "\0")
        self.write_component_file("miniflux/wiring.yml~", "miniflux_enabled: true\n")
        self.write_component_file("miniflux/with/.postgres.yml.swp", "\0")
        self.assertSucceeded(self.check())
        self.standard_inventory()
        self.assertSucceeded(self.pb.just("optimize-enable"))
        self.assertNotIn("miniflux/wiring.yml~", self.pb.group_vars_files())

    def test_ansible_tags_in_wiring(self):
        with open(self.pb.root / "components" / "miniflux" / "wiring.yml", "a") as file:
            file.write('\nminiflux_optimize_test_unsafe: !unsafe "{{ not_templated }}"\n' + INLINE_VAULT.replace("some_secret", "miniflux_optimize_test_secret"))
        self.assertSucceeded(self.check())
        self.standard_inventory()
        self.assertSucceeded(self.pb.just("optimize-enable"))


class TestInventoryComponents(OptimizeTestCase):
    """Components in the inventory's own components/ directory, next to the playbook's."""

    HOOKS_COMPONENT = textwrap.dedent("""\
        activation_prefix: hooks_
        setup:
          - priority: 200
            entry:
              - role: ./roles/before_services
                tags: [setup-all, setup-hooks]
          - priority: 9050
            entry:
              - role: ./roles/after_services
                tags: [setup-all, setup-hooks]
        """)

    NOTES_COMPONENT = textwrap.dedent("""\
        activation_prefix: notes_
        inject:
          systemd_service_manager:
            services:
              - name: "{{ notes_identifier }}.service"
                priority: 2000
                restart_necessary: false
                groups: [mash, notes]
                when: "{{ notes_enabled }}"
        """)

    def setUp(self):
        super().setUp()
        self.standard_inventory()

    def add_hooks(self, inventory=None):
        self.pb.write("components/hooks/component.yml", self.HOOKS_COMPONENT, base=inventory)
        for role in ("before_services", "after_services"):
            self.pb.write("components/hooks/roles/{0}/tasks/main.yml".format(role), "---\n", base=inventory)

    def add_notes(self):
        self.pb.write("components/notes/component.yml", self.NOTES_COMPONENT)
        self.pb.write("components/notes/requirements.yml", "- src: git+https://example.com/notes.git\n  version: v1.0.0\n  name: notes\n")
        self.pb.write("components/notes/wiring.yml", "notes_enabled: false\nnotes_identifier: notes\n")
        self.pb.write("components/notes/with/postgres.yml", "notes_database_hostname: \"{{ postgres_connection_hostname }}\"\n")

    def enable(self, *variables, inventory=None):
        with open((inventory or self.pb.inventory) / "host_vars" / "a" / "vars.yml", "a") as file:
            file.writelines("{0}: true\n".format(variable) for variable in variables)

    def setup_entries(self):
        [play] = yaml.safe_load((self.pb.root / "setup.yml").read_text())
        return [entry["role"] for entry in play["roles"]]

    def test_components_in_use(self):
        self.add_hooks()
        self.add_notes()
        self.enable("hooks_enabled", "notes_enabled", "postgres_enabled")
        self.assertSucceeded(self.pb.just("optimize-enable"))

        self.assertEnabled("notes", "miniflux")
        entries = self.setup_entries()
        before, after = "inventory/components/hooks/roles/before_services", "inventory/components/hooks/roles/after_services"
        # Placed by priority among the playbook's components: between systemd_docker_base (130) and Postgres (220), and after systemd_service_manager (9010)
        self.assertLess(entries.index("galaxy/systemd_docker_base"), entries.index(before))
        self.assertLess(entries.index(before), entries.index("galaxy/postgres"))
        self.assertLess(entries.index("galaxy/systemd_service_manager"), entries.index(after))
        self.assertIn("galaxy/notes", entries)
        for role in (before, after):
            self.assertTrue((self.pb.root / role).is_dir())

        files = self.pb.group_vars_files()
        self.assertIn("notes/wiring.yml", files)
        self.assertIn("notes/with/postgres.yml", files)
        injected = yaml.safe_load(
            (self.pb.root / "group_vars" / "mash_servers" / "systemd_service_manager" / "injected.yml").read_text()
        )
        names = {entry["name"] for entry in injected["devture_systemd_service_manager_services_list_auto_unfiltered"]}
        self.assertIn("{{ notes_identifier }}.service", names)

    def test_components_not_in_use(self):
        self.add_hooks()
        self.add_notes()
        self.assertSucceeded(self.pb.just("optimize-enable"))
        self.assertNotEnabled("notes")
        self.assertNotIn("inventory/components/hooks/roles/before_services", self.setup_entries())
        self.assertNotIn("notes/wiring.yml", self.pb.group_vars_files())

    def test_all_components_without_optimization(self):
        self.add_notes()
        self.assertSucceeded(self.pb.just("optimize-disable"))
        self.assertEnabled("notes", "nextcloud")

    def test_inventory_elsewhere(self):
        inventory = self.pb.root.parent / (self.pb.root.name + "-inventory")
        self.addCleanup(shutil.rmtree, inventory)
        shutil.move(self.pb.inventory, inventory)
        self.add_hooks(inventory)
        self.enable("hooks_enabled", inventory=inventory)

        self.assertSucceeded(self.pb.just("optimize-enable", env={"ANSIBLE_INVENTORY": str(inventory / "hosts")}))
        role = "../{0}/components/hooks/roles/before_services".format(inventory.name)
        self.assertIn(role, self.setup_entries())
        self.assertTrue((self.pb.root / role).is_dir())

    def test_inventory_in_the_playbook_directory(self):
        # Its components/ directory is the playbook's own
        self.pb.write("hosts", "[mash_servers]\na\n", base=self.pb.root)
        self.pb.write("host_vars/a/vars.yml", "miniflux_enabled: true\n", base=self.pb.root)
        self.assertSucceeded(self.pb.just("optimize-enable", env={"ANSIBLE_INVENTORY": "hosts"}))
        self.assertEnabled("miniflux")

    def test_wiring_only_component(self):
        self.pb.write("components/notes/component.yml", "activation_prefix: notes_\nsetup: []\n" + self.NOTES_COMPONENT.split("\n", 1)[1])
        self.pb.write("components/notes/wiring.yml", "notes_identifier: notes\n")
        self.enable("notes_enabled")
        self.assertSucceeded(self.pb.just("optimize-enable"))
        self.assertNotIn("galaxy/notes", self.setup_entries())
        self.assertIn("notes/wiring.yml", self.pb.group_vars_files())

    def test_mistakes(self):
        cases = {
            "has the same name as": lambda: self.pb.write("components/miniflux/component.yml", "activation_prefix: miniflux_\n"),
            "does not exist in": lambda: self.pb.write("components/hooks/component.yml", self.HOOKS_COMPONENT),
            "has neither a requirements.yml nor a `setup.entry`": lambda: self.pb.write(
                "components/notes/component.yml", self.NOTES_COMPONENT
            ),
            "is defined in both": lambda: (
                self.add_notes(),
                self.pb.write("components/notes/wiring.yml", "notes_enabled: false\nminiflux_enabled: true\n"),
            ),
        }
        for expected, make_mistake in cases.items():
            with self.subTest(expected):
                self.setUp()
                self.assertSucceeded(self.pb.just("optimize-enable"))
                setup_yml = (self.pb.root / "setup.yml").read_text()
                make_mistake()
                self.enable("notes_enabled", "hooks_enabled")
                result = self.pb.just("_prepare-files")
                self.assertFailedCleanly(result)
                self.assertIn(expected, result.stderr)
                self.assertEqual((self.pb.root / "setup.yml").read_text(), setup_yml)


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
            if arguments == ["-v"]:
                print(os.environ.get("FAKE_AGRU_VERSION", "v0.3.0"))
                sys.exit(0)
            definitions = []
            for index, argument in enumerate(arguments):
                if argument == "-r":
                    definitions += yaml.safe_load(open(arguments[index + 1]))
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
        subprocess.run(["git", *args], cwd=cwd, env={**clean_environment(), **self.GIT_ENV}, check=True, capture_output=True)

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

    def test_roles_of_inventory_components(self):
        self.pb.write("components/notes/component.yml", "activation_prefix: notes_\n")
        self.pb.write("components/notes/requirements.yml", "- src: git+https://example.com/notes.git\n  version: v1.0.0\n  name: notes\n")
        self.pb.write("host_vars/a/vars.yml", "mash_playbook_generic_secret_key: x\nminiflux_enabled: true\nnotes_enabled: true\n")
        self.assertSucceeded(self.pb.just("roles", env=self.env))
        self.assertTrue((self.pb.root / "roles" / "galaxy" / "notes").is_dir())

        # Like the playbook's roles, it is deleted once no longer in use
        self.pb.write("host_vars/a/vars.yml", "mash_playbook_generic_secret_key: x\nminiflux_enabled: true\n")
        self.assertSucceeded(self.pb.just("roles", env=self.env))
        self.assertFalse((self.pb.root / "roles" / "galaxy" / "notes").exists())
        self.assertTrue((self.pb.root / "roles" / "galaxy" / "miniflux").is_dir())

    def make_clone_with_upstream_change(self):
        """Turns the playbook into a clone of an upstream repository, which then gets a component change."""
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
        with open(work_path / "components" / "miniflux" / "wiring.yml", "a") as file:
            file.write("\n# changed upstream\n")
        self.git("commit", "-q", "-am", "Change", cwd=work_path)
        self.git("push", "-q", "origin", "main", cwd=work_path)

    def test_update_prepares_files_after_pulling(self):
        self.make_clone_with_upstream_change()
        self.assertSucceeded(self.pb.just("update", env=self.env))
        self.assertIn("# changed upstream", (self.pb.root / "group_vars" / "mash_servers" / "miniflux" / "wiring.yml").read_text())
        [(args, roles)] = self.agru_calls()
        self.assertIn("name: miniflux", roles)
        self.assertNotIn("name: nextcloud", roles)

    def test_update_pins_versions_of_all_components(self):
        # `update -u` also regenerates VERSIONS.md and releases.opml, which these tests don't cover
        for script in ("versions.py", "feeds.py"):
            self.pb.write("bin/" + script, "", base=self.pb.root)
        self.make_clone_with_upstream_change()
        self.assertSucceeded(self.pb.just("update", "-u", env=self.env))
        [pinned] = [roles for args, roles in self.agru_calls() if args.endswith(" -u")]
        self.assertEqual(set(pinned.replace("name: ", "").split()), self.pb.component_requirements())

    def test_update_with_old_agru_fails_before_pulling(self):
        # agru before 0.3.0 only takes one requirements file
        self.make_clone_with_upstream_change()
        result = self.pb.just("update", "-u", env={**self.env, "FAKE_AGRU_VERSION": "v0.2.1"})
        self.assertFailedCleanly(result)
        self.assertIn("version 0.3.0 or newer", result.stderr)
        self.assertNotIn("# changed upstream", (self.pb.root / "components" / "miniflux" / "wiring.yml").read_text())

    def test_update_with_unknown_flags_fails_before_pulling(self):
        self.make_clone_with_upstream_change()
        result = self.pb.just("update", "--bogus", env=self.env)
        self.assertFailedCleanly(result)
        self.assertNotIn("# changed upstream", (self.pb.root / "components" / "miniflux" / "wiring.yml").read_text())
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
