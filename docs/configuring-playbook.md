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

For a basic installation, that's all you need.

If you're installing services on the same server using another playbook (like [matrix-docker-ansible-deploy](https://github.com/spantaleev/matrix-docker-ansible-deploy)) or you already have [Traefik](./services/traefik.md) or [Docker](./services/docker.md) installed on the server, consult our [Interoperability](./interoperability.md) documentation.

---------------------------------------------

[▶️](installing.md) When you're done with all the configuration you'd like to do, continue with [Installing](installing.md).
