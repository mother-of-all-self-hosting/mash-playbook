<!--
SPDX-FileCopyrightText: 2020 - 2024 MDAD project contributors
SPDX-FileCopyrightText: 2020 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2020 Aaron Raimist
SPDX-FileCopyrightText: 2020 Chris van Dijk
SPDX-FileCopyrightText: 2020 Dominik Zajac
SPDX-FileCopyrightText: 2020 Mickaël Cornière
SPDX-FileCopyrightText: 2021 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2021 foxcris
SPDX-FileCopyrightText: 2022 François Darveau
SPDX-FileCopyrightText: 2022 Julian Foad
SPDX-FileCopyrightText: 2022 Warren Bailey
SPDX-FileCopyrightText: 2023 Antonis Christofides
SPDX-FileCopyrightText: 2023 Felix Stupp
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara
SPDX-FileCopyrightText: 2025 Nicola Murino

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# traefik-certs-dumper

The playbook can install and configure [traefik-certs-dumper](https://github.com/ldez/traefik-certs-dumper) for you.

traefik-certs-dumper is a tool which dumps [ACME](https://en.wikipedia.org/wiki/Automatic_Certificate_Management_Environment) certificates (like [Let's Encrypt](https://letsencrypt.org/)) from [Traefik](https://traefik.io/)'s `acme.json` file into some directory. It can be used to mount the ceritificate file and its private key to the container of services which need them.

The [Ansible role for traefik-certs-dumper](https://github.com/mother-of-all-self-hosting/ansible-role-traefik-certs-dumper) is developed and maintained by the MASH project. For details about configuring traefik-certs-dumper, you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-traefik-certs-dumper/blob/main/docs/configuring-traefik-certs-dumper.md) online
- 📁 `roles/galaxy/traefik_certs_dumper/docs/configuring-traefik-certs-dumper.md` locally, if you have [fetched the Ansible roles](../installing.md)
