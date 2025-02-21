<!--
SPDX-FileCopyrightText: 2023 - 2025 Slavi Pantaleev
SPDX-FileCopyrightText: 2024 Nikita Chernyi
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Installing

If you've [configured the playbook](configuring-playbook.md) and have prepared the required domains (DNS records) depending on the services you've enabled, you can start the installation procedure.

This playbook makes use of the [`just`](https://github.com/casey/just) utility to make it easier to run playbook-related commands defined in the [`justfile`](../justfile).
We recommend installing and using using `just` - otherwise, you'll need to do more manual work.

**Before installing** and each time you update the playbook in the future, you will need to:

- (only if you're not using the [`just`](https://github.com/casey/just) utility): create `setup.yml`, `requirements.yml` and `group_vars/mash_servers` based on the up-to-date templates found in the [`templates/` directory](../templates). If you are using `just`, these files are created and maintained up-to-date automatically.

- update the Ansible roles in this playbook by either running `just update` or `git pull && just roles`. `just update` is a shortcut that calls `git pull` and `just roles` with a single command, while `just roles` is a shortcut which ultimately runs either [agru](https://github.com/etkecc/agru) or [ansible-galaxy](https://docs.ansible.com/ansible/latest/cli/ansible-galaxy.html) to download Ansible roles defined in the `requirements.yml` file. If you don't have `just`, you can also manually run the `roles` commands seen in the [`justfile`](../justfile).

## Installing services

The Ansible playbook's tasks are tagged, so that certain parts of the Ansible playbook can be run without running all other tasks.

The general command syntax is:
- (**recommended**) when using `just`: `just run-tags COMMA_SEPARATED_TAGS_GO_HERE`
- when not using `just`: `ansible-playbook -i inventory/hosts setup.yml --tags=COMMA_SEPARATED_TAGS_GO_HERE`

It is recommended to get yourself familiar with the [playbook tags](playbook-tags.md) before proceeding.

If you **don't** use SSH keys for authentication, but rather a regular password, you may need to add `--ask-pass` to the all Ansible (or `just`) commands

If you **do** use SSH keys for authentication, **and** use a non-root user to *become* root (sudo), you may need to add `-K` (`--ask-become-pass`) to all Ansible commands

There 2 ways to start the installation process - depending on whether you're [Installing a brand new server (without importing data)](#installing-a-brand-new-server-without-importing-data) or [Installing a server into which you'll import old data](#installing-a-server-into-which-youll-import-old-data).


### Installing a brand new server (without importing data)

If this is **a brand new** server and you **won't be importing old data into it**, run all these tags:

```sh
# This is equivalent to: just run-tags install-all,start
just install-all

# Or, when not using just, you can use this instead:
# ansible-playbook -i inventory/hosts setup.yml --tags=install-all,start
```

This will do a full installation and start all services.

Proceed to [Maintaining your setup in the future](#2-maintaining-your-setup-in-the-future).


### Installing a server into which you'll import old data

If you will be importing data into your newly created server, install it, but **do not** start its services just yet.
Starting its services or messing with its database now will affect your data import later on.

To do the installation **without** starting services, run only the `install-all` tag:

```sh
just run-tags install-all

# Or, when not using just, you can use this instead:
# ansible-playbook -i inventory/hosts setup.yml --tags=install-all
```

When this command completes, **services won't be running yet**.

You can now:

- [Importing an existing Postgres database (from another installation)](services/postgres.md#importing) (optional)

.. and then proceed to starting all services:

```sh
# This is equivalent to: just run-tags start (or: just run-tags start-all)
just start-all

# Or, when not using just, you can use this instead:
# ansible-playbook -i inventory/hosts setup.yml --tags=start
```

Proceed to [Maintaining your setup in the future](#2-maintaining-your-setup-in-the-future).


## 2. Maintaining your setup in the future

Feel free to **re-run the setup command any time** you think something is off with the server configuration. Ansible will take your configuration and update your server to match.

Note that if you remove components from `vars.yml`, or if we switch some component from being installed by default to not being installed by default anymore, you'd need to use `setup-all` instead of `install-all`. See [this page on the playbook tags](playbook-tags.md) for more information.

To do it with `just`:

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


## 3. Things to do next

After you have started the services, you can:

- start using the configured services
- or set up additional services
- or learn how to [upgrade services when new versions are released](maintenance-upgrading-services.md)
- or come say Hi in our [Matrix](https://matrix.org) support room - [#mash-playbook:devture.com](https://matrix.to/#/#mash-playbook:devture.com). You might learn something or get to help someone else new to hosting services with this playbook.
- or help make this playbook better by contributing (code, documentation, or [coffee/beer](https://liberapay.com/mother-of-all-self-hosting/donate))
