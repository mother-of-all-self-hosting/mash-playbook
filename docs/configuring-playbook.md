<!--
SPDX-FileCopyrightText: 2018 - 2025 Slavi Pantaleev
SPDX-FileCopyrightText: 2018 - 2024 MDAD project contributors
SPDX-FileCopyrightText: 2020 Sabine Laszakovits
SPDX-FileCopyrightText: 2021 Cody Neiman
SPDX-FileCopyrightText: 2021 Matthew Cengia
SPDX-FileCopyrightText: 2021 Toni Spets
SPDX-FileCopyrightText: 2022 Julian Foad
SPDX-FileCopyrightText: 2022 Vladimir Panteleev
SPDX-FileCopyrightText: 2022 - 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 MASH project contributors
SPDX-FileCopyrightText: 2023 Shreyas Ajjarapu
SPDX-FileCopyrightText: 2023 Nikita Chernyi
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Configuring the playbook

<sup>[Prerequisites](prerequisites.md) > [Configuring DNS settings](configuring-dns.md) > [Getting the playbook](getting-the-playbook.md) > Configuring the playbook > [Installing](installing.md)</sup>

If you've configured your DNS records and retrieved the playbook's source code to your computer, you can start configuring the playbook. To do so, follow these steps inside the playbook directory:

1. create a directory to hold your configuration (`mkdir -p inventory/host_vars/mash.example.com`)

2. copy the sample configuration file (`cp examples/vars.yml inventory/host_vars/mash.example.com/vars.yml`)

3. edit the configuration file (`inventory/host_vars/mash.example.com/vars.yml`) to your liking. You should [enable one or more services](supported-services.md) in your `vars.yml` file. You may also take a look at the various `roles/*/ROLE_NAME_HERE/defaults/main.yml` files (after importing external roles with `just update` into `roles/galaxy`) and see if there's something you'd like to copy over and override in your `vars.yml` configuration file.

4. copy the sample inventory hosts file (`cp examples/hosts inventory/hosts`)

5. edit the inventory hosts file (`inventory/hosts`) to your liking

6. (optional, advanced) you may wish to keep your `inventory` directory under version control with [git](https://git-scm.com/) or any other version-control system. The `inventory` directory path is ignored via `.gitignore`, so it won't be part of the playbook repository. You can safely create a new git repository inside that directory with `git init`, etc.

## Inventory connection options

The `inventory/hosts` file defines which servers Ansible manages and how it connects to them.

`ansible_host` is the address or hostname Ansible uses for SSH. This is often the server's public IP address, but it can be another SSH-reachable address if your control node reaches the server through a private network, VPN, or other routing. It does not by itself define where services are publicly reachable; public DNS records and service hostnames are configured separately in [Configuring DNS settings](configuring-dns.md) and in your `vars.yml` file.

The default example connects as `root`:

```ini
[mash_servers]
mash.example.com ansible_host=YOUR_SERVER_SSH_ADDRESS_HERE ansible_ssh_user=root
```

To connect as a non-root user and elevate privileges with sudo, use `ansible_become`:

```ini
[mash_servers]
mash.example.com ansible_host=YOUR_SERVER_SSH_ADDRESS_HERE ansible_ssh_user=username ansible_become=true ansible_become_user=root
```

If sudo requires a password, let Ansible ask for it interactively by adding `--ask-become-pass` to your `ansible-playbook` or `just` command. If you need to store `ansible_become_password`, keep it in an encrypted Vault variable instead of plaintext inventory.

If your SSH private key is protected by a passphrase, unlock it before running the playbook, for example with `ssh-agent` and `ssh-add`. Ansible's default SSH connection plugin does not provide an interactive channel for decrypting SSH private keys during a playbook run, so an encrypted key that has not been loaded may fail instead of prompting you. See Ansible's [SSH connection plugin documentation](https://docs.ansible.com/projects/ansible/latest/collections/ansible/builtin/ssh_connection.html) for details.

For encrypted Ansible Vault files, add `--ask-vault-pass` to your commands. Inventories using named or multiple Vault IDs may need `--vault-id <id>@prompt` instead. See Ansible's [Vault password documentation](https://docs.ansible.com/projects/ansible/latest/vault_guide/vault_managing_passwords.html). When both Vault and sudo passwords are required, pass both flags, for example:

```sh
just install-all --ask-vault-pass --ask-become-pass
```

If SSH listens on a non-standard port, add `ansible_port`:

```ini
mash.example.com ansible_host=YOUR_SERVER_SSH_ADDRESS_HERE ansible_ssh_user=root ansible_port=2222
```

If you run this playbook on the same server that it manages, you can use a local Ansible connection. Keep the inventory host name aligned with the `inventory/host_vars/<host>/vars.yml` directory, and set `ansible_connection` for that host:

```ini
[mash_servers]
mash.example.com ansible_connection=local
```

This keeps the host identity and host-specific variables consistent while using a local connection. Ansible's inventory and connection behavior is documented in its [inventory guide](https://docs.ansible.com/projects/ansible/latest/inventory_guide/intro_inventory.html) and [connection details](https://docs.ansible.com/projects/ansible/latest/inventory_guide/connection_details.html).

Python interpreter requirements and discovery problems are covered in [Prerequisites](prerequisites.md#managed-node). If Ansible detects the wrong Python interpreter for a host, set an explicit value such as `ansible_python_interpreter=/usr/bin/python3`.

## Configuring interoperability with other services

If you're installing services on the same server using another playbook (like [matrix-docker-ansible-deploy](https://github.com/spantaleev/matrix-docker-ansible-deploy)) or you already have [Traefik](./services/traefik.md) or [Docker](./services/docker.md) installed on the server, consult our [Interoperability](./interoperability.md) documentation.

---------------------------------------------

[▶️](installing.md) When you're done with all the configuration you'd like to do, continue with [Installing](installing.md).
