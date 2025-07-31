<!--
SPDX-FileCopyrightText: 2018 - 2025 Slavi Pantaleev
SPDX-FileCopyrightText: 2018 Aaron Raimist
SPDX-FileCopyrightText: 2018 - 2024 MDAD project contributors
SPDX-FileCopyrightText: 2019 Edgars Voroboks
SPDX-FileCopyrightText: 2019 Michael Haak
SPDX-FileCopyrightText: 2020 Kevin Lanni
SPDX-FileCopyrightText: 2024 Nikita Chernyi
SPDX-FileCopyrightText: 2024 Mitja Jež
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Installing

<sup>[Prerequisites](prerequisites.md) > [Configuring DNS settings](configuring-dns.md) > [Getting the playbook](getting-the-playbook.md) > [Configuring the playbook](configuring-playbook.md) > Installing</sup>

Once you've configured your DNS records and the playbook, you can start the installation procedure.

## Update Ansible roles

Before installing, you need to update the Ansible roles that this playbook uses and fetches from outside.

To update your playbook directory and all upstream Ansible roles (defined in the `requirements.yml` file), run:

- Either: `just update`
- Or: a combination of `git pull` and `just roles`

If you don't have the `just` tool, you can run the `ansible-galaxy` tool directly:

```sh
rm -rf roles/galaxy; ansible-galaxy install -r requirements.yml -p roles/galaxy/ --force
```

For details about `just` commands, see: [Running `just` commands](just.md).

**Note:** If you're not using the [`just`](https://github.com/casey/just) utility, you need to create `setup.yml`, `requirements.yml`, and `group_vars/mash_servers` based on the up-to-date templates found in the [`templates/` directory](../templates). If you are using `just`, these files are created and maintained automatically.

## Installing services

The Ansible playbook's tasks are tagged, so that certain parts of the playbook can be run without running all other tasks.

The general command syntax is:
- (**Recommended**) when using `just`: `just run-tags COMMA_SEPARATED_TAGS_GO_HERE`
- When not using `just`: `ansible-playbook -i inventory/hosts setup.yml --tags=COMMA_SEPARATED_TAGS_GO_HERE`

It is recommended to get familiar with the [playbook tags](playbook-tags.md) before proceeding.

If you **don't** use SSH keys for authentication, but rather a regular password, you may need to add `--ask-pass` to all Ansible (or `just`) commands.

If you **do** use SSH keys for authentication, **and** use a non-root user to *become* root (sudo), you may need to add `-K` (`--ask-become-pass`) to all Ansible commands.

There are two ways to start the installation process, depending on whether you're [installing a brand new server (without importing data)](#installing-a-brand-new-server-without-importing-data) or [installing a server into which you'll import old data](#installing-a-server-into-which-youll-import-old-data).

### Installing a brand new server (without importing data)

If this is **a brand new** server and you **won't be importing old data into it**, run all these tags:

```sh
# This is equivalent to: just run-tags install-all,start
just install-all

# Or, when not using just, you can use this instead:
# ansible-playbook -i inventory/hosts setup.yml --tags=install-all,start
```

This will do a full installation and start all services.

**Note:** If the command does not work as expected, make sure that you have properly installed and configured the required software, as described in [Prerequisites](prerequisites.md).

### Installing a server into which you'll import old data

If you will be importing data into your newly created server, install it, but **do not** start its services yet. Starting services or modifying the database now may affect your data import later on.

To do the installation **without** starting services, run only the `install-all` tag:

```sh
just run-tags install-all

# Or, when not using just, you can use this instead:
# ansible-playbook -i inventory/hosts setup.yml --tags=install-all
```

> [!WARNING]
> Do not run the just "recipe" `just install-all` instead, because it automatically starts services at the end of execution. See: [Difference between playbook tags and shortcuts](just.md#difference-between-playbook-tags-and-shortcuts)

When this command completes, services won't be running yet.

You can now:

- [Import an existing Postgres database (from another installation)](services/postgres.md#importing) (optional)

...and then proceed to starting all services:

```sh
# This is equivalent to: just run-tags start (or: just run-tags start-all)
just start-all

# Or, when not using just, you can use this instead:
# ansible-playbook -i inventory/hosts setup.yml --tags=start
```

Regardless of the installation method you have chosen, **if no error is returned, the installation has completed and the services have been started successfully** 🎉

## Things to do next

After you have started the services, you can:

- Start using the configured services
- Set up additional services
- Learn how to [upgrade services when new versions are released](maintenance-upgrading-services.md)
- Join our [Matrix](https://matrix.org) support room — [#mash-playbook:devture.com](https://matrixrooms.info/room/mash-playbook:devture.com). You might learn something or help someone new to hosting services with this playbook.
- Help make this playbook better by contributing (code, documentation, or [coffee/beer](https://liberapay.com/mother-of-all-self-hosting/donate))

### ⚠️ Keep the playbook and services up-to-date

While this playbook helps you set up and maintain services, it will **not** automatically run maintenance tasks for you. You will need to update the playbook and re-run it **manually**.

The upstream projects used by this playbook occasionally (if not often) suffer from security vulnerabilities.

Since it is unsafe to keep outdated services running on a server connected to the internet, please update the playbook and re-run it periodically to keep services up-to-date.

For more information about upgrading or maintaining services with the playbook, see: [Upgrading services](maintenance-upgrading-services.md)

Feel free to **re-run the setup command any time** you think something is wrong with the server configuration. Ansible will take your configuration and update your server to match.

```sh
just install-all

# Or, to run potential uninstallation tasks too:
# just setup-all
```

To do it without `just`:

```sh
ansible-playbook -i inventory/hosts setup.yml --tags=install-all,start

# Or, to run potential uninstallation tasks too:
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

**Note:** See [this page on playbook tags](playbook-tags.md) for more information about those tags.
