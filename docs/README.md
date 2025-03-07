<!--
SPDX-FileCopyrightText: 2018 - 2023 Slavi Pantaleev
SPDX-FileCopyrightText: 2018 Aaron Raimist
SPDX-FileCopyrightText: 2019 Lyubomir Popov
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Table of Contents

## ⬇️ Installaton guide <!-- NOTE: the 🚀 emoji is used by "Getting started" on README.md -->

<!-- TODO: consider to add a quick start guide like the MDAD project has done. -->

Follow this guide to install services on your server using this Ansible playbook.

- [Prerequisites](prerequisites.md)

- [Configuring DNS settings](configuring-dns.md)

- [Getting the playbook](getting-the-playbook.md)

- [Configuring the playbook](configuring-playbook.md)

- [Installing](installing.md)

## 🛠️ Configuration options

You can check useful documentation for configuring components in [`services`](services/) directory. See [this page](supported-services.md) for a list of all supported services.

## 👨‍🔧 Maintenance

If your server and services experience issues, feel free to come to [our support room](https://matrix.to/#/#mash-playbook:devture.com) on Matrix and ask for help.

<!-- NOTE: sort list items alphabetically -->

- [Maintenance and Troubleshooting](maintenance-and-troubleshooting.md)

- [PostgreSQL maintenance](services/postgres.md#maintenance)

- [Upgrading services](maintenance-upgrading-services.md)

## Other documentation pages <!-- NOTE: this header's title and the section below need optimization -->

<!-- NOTE: sort list items under faq.md alphabetically -->

- [Alternative architectures](alternative-architectures.md)

- [Configuring interoperability with other services](interoperability.md)

- [Developer documentation](developer-documentation.md)

- [Playbook tags](playbook-tags.md)

- [Running `just` commands](just.md)

- [Running multiple instances of the same service on the same host](running-multiple-instances.md)

- [Self-building](self-building.md)

- [Setting up MASH services on a Matrix server configured with the matrix-docker-ansible-deploy Ansible playbook](setting-up-services-on-mdad-server.md)

- [Supported services](supported-services.md)

- [Uninstalling](uninstalling.md)

- [Using Ansible for the playbook](ansible.md)
