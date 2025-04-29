[![Support room on Matrix](https://img.shields.io/matrix/mash-playbook:devture.com.svg?label=%23mash-playbook%3Adevture.com&logo=matrix&style=for-the-badge&server_fqdn=matrix.devture.com&fetchMode=summary)](https://matrix.to/#/#mash-playbook:devture.com) [![donate](https://liberapay.com/assets/widgets/donate.svg)](https://liberapay.com/mother-of-all-self-hosting/donate)

# Mother-of-All-Self-Hosting Ansible playbook

**MASH** (**M**other-of-**A**ll-**S**elf-**H**osting) is an [Ansible](https://www.ansible.com/) playbook that helps you self-host services as [Docker](https://www.docker.com/) containers on your own server.

By running services in containers, we can have a predictable and up-to-date setup, across multiple supported distros and CPU architectures.

This project allows self-hosting of a [large number of services](docs/supported-services.md) and will continue to grow by adding support for [FOSS](https://en.wikipedia.org/wiki/Free_and_open-source_software).

[Installation](docs/README.md) (upgrades) and some maintenance tasks are automated using [Ansible](https://www.ansible.com/) (see [our Ansible guide](docs/ansible.md)).


## Supported services

See the [full list of supported services here](docs/supported-services.md).


## Installation

To configure and install services on your own server, follow the [README in the docs/ directory](docs/README.md).


## Changes

This playbook evolves over time, sometimes with backward-incompatible changes.

When updating the playbook, refer to [the changelog](CHANGELOG.md) to catch up with what's new.


## Support

- Matrix room: [#mash-playbook:devture.com](https://matrix.to/#/#mash-playbook:devture.com). To join Matrix, [use a public server](https://app.element.io) like `matrix.org` or self-host Matrix yourself using the related [matrix-docker-ansible-deploy](https://github.com/spantaleev/matrix-docker-ansible-deploy) Ansible playbook

- GitHub issues: [mother-of-all-self-hosting/mash-playbook/issues](https://github.com/mother-of-all-self-hosting/mash-playbook/issues)


## Why create such a mega playbook?

We used to maintain separate playbooks for various services ([Matrix](https://github.com/spantaleev/matrix-docker-ansible-deploy), [Nextcloud](https://github.com/spantaleev/nextcloud-docker-ansible-deploy), [Gitea](https://github.com/spantaleev/gitea-docker-ansible-deploy), [Gitlab](https://github.com/spantaleev/gitlab-docker-ansible-deploy), [Vaultwarden](https://github.com/spantaleev/vaultwarden-docker-ansible-deploy), [PeerTube](https://github.com/spantaleev/peertube-docker-ansible-deploy), ..). They re-used Ansible roles (for [Postgres](https://github.com/devture/com.devture.ansible.role.postgres), [Traefik](https://github.com/devture/com.devture.ansible.role.traefik), etc.), but were still hard to maintain due to the large duplication of effort.

Most of these playbooks hosted services which require a Postgres database, a Traefik reverse-proxy, a backup solution, etc. All of them needed to come with documentation, etc.
All these things need to be created and kept up-to-date in each and every playbook.

Having to use a dedicated Ansible playbook for each and every piece of software means that you have to juggle many playbooks and make sure they don't conflict with one another when installing services on the same server. All these related playbooks interoperated nicely, but still required at least a bit of manual configuration to achieve this interoperability.

Using specialized Ansible playbooks also means that trying out new software is difficult. Despite the playbooks being similar (which eases the learning curve), each one is still a new git repository you need to clone and maintain, etc.

Furthermore, not all pieces of software are large enough to justify having their own dedicated Ansible playbook. They have no home, so no one uses them.

We're finding the need for a playbook which combines all of this into one, so that:

- you don't need to juggle multiple Ansible playbooks
- you can try out various services easily - a few lines of extra configuration and you're ready to go
- small pieces of software (like [Miniflux](https://miniflux.app/), powered by the [miniflux](https://gitlab.com/etke.cc/roles/miniflux) Ansible role) which don't have their own playbook can finally find a home
- you can use a single playbook with the quality you know and trust
- shared services (like Postgres) are maintained in one single place
- backups are made easy, because everything lives together (same base data path, same Postgres instance)

Having one large playbook with all services does not necessarily mean you need to host everything on the same server though. Feel free to use as many servers as you see fit. While containers provide some level of isolation, it's still better to not put all your eggs in one basket and create a single point of failure.

All of the aforementioned playbooks have been absorbed into this one. See the [full list of supported services here](docs/supported-services.md).
The [Matrix playbook](https://github.com/spantaleev/matrix-docker-ansible-deploy) will remain separate, because it contains a huge number of components and will likely grow even more. It deserves to stand on its own.


## What's with the name?

Our goal is to create a large Ansible playbook which can be your all-in-one-toolkit for self-hosting services in a clean and reliable way.

We like the MASH acronym, and [mashing](https://en.wikipedia.org/wiki/Mashing) is popular in the alcohol brewing industry. The result of all that mash is an enjoyable (at least by some) product.

Then, there's mixing and mashing stuff, which is also what this Ansible playbook is all about - you can mix and mash various pieces of software to create the self-hosted stack of your dreams!
