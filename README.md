# Mother-of-All-Self-Hosting Ansible playbook

[![Support room on Matrix](https://img.shields.io/matrix/mash-playbook:devture.com.svg?label=%23mash-playbook%3Adevture.com&logo=matrix&style=for-the-badge&server_fqdn=matrix.devture.com&fetchMode=summary)](https://matrixrooms.info/room/mash-playbook:devture.com) [![donate](https://liberapay.com/assets/widgets/donate.svg)](https://liberapay.com/mother-of-all-self-hosting/donate) [![REUSE status](https://api.reuse.software/badge/github.com/mother-of-all-self-hosting/mash-playbook)](https://api.reuse.software/info/github.com/mother-of-all-self-hosting/mash-playbook)

**MASH** (**M**other-of-**A**ll-**S**elf-**H**osting) is an [Ansible](https://www.ansible.com/) playbook that helps you self-host services as [Docker](https://www.docker.com/) containers on your own server.

By running services in containers, we can have a predictable and up-to-date setup, across multiple supported distros and CPU architectures.

This project allows self-hosting of a [large number of services](docs/supported-services.md) and will continue to grow by adding support for [FOSS](https://en.wikipedia.org/wiki/Free_and_open-source_software).

[Installation](docs/README.md) (upgrades) and some maintenance tasks are automated using [Ansible](https://www.ansible.com/) (refer to [our Ansible guide](docs/ansible.md)).

## Supported services

See the [full list of supported services here](docs/supported-services.md).

## Installation

To configure and install services on your own server, follow the [README in the docs/ directory](docs/README.md).

## Changes

This playbook evolves over time, sometimes with backward-incompatible changes.

When updating the playbook, refer to [the changelog](CHANGELOG.md) to catch up with what's new.

## Support

- Matrix room: [#mash-playbook:devture.com](https://matrixrooms.info/room/mash-playbook:devture.com). To join Matrix, [use a public server](https://app.element.io) like `matrix.org` or self-host Matrix yourself using the related [matrix-docker-ansible-deploy](https://github.com/spantaleev/matrix-docker-ansible-deploy) Ansible playbook

- GitHub issues: [mother-of-all-self-hosting/mash-playbook/issues](https://github.com/mother-of-all-self-hosting/mash-playbook/issues)

## What's with the name?

Our goal is to create a large Ansible playbook which can be your all-in-one-toolkit for self-hosting services in a clean and reliable way.

We like the MASH acronym, and [mashing](https://en.wikipedia.org/wiki/Mashing) is popular in the alcohol brewing industry. The result of all that mash is an enjoyable (at least by some) product.

Then, there's mixing and mashing stuff, which is also what this Ansible playbook is all about - you can mix and mash various pieces of software to create the self-hosted stack of your dreams!
