# Installing

If you've [configured the playbook](configuring-playbook.md) and have prepared the required domains (DNS records) depending on the services you've enabled, you can start the installation procedure.

**Before installing** and each time you update the playbook in the future, you will need to update the Ansible roles in this playbook by running `just roles`. `just roles` is a shortcut (a `roles` target defined in [`justfile`](../justfile) and executed by the [`just`](https://github.com/casey/just) utility) which ultimately runs [ansible-galaxy](https://docs.ansible.com/ansible/latest/cli/ansible-galaxy.html) to download Ansible roles. If you don't have `just`, you can also manually run the `roles` commands seen in the `justfile`.


## Playbook tags introduction

The Ansible playbook's tasks are tagged, so that certain parts of the Ansible playbook can be run without running all other tasks.

The general command syntax is: `ansible-playbook -i inventory/hosts setup.yml --tags=COMMA_SEPARATED_TAGS_GO_HERE`

Here are some playbook tags that you should be familiar with:

- `setup-all` - runs all setup tasks (installation and uninstallation) for all components, but does not start/restart services

- `install-all` - like `setup-all`, but skips uninstallation tasks. Useful for maintaining your setup quickly when its components remain unchanged. If you adjust your `vars.yml` to remove components, you'd need to run `setup-all` though, or these components will still remain installed

- `setup-SERVICE` (e.g. `setup-miniflux`) - runs the setup tasks only for a given role ([Miniflux](services/miniflux.md) in this example), but does not start/restart services. You can discover these additional tags in each role (`roles/**/tasks/main.yml`). Running per-component setup tasks is **not recommended**, as components sometimes depend on each other and running just the setup tasks for a given component may not be enough. For example, for setting up the [Miniflux](services/miniflux.md) service, in addition to the `setup-miniflux` tag, changes to the database are also necessary (the `setup-postgres` tag).

- `install-SERVICE` (e.g. `install-miniflux`) - like `setup-SERVICE`, but skips uninstallation tasks. See `install-all` above for additional information.

- `start` - starts all systemd services and makes them start automatically in the future

- `stop` - stops all systemd services

`setup-*` tags and `install-*` tags **do not start services** automatically, because you may wish to do things before starting services, such as importing a database dump, restoring data from another server, etc.


## 1. Installing services

If you **don't** use SSH keys for authentication, but rather a regular password, you may need to add `--ask-pass` to the all Ansible commands

If you **do** use SSH keys for authentication, **and** use a non-root user to *become* root (sudo), you may need to add `-K` (`--ask-become-pass`) to all Ansible commands

There 2 ways to start the installation process - depending on whether you're [Installing a brand new server (without importing data)](#installing-a-brand-new-server-without-importing-data) or [Installing a server into which you'll import old data](#installing-a-server-into-which-youll-import-old-data).


### Installing a brand new server (without importing data)

If this is **a brand new** server and you **won't be importing old data into it**, run all these tags:

```sh
ansible-playbook -i inventory/hosts setup.yml --tags=install-all,start
```

This will do a full installation and start all services.

Proceed to [Maintaining your setup in the future](#2-maintaining-your-setup-in-the-future) and [Finalize the installation](#3-finalize-the-installation)


### Installing a server into which you'll import old data

If you will be importing data into your newly created server, install it, but **do not** start its services just yet.
Starting its services or messing with its database now will affect your data import later on.

To do the installation **without** starting services, run only the `install-all` tag:

```sh
ansible-playbook -i inventory/hosts setup.yml --tags=install-all
```

When this command completes, services won't be running yet.

You can now:

- [Importing an existing Postgres database (from another installation)](services/postgres.md#importing) (optional)

.. and then proceed to starting all services:

```sh
ansible-playbook -i inventory/hosts setup.yml --tags=start
```

Proceed to [Maintaining your setup in the future](#2-maintaining-your-setup-in-the-future).


## 2. Maintaining your setup in the future

Feel free to **re-run the setup command any time** you think something is off with the server configuration. Ansible will take your configuration and update your server to match.

Note that if you remove components from `vars.yml`, or if we switch some component from being installed by default to not being installed by default anymore, you'd need to run the setup command with `--tags=setup-all` instead of `--tags=install-all`. See [Playbook tags introduction](#playbook-tags-introduction)

A way to invoke these `ansible-playbook` commands with less typing in the future is to use [just](https://github.com/casey/just) to run them: `just install-all` or `just setup-all`. See [our `justfile`](../justfile) for more information.


## 3. Things to do next

After you have started the services, you can:

- start using the configured services
- or set up additional services
- or learn how to [upgrade services when new versions are released](maintenance-upgrading-services.md)
- or come say Hi in our [Matrix](https://matrix.org) support room - [#mash-playbook:devture.com](https://matrix.to/#/#mash-playbook:devture.com). You might learn something or get to help someone else new to hosting services with this playbook.
- or help make this playbook better by contributing (code, documentation, or [coffee/beer](https://liberapay.com/mother-of-all-self-hosting/donate))
