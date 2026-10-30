<!--
SPDX-FileCopyrightText: 2020 Aaron Raimist
SPDX-FileCopyrightText: 2020 Chris van Dijk
SPDX-FileCopyrightText: 2020 Dominik Zajac
SPDX-FileCopyrightText: 2020 Mickaël Cornière
SPDX-FileCopyrightText: 2020-2024 MDAD project contributors
SPDX-FileCopyrightText: 2020-2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2022 François Darveau
SPDX-FileCopyrightText: 2022 Julian Foad
SPDX-FileCopyrightText: 2022 Warren Bailey
SPDX-FileCopyrightText: 2023 Antonis Christofides
SPDX-FileCopyrightText: 2023 Felix Stupp
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 Thomas Miceli
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# kukaroll

The playbook can install and configure [kukaroll](https://github.com/devture/kukaroll) for you.

kukaroll implements "git push to deploy" for projects checked out on the server. When you push, your forge (Forgejo, Gitea or GitHub) notifies kukaroll via a webhook, and kukaroll moves the project's checkout to the tip of its branch and runs the project's own deploy command.

See the project's [documentation](https://github.com/devture/kukaroll/blob/main/docs/README.md) to learn what kukaroll does and why it might be useful to you.

For details about configuring the [Ansible role for kukaroll](https://github.com/mother-of-all-self-hosting/ansible-role-kukaroll), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-kukaroll/blob/main/docs/configuring-kukaroll.md) online
- 📁 `roles/galaxy/kukaroll/docs/configuring-kukaroll.md` locally, if you have [fetched the Ansible roles](../../docs/installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](../traefik/README.md) reverse-proxy server (or another reverse proxy; refer to the role's documentation)

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../../docs/installing.md) process:

```yaml
########################################################################
#                                                                      #
# kukaroll                                                             #
#                                                                      #
########################################################################

kukaroll_enabled: true

kukaroll_hostname: mash.example.com
kukaroll_path_prefix: /kukaroll

kukaroll_projects:
  myapp:
    checkout: /srv/myapp
    remote: origin
    branch: main
    git_user: myapp
    hooks_user: root
    lock_file: /srv/myapp/var/deploy.lock
    pre_flight: null
    deploy: [just, deploy]
    healthchecks_ping_url: null
    webhook_provider: forgejo
    webhook_secret: A_LONG_RANDOM_STRING
    webhook_authorization_header: "Bearer ANOTHER_LONG_RANDOM_STRING"

########################################################################
#                                                                      #
# /kukaroll                                                            #
#                                                                      #
########################################################################
```

With the configuration above, the webhook URL of `myapp` is set to `https://mash.example.com/kukaroll/hooks/myapp`. Refer to The role's documentation for how to set up the webhook on the forge, including details about project keys.

>[!WARNING]
> Whoever can push to a deployed branch, or write to the checkout, can run commands on the server as the project's `hooks_user`. With `hooks_user: root`, treat the git user's account as root.

### Pausing deploys while services restart

When the playbook starts, restarts or stops services, it pauses deploys first, and resumes them once the services are up again, so that no deploy works on a project while its services restart.

`just install-service <service>` and `just setup-service <service>` pause deploys only when the service is in `mash_playbook_kukaroll_deploys_service_manager_groups`. If a project deploys a service which this playbook manages, add that service's group by adding the following configuration to your `vars.yml` file:
:

```yaml
mash_playbook_kukaroll_deploys_service_manager_groups: [mash, kukaroll, myapp]
```

## Usage

After installation, push to a deployed branch, or deploy right away from the server:

```sh
/mash/kukaroll/bin/trigger myapp
```

See the role's documentation for the other helpers, logs and pausing deploys by hand.
