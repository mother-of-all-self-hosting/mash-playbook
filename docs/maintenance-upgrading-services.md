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

This playbook not only installs various services for you, but can also upgrade them as new versions become available.

While this playbook helps you set up and maintain services, it will **not** automatically run maintenance tasks for you. You will need to update the playbook and re-run it **manually**.

The upstream projects used by this playbook occasionally (if not often) suffer from security vulnerabilities.

Since it is unsafe to keep outdated services running on a server connected to the internet, please update the playbook and re-run it periodically to keep services up-to-date.

The developers of this playbook strive to keep it updated, so you can re-run the playbook to address such vulnerabilities. It is **your responsibility** to keep your server and its services up-to-date.

## Steps to upgrade the services

### Check the changelog

Before updating the playbook and the Ansible roles, check [the changelog](../CHANGELOG.md) to see if there have been any backward-incompatible changes you need to address.

### Update the playbook and the Ansible roles

If all looks good, go to the `mash-playbook` directory and update your playbook directory and all upstream Ansible roles (defined in the `requirements.yml` file) by running:

- Either: `just update`
- Or: a combination of `git pull` and `just roles`

If you don't have the `just` tool, you can run the `ansible-galaxy` tool directly:

```sh
rm -rf roles/galaxy; ansible-galaxy install -r requirements.yml -p roles/galaxy/ --force
```

**Note:** For details about `just` commands, see: [Running `just` commands](just.md).

### Re-run the playbook setup

After updating the Ansible roles, re-run the [playbook setup](installing.md#2-maintaining-your-setup-in-the-future) and restart all services:

```sh
just install-all
```

If you remove components from `vars.yml`, or if a component is no longer installed by default, you need to run the setup command with the `setup-all` shortcut:

```sh
just setup-all
```

## PostgreSQL major version upgrade

Major version upgrades to the internal PostgreSQL database are not done automatically. Upgrades must be performed manually.

For details about upgrading, refer to the [upgrading PostgreSQL guide](services/postgres.md#upgrading-postgresql).
