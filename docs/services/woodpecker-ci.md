<!--
SPDX-FileCopyrightText: 2020 Aaron Raimist
SPDX-FileCopyrightText: 2020 Chris van Dijk
SPDX-FileCopyrightText: 2020 Dominik Zajac
SPDX-FileCopyrightText: 2020 Mickaël Cornière
SPDX-FileCopyrightText: 2020-2024 MDAD project contributors
SPDX-FileCopyrightText: 2020-2025 Slavi Pantaleev
SPDX-FileCopyrightText: 2022 François Darveau
SPDX-FileCopyrightText: 2022 Julian Foad
SPDX-FileCopyrightText: 2022 Warren Bailey
SPDX-FileCopyrightText: 2023 Antonis Christofides
SPDX-FileCopyrightText: 2023 Felix Stupp
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 MASH project contributors
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 Sergio Durigan Junior
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Woodpecker CI

The playbook can install and configure [Woodpecker CI](https://woodpecker-ci.org/) for you.

Woodpecker CI is a [Continuous Integration](https://en.wikipedia.org/wiki/Continuous_integration) engine which can build and deploy your code automatically after pushing to a [Gitea](gitea.md) or [Forgejo](forgejo.md) repository.

>[!NOTE]
> If you are looking for an CI engine for Forgejo, you might also be interested in [Forgejo Runner](https://code.forgejo.org/forgejo/runner) that this playbook [supports](forgejo-runner.md) too.

A Woodpecker CI installation contains 2 components:

- one [Woodpecker CI **server**](#woodpecker-ci-server) (web interface, central management node)
- one or more [Woodpecker CI **agent**](#woodpecker-ci-agent) instances (which run your CI jobs)

>[!WARNING]
> It's better to run the **agent** instances elsewhere (not on the source-control server or a server serving anything of value) — on a machine that doesn't contain sensitive data.

Small installations which only run trusted CI jobs can afford to run an agent instance on the source-control server itself.

## Woodpecker CI server

For details about configuring the [Ansible role for Woodpecker CI server](https://github.com/mother-of-all-self-hosting/ansible-role-woodpecker-ci-server), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-woodpecker-ci-server/blob/main/docs/configuring-woodpecker-ci-server.md) online
- 📁 `roles/galaxy/woodpecker_ci_server/docs/configuring-woodpecker-ci-server.md` locally, if you have [fetched the Ansible roles](../installing.md)

### Dependencies — Woodpecker CI server

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server
- (optional) [Postgres](postgres.md) / MySQL / [MariaDB](mariadb.md) database — Woodpecker CI server will default to [SQLite](https://www.sqlite.org/) if Postgres is not enabled

### Configuration — Woodpecker CI server

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# woodpecker_ci_server                                                 #
#                                                                      #
########################################################################

woodpecker_ci_server_enabled: true

woodpecker_ci_server_hostname: mash.example.com
woodpecker_ci_server_path_prefix: /ci

########################################################################
#                                                                      #
# /woodpecker_ci_server                                                #
#                                                                      #
########################################################################
```

#### Set username matching VCS

It is necessary to specify one or more usernames that match your version control system (e.g. Gitea). Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-woodpecker-ci-server/blob/main/docs/configuring-woodpecker-ci-server.md#set-username-matching-vcs) on the role's documentation for details.

#### Select database to use (optional)

By default Woodpecker CI server is configured to use Postgres, but you can choose other database such as SQLite and MySQL (MariaDB). Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-woodpecker-ci-server/blob/main/docs/configuring-woodpecker-ci-server.md#specify-database-optional) on the role's documentation for details.

#### Gitea Integration

The Woodpecker CI server can integrate with [Gitea](gitea.md) by adding the following **additional** `vars.yml` configuration:

```yaml
woodpecker_ci_server_provider: gitea

# We must use the public URL here, because it's also used for login redirects
woodpecker_ci_server_config_gitea_url: "{{ gitea_config_root_url }}"

# Populate these with the OAuth 2 application information
# (see the Gitea configuration section above)
woodpecker_ci_server_config_gitea_client: GITEA_OAUTH_CLIENT_ID_HERE
woodpecker_ci_server_config_gitea_secret: GITEA_OAUTH_CLIENT_SECRET_HERE

woodpecker_ci_server_container_add_host_domain_name: "{{ gitea_hostname }}"
woodpecker_ci_server_container_add_host_ip_address: "{{ ansible_host }}"
```

#### Forgejo Integration

The Woodpecker CI server comes with built-in support for Forgejo.

To integrate it, you need to create an OAuth 2 application on a Forgejo instance at `https://FORGEJO_INSTANCE_URL_HERE/user/settings/applications` for Woodpecker CI server authorization. When creating one, set `https://FORGEJO_INSTANCE_URL_HERE/authorize` to the "Redirect URIs" text input area. Refer to [this section](https://woodpecker-ci.org/docs/administration/configuration/forges/forgejo#registration) on the Woodpecker CI's documentation for details.

After creating the application, add the following configuration to your `vars.yml` file:

```yaml
woodpecker_ci_server_provider: forgejo

# We must use the public URL here, because it's also used for login redirects
woodpecker_ci_server_config_forgejo_url: "{{ forgejo_config_root_url }}"

# Populate these with the OAuth 2 client ID and client secret
woodpecker_ci_server_config_forgejo_client: FORGEJO_OAUTH_CLIENT_ID_HERE
woodpecker_ci_server_config_forgejo_secret: FORGEJO_OAUTH_CLIENT_SECRET_HERE

woodpecker_ci_server_container_add_host_domain_name: "{{ forgejo_hostname }}"
woodpecker_ci_server_container_add_host_ip_address: "{{ ansible_host }}"
```

### Usage — Woodpecker CI server

After running the command for installation, the Woodpecker CI server becomes available at the URL specified with `woodpecker_ci_server_hostname` and `woodpecker_ci_server_path_prefix`. With the configuration above, the service is hosted at `https://mash.example.com/ci`.

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-woodpecker-ci-server/blob/main/docs/configuring-woodpecker-ci-server.md#usage) on the role's documentation for details about the usage.

## Woodpecker CI agent

For details about configuring the [Ansible role for Woodpecker CI agent](https://github.com/mother-of-all-self-hosting/ansible-role-woodpecker-ci-agent), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-woodpecker-ci-agent/blob/main/docs/configuring-woodpecker-ci-agent.md) online
- 📁 `roles/galaxy/woodpecker_ci_agent/docs/configuring-woodpecker-ci-agent.md` locally, if you have [fetched the Ansible roles](../installing.md)

### Dependencies — Woodpecker CI agent

This service requires the following other services:

- Woodpecker CI server

### Configuration — Woodpecker CI agent

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# woodpecker_ci_agent                                                  #
#                                                                      #
########################################################################

woodpecker_ci_agent_enabled: true

########################################################################
#                                                                      #
# /woodpecker_ci_agent                                                 #
#                                                                      #
########################################################################
```

### Usage — Woodpecker CI agent

The agent should automatically register with the Woodpecker CI server and take jobs from it.

## Related services

- [Forgejo Runner](forgejo-runner.md) — Runner to use with Forgejo Actions
- [GitLab Runner](gitlab-runner.md) — Runner to use with GitLab CI/CD
