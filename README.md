# Mother-of-All-Self-Hosting Ansible playbook

**MASH** (**M**other-of-**A**ll-**S**elf-**H**osting) is an [Ansible](https://www.ansible.com/) playbook that helps you self-host services as [Docker](https://www.docker.com/) containers on your own server.

By running services in containers, we can have a predictable and up-to-date setup, across multiple supported distros and CPU architectures.

This project is fairly new and only supports a few [services](docs/services/README.md) so far, but will grow to support self-hosting a large number of [FOSS](https://en.wikipedia.org/wiki/Free_and_open-source_software) pieces of software.


## Supported services

See the [full list of supported services here](docs/services/README.md).


## Installation

To configure and install service on your own server, follow the [README in the docs/ directory](docs/README.md).


## Changes

This playbook evolves over time, sometimes with backward-incompatible changes.

When updating the playbook, refer to [the changelog](CHANGELOG.md) to catch up with what's new.


## Support

- Matrix room: [#mash-playbook:devture.com](https://matrix.to/#/#mash-playbook:devture.com). To join Matrix, [use a public server](https://app.element.io) like `matrix.org` or self-host Matrix yourself using the related [matrix-docker-ansible-deploy](https://github.com/spantaleev/matrix-docker-ansible-deploy) Ansible playbook

- GitHub issues: [mother-of-all-self-hosting/mash-playbook/issues](https://github.com/mother-of-all-self-hosting/mash-playbook/issues)


## Related projects

You may also be interested in these other Ansible playbooks:

- [gitea-docker-ansible-deploy](https://github.com/spantaleev/gitea-docker-ansible-deploy) - for deploying a [Gitea](https://gitea.io/) git version-control server - this playbook will soon be merged into `mash-playbook`

- [nextcloud-docker-ansible-deploy](https://github.com/spantaleev/nextcloud-docker-ansible-deploy) - for deploying a [Nextcloud](https://nextcloud.com/) server - this playbook will soon be merged into `mash-playbook`

- [matrix-docker-ansible-deploy](https://github.com/spantaleev/matrix-docker-ansible-deploy) - for deploying a fully-featured [Matrix](https://matrix.org) homeserver

- [peertube-docker-ansible-deploy](https://github.com/spantaleev/peertube-docker-ansible-deploy) - for deploying a [PeerTube](https://joinpeertube.org/) video-platform server - this playbook will soon be merged into `mash-playbook`

- [vaultwarden-docker-ansible-deploy](https://github.com/spantaleev/vaultwarden-docker-ansible-deploy) - for deploying a [Vaultwarden](https://github.com/dani-garcia/vaultwarden) password manager server (unofficial [Bitwarden](https://bitwarden.com/) compatible server) - this playbook will soon be merged into `mash-playbook`

The [Matrix](https://matrix.org) playbook ([matrix-docker-ansible-deploy](https://github.com/spantaleev/matrix-docker-ansible-deploy)) will remain independent, because the Matrix ecosystem is incredibly large - lots of bots, bridges and other pieces of software. It deserves its own dedicated playbook.

All other playbooks are for smaller pieces and will be moved into into this playbook for ease of maintenance and all [reasons explained below](#why-create-such-a-mega-playbook).


## Why create such a mega playbook?

All our [Related](#related-projects) Ansible playbooks re-use roles (for Postgres, Traefik, etc.), but are still hard to maintain and there's a lot of duplication of effort.

Most of these playbooks host services which require a Postgres database, a Traefik reverse-proxy, a backup solution, etc. All of them need to come with documentation, etc.
All these things need to be created and kept up-to-date in each and every playbook.

Having to use a dedicated Ansible playbook for each and every piece of software means that you have to juggle many playbooks and make sure they don't conflict with one another when installing services on the same server. All [Related](#related-projects) playbooks interoperate nicely, but still require at least a bit of manual configuration to achieve this interoperability.

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


## What's with the name?

Our goal is to create a large Ansible playbook which can be your all-in-one-toolkit for self-hosting services in a clean and reliable way.

We like the MASH acronym, and [mashing](https://en.wikipedia.org/wiki/Mashing) is popular in the alcohol brewing industry. The result of all that mash is an enjoyable (at least by some) product.

Then, there's mixing and mashing stuff, which is also what this Ansible playbook is all about - you can mix and mash various pieces of software to create the self-hosted stack of your dreams!
