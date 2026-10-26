<!--
SPDX-FileCopyrightText: 2024 Bergrübe
SPDX-FileCopyrightText: 2024, 2026 Slavi Pantaleev
SPDX-FileCopyrightText: 2025, 2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Developer documentation

## Style guide for playbook developers

This section describes the conventions used when developing this playbook and writing its documentation. Follow it when adding a new component (a role and its documentation page) or editing existing ones, so that everything stays consistent.

The guide is meant for anyone preparing a contribution. If you find existing files that deviate from it, feel free to send a pull request bringing them in line.

### Language

- Write in English, using American spelling ("customize", not "customise").
- Proper nouns are capitalized: Ansible, Docker, Traefik, Postgres, Grafana, etc. Some projects deliberately brand themselves in lowercase (e.g. `authentik`, `coturn`) and keep their lowercase name even at the start of a sentence. When in doubt, follow the upstream project's own spelling.

### Markdown style

- Do not hard-wrap prose. Each paragraph is a single line in the source file, no matter how long. This keeps the source and the rendered result consistent and makes diffs easier to work with.
- Number ordered lists sequentially (`1.`, `2.`, `3.`), instead of relying on the Markdown renderer to fix a repeated (`1.`, `1.`, `1.`) or wrong (`1.`, `2.`, `4.`) sequence.
- Use `-` for unordered lists.
- Wrap variable names, file paths, commands, domains, and service names in backticks (`` ` ``).
- Use fenced code blocks with a language hint (```` ```yaml ````, ```` ```sh ````) for configuration and command examples.
- Use relative links when linking between documentation pages (e.g. `[Configuring DNS](configuring-dns.md)`).

### Miscellaneous

- Link to the role's documentation instead of duplicating its content (installation steps, distro-specific commands, etc.). Copied instructions go stale; links age much better.
- Reuse existing files to minimize inconsistencies.
- When reusing, copyright attributions must be preserved on the files. Never strip them away, and **do not pretend you were the sole original author.** This often happens when a Gen-AI / LLM is involved, and it is your responsibility to avoid this slop. Additionally, consider to add URLs to the original files in a commit message, so that one can easily trace and verify the relationship between you and the authors.

## Support a new service | Create your own role

Are you interested in adding a new service which is not yet [available on this playbook](supported-services.md)? Great! By following the guide below, you can easily implement one to the playbook.

If you have any questions, you are welcomed to join the Matrix room for the MASH playbook and free free to ask: <https://matrix.to/#/%23mash-playbook:devture.com>

### 1. Get started

Before working on implementation, check if:

- the role does not exist already in [`supported-services.md`](supported-services.md) and no one else is already [working on it](https://github.com/mother-of-all-self-hosting/mash-playbook/pulls)

- the service you wish to add can run in a Docker container

- a container image already exists

### 2. Create an Ansible role in a public git repository

To support a new service, at first you need to create an Ansible role for it in its public git repository. It does not have to be maintained on a specific forge like GitHub; you can use GitLab, Codeberg, or anywhere you choose. Note that the instance should be stable and globally available as the roles are to be fetched anytime.

When it comes to the structure of roles, you can follow existing roles such as [`ansible-role-echoip`](https://github.com/mother-of-all-self-hosting/ansible-role-echoip), [`ansible-role-readeck`](https://github.com/mother-of-all-self-hosting/ansible-role-readeck), and [`ansible-role-syncthing`](https://github.com/mother-of-all-self-hosting/ansible-role-syncthing). Generally, it is not recommended to create a role from the scratch as it can lack important variables required for the playbook. If you are not quite sure where to start, your best bet would be to copy the existing (and recently updated) role maintained by [MASH project](https://github.com/mother-of-all-self-hosting), and reuse it as a template.

💡 **Notes**:

- Your role's file structure should be similar to this tree:

    ```txt
    .
    ├── .github/
    │   ├── renovate.json
    │   └── workflows/
    │       ├── autotag.yml
    │       └── pre-commit.yml
    ├── defaults/
    │   └── main.yml
    ├── docs/
    │   └── configuring-YOUR-SERVICE.md
    ├── LICENSES
    │   ├── AGPL-3.0-or-later.txt
    │   └── CC0-1.0.txt
    ├── meta/
    │   └── main.yml
    ├── tasks/
    │   ├── main.yml
    │   ├── install.yml
    │   ├── uninstall.yml
    │   └── validate_config.yml
    ├── templates/
    │   ├── env.j2
    │   ├── labels.j2
    │   └── systemd/
    │       └── YOUR-SERVICE.service.j2
    ├── .ansible-lint
    ├── .gitignore
    ├── .pre-commit-config.yaml
    ├── .yamllint.yml
    ├── justfile
    ├── LICENSE
    ├── mise.toml
    ├── README.md
    └── REUSE.toml
    ```

- You will also need to decide on a licence. Otherwise ansible-galaxy won't work. We recommend AGPLv3, as it is adoped by the most roles of the MASH playbook.
- If you are committed to free software, you might probably be interested in publishing the role based on [REUSE](https://reuse.software/), an initiative by [FSFE](https://fsfe.org/).
- It is recommended to set up a Git pre-commit hook (via [mise](https://mise.jdx.dev/) + [prek](https://prek.j178.dev/)) that runs formatting and linting checks before each commit, and make sure that your role passes the linter before submitting. `.pre-commit-config.yaml` defines which hooks are to be executed.
- Please consider to add a line like `# Project source code URL: YOUR-SERVICE-GIT-REPO` to your Ansible role's `defaults/main.yml` file, so that [`bin/feeds.py`](/bin/feeds.py) can automatically find the Atom/RSS feed for new releases.

### 3. Update the MASH playbook to support your created Ansible role

Each role the playbook can use is wired in by a *component*: a directory in [`components/`](../components) named after the role. To add your role, add its component and its documentation:

```txt
.
├── components/
│   └── YOUR-SERVICE/
│       ├── component.yml  ← When the component is in use, where it runs, what it adds to other components
│       ├── README.md  ← Documentation about how to configure the service
│       ├── requirements.yml  ← Your Ansible role and its version
│       ├── wiring.yml  ← Default configuration of your role for this playbook
│       ├── assets/  ← Media files (pictures, sound files, etc.) to be attached to the documentation
│       └── with/
│           ├── postgres.yml  ← Configuration which applies only when Postgres is in use too
│           └── traefik.yml  ← … or Traefik, etc.
└── docs/
    └── supported-services.md  ← Add your service
```

>[!NOTE]
> Before every run, `just` generates `requirements.yml`, `setup.yml` and `group_vars/mash_servers/` from the components in use by the inventory (see [`bin/optimize.py`](../bin/optimize.py)). Do not edit those generated files.

Components can also live in the inventory, to extend the playbook without changing it (refer to [this page](extending-the-playbook.md)).

💡 The easiest way to start is to copy the component of a similar service and adapt it. It is recommended to take a look at the components as below first to grasp the whole picture:

- [`actual`](../components/actual): simple one with Traefik
- [`freescout`](../components/freescout): with multiple databases (Postgres, MariaDB, SQLite)
- [`pinepods`](../components/postgres): with multiple databases and a Valkey data-store
- [`opengist`](../components/opengist): with multiple databases, an additional component (Meilisearch), and optional Prometheus metrics
- [`reitti`](../components/reitti): with multiple systemd services
- [`postgres`](../components/postgres): entries from other components
- [`docker`](../components/docker): with a special entry in `setup.yml`

#### `component.yml`

<details>
<summary>Click here to display the details</summary>

```yaml
# The component is in use when the inventory sets any variable starting with this prefix (`''`: always in use)
activation_prefix: YOUR-SERVICE_

# Entries added to other components' lists, while those components are in use (see below)
inject:
  systemd_service_manager:
    services:
      - name: "{{ YOUR-SERVICE_identifier }}.service"
        priority: 2000
        restart_necessary: "{{ YOUR-SERVICE_restart_necessary | bool }}"
        groups: [mash, YOUR-SERVICE]
        when: "{{ YOUR-SERVICE_enabled }}"
```

Optional fields:

- `setup`: where the role runs in `setup.yml`. Components without it run `galaxy/YOUR-SERVICE` at priority `1000`, sorted by name with the others. A lower `priority` runs earlier, and `entry` replaces the default entry (e.g. to add `when` or `tags`):

    ```yaml
    setup:
      priority: 140
      entry:
        - role: galaxy/docker
          when: mash_playbook_docker_installation_enabled | bool
    ```

    `setup` may also be a list of such placements, for a component which runs in several places, or `[]` for one which runs nothing. Role paths starting with `./` (e.g. `./roles/YOUR-ROLE`) are relative to the component's directory.

- `accepts`: lists which other components can add entries to (with `inject`), for components such as Postgres. `into` names the variable which gets the entries of the components in use (those whose `when` is true, without `when`), and `required_keys` the keys each entry needs:

    ```yaml
    accepts:
      managed_databases:
        description: Databases (and users) to create and keep up to date
        into: postgres_managed_databases_auto
        required_keys: [name, password, username]
    ```

- `inject`: entries for other components' lists, as shown above. Each entry is added only while that component is in use, and only if its `when` (true when omitted) is true. Look at the `accepts` of a component for the lists it has. Ansible versions before 2.19 evaluate all entries of a list, also those whose `when` is false, so an entry must not fail when its component is disabled (e.g. use `default()` for variables which may be undefined then).

</details>

#### `requirements.yml`

<details>
<summary>Click here to display the details</summary>

Your role, as for `ansible-galaxy`. The name must match the component's directory:

```yaml
- src: git+https://github.com/YOUR-USERNAME/ansible-role-YOUR-SERVICE.git
  version: v1.0.0-0
  name: YOUR-SERVICE
```

</details>

#### `wiring.yml` and `with/`

<details>
<summary>Click here to display the details</summary>

`wiring.yml` holds the default configuration of your role for this playbook, which applies whenever the component is in use. `with/OTHER.yml` holds configuration which applies only when the `OTHER` component is in use too. A variable may only be defined in one of these files.

Keep the playbook's variables and the roles' variables apart:

- Only set variables which the role has. Setting one which it does not have (e.g. after the role renamed it) has no effect, and nothing reports it.
- Name variables which the playbook defines for itself (e.g. a value which several components use, or a switch for an integration) `mash_playbook_*`, not after a role, so that they are not mistaken for the role's.
- Leave the role's variables meant for users (e.g. `*_custom`, `*_additional_labels` and `*_additional_variables`) to them. The playbook sets the `*_auto` ones, and if a role lacks a variable for something, add one to the role. A pre-commit hook (`bin/check-components-user-variables.py`) checks this by the variables' names.

```yaml
# wiring.yml

# The role enables itself by default. It stays disabled, unless enabled in your inventory.
YOUR-SERVICE_enabled: false

YOUR-SERVICE_identifier: "{{ mash_playbook_service_identifier_prefix }}YOUR-SERVICE"

YOUR-SERVICE_base_path: "{{ mash_playbook_base_path }}/{{ mash_playbook_service_base_directory_name_prefix }}YOUR-SERVICE"

YOUR-SERVICE_uid: "{{ mash_playbook_uid }}"
YOUR-SERVICE_gid: "{{ mash_playbook_gid }}"
```

Variables referring to another component which may not be in use need a default, e.g. `postgres_enabled | default(false)`.

💡 Please do not use `mash_playbook_generic_secret_key` for a fixed string for something like passwords, because it is intended for secrets that are fine to be changed later.

Not all roles need to be wired to anything other than `systemd_service_manager` (see `inject` above). Wire your role to other services if necessary:

<details>
<summary>Wire the role to Postgres / MariaDB</summary>

On this playbook Postgres is enabled by default (refer to [`examples/vars.yml`](../examples/vars.yml)). To have Postgres create the database for your service, add it to `component.yml`:

```yaml
inject:
  [...]
  postgres:
    managed_databases:
      - name: "{{ YOUR-SERVICE_database_name }}"
        username: "{{ YOUR-SERVICE_database_username }}"
        password: "{{ YOUR-SERVICE_database_password }}"
        when: "{{ YOUR-SERVICE_enabled and (YOUR-SERVICE_database_hostname == postgres_connection_hostname or YOUR-SERVICE_database_socket_enabled) }}"
```

Make your service depend on Postgres and join its network in `wiring.yml`:

```yaml
YOUR-SERVICE_systemd_required_services_list_auto: |
  {{
    ([postgres_identifier ~ '.service'] if postgres_enabled | default(false) and (YOUR-SERVICE_database_hostname == postgres_connection_hostname or YOUR-SERVICE_database_socket_enabled) else [])
  }}

YOUR-SERVICE_container_additional_networks_auto: |
  {{
    [...]
    +
    ([postgres_container_network] if postgres_enabled | default(false) and (YOUR-SERVICE_database_hostname == postgres_connection_hostname and YOUR-SERVICE_container_network != postgres_container_network and not YOUR-SERVICE_database_socket_enabled) else [])
  }}
```

And point it at Postgres in `with/postgres.yml`:

```yaml
YOUR-SERVICE_database_hostname: "{{ postgres_connection_hostname if postgres_enabled and not YOUR-SERVICE_database_socket_enabled else '' }}"
YOUR-SERVICE_database_port: "{{ postgres_connection_port if postgres_enabled else '5432' }}"
YOUR-SERVICE_database_password: "{{ (mash_playbook_generic_secret_key + ':YOUR-SERVICE.db') | hash('sha512') | to_uuid }}"
YOUR-SERVICE_database_sslmode: "{{ 'disable' if postgres_enabled and (YOUR-SERVICE_database_hostname == postgres_connection_hostname or YOUR-SERVICE_database_socket_enabled) else 'prefer' }}"
YOUR-SERVICE_database_socket_path_host: "{{ postgres_run_path }}"
```

The example above presupposes that the role is configured to wire the service to Postgres with a Unix socket. Adjust it as necessary if the service does not support one.

💡 **Notes**:

- If your role requires MySQL, you can instead wire it to MariaDB on this playbook via `inject.mariadb.managed_databases` and `with/mariadb.yml` in a similar way. See the [service documentation](../components/mariadb/README.md) for details about managing a MariaDB instance.
- If the service supports multiple database drivers (MySQL, Postgres, SQLite, etc.), please prepare a `YOUR-SERVICE_database_type` variable on `defaults/main.yml` *without setting a default value*, so that users will be able to choose which one to use by themselves. Though a default database driver is specified for some roles in their component with a value such as `"{{ 'postgres' if postgres_enabled | default(false) else 'sqlite' }}"`, it is not a best practice, and should be avoided for a new role. Please refer to <https://github.com/mother-of-all-self-hosting/mash-playbook/issues/1061> for the context.

</details>

<details>
<summary>Wire the role to exim-relay (mailer)</summary>

This playbook implements [exim-relay](https://github.com/devture/exim-relay), a SMTP mailer service.

Various services need to send out email, and exim-relay gives you a centralized place for configuring email-sending.

To wire the role to exim-relay, add the configuration for it to `wiring.yml`:

```yaml
YOUR-SERVICE_systemd_wanted_services_list_auto: |
  {{
    ([exim_relay_identifier ~ '.service'] if exim_relay_enabled | default(false) and YOUR-SERVICE_config_mailer_smtp_addr == exim_relay_identifier else [])
  }}

YOUR-SERVICE_container_additional_networks_auto: |
  {{
    [...]
    +
    ([exim_relay_container_network] if exim_relay_enabled | default(false) and YOUR-SERVICE_config_mailer_smtp_addr == exim_relay_identifier and YOUR-SERVICE_container_network != exim_relay_container_network else [])
  }}
```

And to `with/exim_relay.yml`:

```yaml
YOUR-SERVICE_config_mailer_enabled: "{{ exim_relay_enabled }}"
YOUR-SERVICE_config_mailer_smtp_addr: "{{ exim_relay_identifier if exim_relay_enabled else '' }}"
YOUR-SERVICE_config_mailer_smtp_port: 8025
YOUR-SERVICE_config_mailer_from: "{{ exim_relay_sender_address if exim_relay_enabled else '' }}"
YOUR-SERVICE_config_mailer_protocol: "{{ 'smtp' if exim_relay_enabled else '' }}"
```

</details>

</details>

### 4. Make sure the playbook can actually install a service with the role

If you are willing to submit the change to this repository, please make sure that the role is integrated with the playbook properly, and the playbook can install a service with the role as expected. This is an important step which should never be skipped.

Our pick to **test a role** is to use a [Molecule](https://docs.ansible.com/projects/molecule/) test framework. It is versatile, simulates installation in a predictable way, and helps you to spot an implementation bug before it is published.

>[!NOTE]
> If you look at the roles maintained by the MASH organization, you might be overwhelmed with intensiveness and aggressiveness of the Molecule test implementation. It is basically because the team enables patch level automerging with Renovate for them and wants to make sure as much as possible that they can be successfully updated without causing a disruption. *Verifying that the service that the role installs works is by default out-of-scope of the tests, and not your responsibility either*, though it might be appreciated.
>
> If you are not familiar with Molecule, it is fine not to implement a test with it. Please avoid making something up which you cannot confirm by yourself that it really works as expected (by using Gen-AI / LLM, etc). A defected test is worse than not having one in the first place.

However, please do note that *it is not (yet) possible to check with Molecule whether the playbook can install a service with the role as expected*. In other words, passing Molecule tests on the side of the role has nothing to with whether the role is properly implemented to the playbook; even if Molecule tests will be implemented to the playbook, it won't be nothing more than a mere simulation, under certain specific conditions. **It is always encouraged to confirm with your own eyes that the service has become usable on an actual machine, and discouraged to rely on a simulation by a Gen-AI / LLM or something else to assume the service probably might be installed.** Such implementation can be labelled as a AI slop, and dropped from the playbook.

There are several ways of testing the playbook; from using a local virtual machine to running the locally modified playbook against an actual machine, and so on. In these cases, creating a symbolic link to the role's directory inside `roles/galaxy` should make it easier to test the role while debugging it, as you won't have to delete the directory and recreate it again and again. The playbook never replaces or deletes such symlinked roles (see [Roles you are working on](just.md#roles-you-are-working-on)).

### 5. Maintain your role

While the roles managed under [the MASH organization](https://github.com/orgs/mother-of-all-self-hosting) are maintained and updated when necessary by the organization in general, it is essentially your responsibility to maintain yours, though an organization member might send a push request to your role's repository to apply such changes that have been added to the MASH roles in order to improve maintainability (by sharing codebase).

If the role is regarded to have been abandoned by the author from the viewpoint of common sense (the role being unusable for a long time, for example), the MASH organization might fork the repository at will to resurrect the role to make it usable on the MASH playbook. However, if it simply stopped working or blocks the playbook from running, the role can be removed from the playbook until the issue will be fixed — though this has not happened yet.

Please keep an eye on the roles maintained by the MASH organization to keep yours up-to-date by adding proper changes if any. Since the background of the decision for the changes are usually not announced (though you may find references in a commit message), you might as well to ask an organization member on the Matrix room about changes you are expected to apply.

Please do not hesitate to ask for help to let the community members help you! 👋

## Local directories: `run/` and `var/`

Both directories are ignored by git, but they are not interchangeable:

- `run/` holds state that the playbook keeps between runs, such as whether optimization is enabled, and checksums of the roles installed into `roles/galaxy/`, used to detect local changes to them. Deleting it changes how the playbook behaves.
- `var/` holds data of development tools (mise, prek) and temporary files of tests. It can be deleted at any time; the tools set it up again when needed.

## Reviewing role dependency updates

Renovate opens pull requests for Ansible role version updates instead of merging their branches directly. Review the released role changes and the playbook wiring before merging; a role update may need a playbook adaptation even when its role tests pass. In particular, check that the variables the components set still exist in the role (see [`wiring.yml` and `with/`](#wiringyml-and-with)). Other dependency classes retain their separate Renovate policies.

## Maintaining the Renovate runner

The self-hosted runner version is pinned in [`.github/workflows/renovate.yml`](../.github/workflows/renovate.yml). Renovate updates this pin and automerges passing updates during the monthly window configured in [`.github/renovate.json`](../.github/renovate.json).

The `Renovate smoke test` workflow tests the candidate image on branch pushes and fork pull requests. It validates configuration and starts the real Renovate runtime to extract dependencies from the checked-out repository. It requires results from every manager currently used here, including the custom manager that updates Renovate itself, and rejects errors or missing completion logs. The containers have no network access, receive no credentials, and mount the checkout read-only.

Run the same check locally with Docker, Bash, and jq installed:

```sh
bin/renovate-smoke-test.sh
# Test a candidate image without changing the workflow pin:
bin/renovate-smoke-test.sh 44.64.0
```

Version `44.64.0` is deliberately excluded from runner updates: its APK datasource imports `tar`, which was only declared as a development dependency and is missing from the production image. It passed configuration validation and `--version`, then crashed at startup with exit code 0 ([incident log](https://github.com/mother-of-all-self-hosting/mash-playbook/actions/runs/34634294937/job/103378353720)). The runner was reverted to `44.61.6`. Both production and the smoke test set `NODE_OPTIONS=--unhandled-rejections=strict` so unhandled startup failures return a failing exit code.

Upstream corrected the packaging in [Renovate PR #45699](https://github.com/renovatebot/renovate/pull/45699). A runner that crashes before processing the repository cannot discover its own replacement, so recovery requires manually changing the pin to a working version.

This smoke test would have blocked that upgrade. It does not exercise registry lookups, GitHub authentication, or branch/PR writes. For live integration checks, manually dispatch the `Renovate` workflow on `main` with `dry_run` enabled and `log_level` set to `debug`. That tests the pin already on `main`; it is not a pre-merge test of a candidate branch. GitHub's current default-branch rules protect against deletion and force pushes, but do not require CI checks, so manual merges must also check the smoke-test result.
