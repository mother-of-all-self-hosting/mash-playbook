<!--
SPDX-FileCopyrightText: 2018 - 2025 Slavi Pantaleev
SPDX-FileCopyrightText: 2019 - 2022 Aaron Raimist
SPDX-FileCopyrightText: 2019 - 2023 MDAD project contributors
SPDX-FileCopyrightText: 2023 QEDeD
SPDX-FileCopyrightText: 2024 Nikita Chernyi
SPDX-FileCopyrightText: 2024 Fabio Bonelli
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->


# Prerequisites

<sup>Prerequisites > [Configuring DNS settings](configuring-dns.md) > [Getting the playbook](getting-the-playbook.md) > [Configuring the playbook](configuring-playbook.md) > [Installing](installing.md)</sup>

To install services using this Ansible playbook, you need to prepare several requirements both on your local computer (where you will run the playbook) and on the server (where the playbook will install the services). **These requirements must be set up manually** before proceeding to the next step.

Throughout this documentation, `example.com` is used as a placeholder domain. Be sure to replace it with your own domain before running any commands.

## Your local computer

- [Ansible](http://ansible.com/): Used to run this playbook and configure your server. See [our guide about Ansible](ansible.md) for more information, including [version requirements](ansible.md#supported-ansible-versions) and alternative ways to run Ansible.
- [passlib](https://passlib.readthedocs.io/en/stable/index.html) Python library. See the [official documentation](https://passlib.readthedocs.io/en/stable/install.html#installation-instructions) for installation instructions. On most distros, install the `python-passlib` or `py3-passlib` package, etc.
- [`git`](https://git-scm.com/): Recommended for downloading the playbook. `git` may also be required on the server if you will be [self-building](self-building.md) components.
- [`just`](https://github.com/casey/just): For running `just roles`, `just update`, etc. (see [`justfile`](../justfile)). You can also run these commands manually. See: [Running `just` commands](just.md).
- Strong password (random string) generator. The playbook often requires you to create strong passwords for `vars.yml` and components. Any tool is fine, but this playbook recommends [`pwgen`](https://linux.die.net/man/1/pwgen) (`pwgen -s 64 1`). [Password Tech](https://pwgen-win.sourceforge.io/) is a free and open source password generator for Windows. Avoid using random generators from the internet for security reasons.

## Server

- (Recommended) An **x86** server running one of these operating systems that use [systemd](https://systemd.io/):
  - **Archlinux**
  - **CentOS**, **Rocky Linux**, **AlmaLinux**, or other RHEL alternatives (your mileage may vary)
  - **Debian** (10/Buster or newer)
  - **Ubuntu** (18.04 or newer; [20.04 may be problematic](ansible.md#supported-ansible-versions) if you run the Ansible playbook on it)

  Generally, newer is better. Only released stable versions of distributions are supported, not betas or pre-releases. The playbook can take over your whole server or co-exist with other services.

  This playbook also supports running on non-`amd64` architectures like ARM. See [Alternative Architectures](alternative-architectures.md).

  If your distro runs within an [LXC container](https://linuxcontainers.org/), you may hit [this issue](https://github.com/spantaleev/matrix-docker-ansible-deploy/issues/703). It can be worked around if absolutely necessary, but it is recommended to avoid running from within an LXC container.

- `root` access to your server (or a user capable of elevating to `root` via `sudo`).
- [Python](https://www.python.org/). Most distributions install Python by default, but some don't (e.g. Ubuntu 18.04) and require manual installation (`apt-get install python3`). On some distros, Ansible may incorrectly [detect the Python version](https://docs.ansible.com/ansible/latest/reference_appendices/interpreter_discovery.html) (2 vs 3) and you may need to explicitly specify the interpreter path in `inventory/hosts` during installation (e.g. `ansible_python_interpreter=/usr/bin/python3`).
- [sudo](https://www.sudo.ws/), even when you've configured Ansible to log in as `root`, because this playbook sometimes uses the Ansible [become](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_privilege_escalation.html) module to perform tasks as another user (e.g. `mash`). The `become` module's default implementation uses `sudo`. Some distributions, like a minimal Debian net install, do not include the `sudo` package by default.
- Properly configured DNS records for `example.com` (see [Configuring DNS](configuring-dns.md)).
- Some TCP/UDP ports open. This playbook (actually [Docker itself](https://docs.docker.com/network/iptables/)) configures the server's internal firewall for you. In most cases, you don't need to do anything special. **If your server is behind another firewall**, you need to open these ports:
  - `80/tcp`: HTTP webserver
  - `443/tcp`: HTTPS webserver
  - Potentially other ports, depending on the services you enable in the **configuring the playbook** step. Consult each service's documentation page in `docs/` for details.

---

[▶️](configuring-dns.md) When ready to proceed, continue with [Configuring DNS](configuring-dns.md).
