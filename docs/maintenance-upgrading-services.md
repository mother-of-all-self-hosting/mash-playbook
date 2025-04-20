<!--
SPDX-FileCopyrightText: 2018 - 2023 Slavi Pantaleev
SPDX-FileCopyrightText: 2018 Aaron Raimist
SPDX-FileCopyrightText: 2024 MDAD project contributors
SPDX-FileCopyrightText: 2024 Nikita Chernyi
SPDX-FileCopyrightText: 2024 Felix Stupp
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Upgrading services

This playbook not only installs various services for you, but can also upgrade them as new versions are made available.

While this playbook helps you to set up services and maintain them, it will **not** automatically run the maintenance task for you. You will need to update the playbook and re-run it **manually**.

The upstream projects, which this playbook makes use of, occasionally if not often suffer from security vulnerabilities.

Since it is unsafe to keep outdated services running on the server connected to the internet, please consider to update the playbook and re-run it periodically, in order to keep the services up-to-date.

The developers of this playbook strive to maintain the playbook updated, so that you can re-run the playbook to address such vulnerabilities. It is **your responsibility** to keep your server and the services on it up-to-date.

## Steps to upgrade the services

### Check the changelog

Before updating the playbook and the Ansible roles in the playbook, take a look at [the changelog](../CHANGELOG.md) to see if there have been any backward-incompatible changes that you need to take care of.

### Update the playbook and the Ansible roles

If it looks good to you, go to the `mash-playbook` directory, update your playbook directory and all upstream Ansible roles (defined in the `requirements.yml` file) by running:

- either: `just update`
- or: a combination of `git pull` and `just roles`

If you don't have either `just` tool, you can run the `ansible-galaxy` tool directly: `rm -rf roles/galaxy; ansible-galaxy install -r requirements.yml -p roles/galaxy/ --force`

**Note**: for details about `just` commands, take a look at: [Running `just` commands](just.md).

### Re-run the playbook setup

After updating the Ansible roles, then re-run the [playbook setup](installing.md#2-maintaining-your-setup-in-the-future) and restart all services:

```sh
just install-all
```

If you remove components from `vars.yml`, or if we switch some component from being installed by default to not being installed by default anymore, you'd need to run the setup command with the `setup-all` shortcut as below:

```sh
just setup-all
```

## PostgreSQL major version upgrade

Major version upgrades to the internal PostgreSQL database are not done automatically. Upgrades must be performed manually.

For details about upgrading it, refer to the [upgrading PostgreSQL guide](services/postgres.md#upgrading-postgresql).
