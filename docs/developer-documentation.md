<!--
SPDX-FileCopyrightText: 2024 Bergrübe
SPDX-FileCopyrightText: 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Developer documentation

## Support a new service | Create your own role

Are you interested in adding a new service which is not yet [available on this playbook](supported-services.md)? Great! By following the guide below, you can easily implement one to the playbook.

### 1. Get started

Before working on implementation, check if:

- the role does not exist already in [`supported-services.md`](supported-services.md) and no one else is already [working on it](https://github.com/mother-of-all-self-hosting/mash-playbook/pulls)

- the service you wish to add can run in a Docker container

- a container image already exists

### 2. Create an Ansible role in a public git repository

To support a new service, at first you need to create an Ansible role for it in its public git repository. It does not have to be maintained on a specific forge like GitHub; you can use GitLab, Codeberg, or anywhere you choose. Note that the instance should be stable and globally available as the roles are to be fetched anytime.

When it comes to the structure of roles, you can follow existing roles such as [`ansible-role-postgres`](https://github.com/mother-of-all-self-hosting/ansible-role-postgres), [`ansible-role-syncthing`](https://github.com/mother-of-all-self-hosting/ansible-role-syncthing), and [`ansible-role-ntfy`](https://github.com/mother-of-all-self-hosting/ansible-role-ntfy). Generally, it is not recommended to create a role from the scratch as it can lack important variables required for the playbook. If you are not quite sure where to start, your best bet would be to copy the existing (and recently updated) role maintained by [MASH project](https://github.com/mother-of-all-self-hosting), and reuse it as a template.

💡 **Notes**:
- Your role's file structure should be similar to this tree:
    ```
    .
    ├── defaults/
    │   └── main.yml
    ├── docs/
    │   └── configuring-YOUR-SERVICE.md
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
    ├── justfile
    ├── LICENSE
    └── README.md
    ```
- You will also need to decide on a licence. Otherwise ansible-galaxy won't work. We recommend AGPLv3, as it is adoped by the most roles of the MASH playbook.
- If you are committed to free software, you might probably be interested in publishing the role based on [REUSE](https://reuse.software/), an initiative by [FSFE](https://fsfe.org/).

### 3. Update the MASH playbook to support your created Ansible role

There are a few files that you need to adapt:

```
.
├── docs/
│   ├── supported-services.md  -> Add your service
│   └── services/
│       └── YOUR-SERVICE.md  -> Add documentation about how to configure it
├── templates/
│   ├── group_vars_mash_servers  -> Add default configuration
│   └── requirements.yml  -> Add your Ansible role
│   └── setup.yml  -> Add your Ansible role
```

💡 Make sure to edit configuration files inside `templates` — These are source files to be optimized and used when running [`just`](just.md) commands to install, configure, or uninstall services.

#### Add the role to `group_vars_mash_servers` in `templates` directory

On `group_vars_mash_servers` you need to wire your role with the rest of the services of the playbook — integrating with the service manager or potentially with other roles.

When adding the role, replace `YOUR-SERVICE` with yours, and also mind the place to add the role, as the roles are (mostly) sorted alphabetically for other developers' sanity.

See below for details about what to configure. Note that not all roles require to be wired to anything other than `systemd_service_manager`.

<details>
<summary>Wire the role to systemd_service_manager</summary>

You have to add the role to `mash_playbook_devture_systemd_service_manager_services_list_auto_itemized` so that it is wired to `systemd_service_manager`.

See below for an example:

```yaml
# role-specific:systemd_service_manager
########################################################################
#                                                                      #
# systemd_service_manager                                              #
#                                                                      #
########################################################################

mash_playbook_devture_systemd_service_manager_services_list_auto_itemized:
  [...]
  # role-specific:YOUR-SERVICE
  - |-
    {{ ({'name': (YOUR-SERVICE_identifier + '.service'), 'priority': 2000, 'groups': ['mash', 'YOUR-SERVICE']} if YOUR-SERVICE_enabled else omit) }}
  # /role-specific:YOUR-SERVICE

[...]
########################################################################
#                                                                      #
# /systemd_service_manager                                             #
#                                                                      #
########################################################################
# /role-specific:systemd_service_manager

```
</details>

**Optional**:

Please wire your role to other services than `systemd_service_manager` if necessary.

<details>
<summary>Wire the role to Postgres / MariaDB</summary>

On this playbook Postgres is enabled by default (see [`examples/vars.yml`](../examples/vars.yml)), and you can wire your role to Postgres by adding it to the configuration for Postgres as below:

```yaml
# role-specific:postgres
########################################################################
#                                                                      #
# postgres                                                             #
#                                                                      #
########################################################################
[...]

mash_playbook_postgres_managed_databases_auto_itemized:
  [...]
  # role-specific:YOUR-SERVICE
  - |-
    {{
      ({
        'name': YOUR-SERVICE_database_name,
        'username': YOUR-SERVICE_database_username,
        'password': YOUR-SERVICE_database_password,
      } if YOUR-SERVICE_enabled else omit)
    }}
  # /role-specific:YOUR-SERVICE

  [...]
########################################################################
#                                                                      #
# /postgres                                                            #
#                                                                      #
########################################################################
# /role-specific:postgres

[...]

# role-specific:YOUR-SERVICE
########################################################################
#                                                                      #
# YOUR-SERVICE                                                         #
#                                                                      #
########################################################################

YOUR-SERVICE_systemd_required_services_list_auto: |
  {{
    ([postgres_identifier ~ '.service'] if postgres_enabled and YOUR-SERVICE_database_hostname == postgres_identifier else [])
  }}

YOUR-SERVICE_container_additional_networks_auto: |
  {{
    [...]
    +
    ([postgres_container_network] if postgres_enabled and YOUR-SERVICE_database_hostname == postgres_identifier and YOUR-SERVICE_container_network != postgres_container_network else [])
  }}

[...]

# role-specific:postgres
YOUR-SERVICE_database_hostname: "{{ postgres_identifier if postgres_enabled else '' }}"
YOUR-SERVICE_database_port: "{{ '5432' if postgres_enabled else '' }}"
YOUR-SERVICE_database_password: "{{ '%s' | format(mash_playbook_generic_secret_key) | password_hash('sha512', 'db.yourservice', rounds=655555) | to_uuid }}"
YOUR-SERVICE_database_username: "{{ YOUR-SERVICE_identifier }}"
# /role-specific:postgres

########################################################################
#                                                                      #
# /YOUR-SERVICE                                                        #
#                                                                      #
########################################################################
# /role-specific:YOUR-SERVICE
```

💡 If your role requires MySQL, you can instead wire it to MariaDB on this playbook via `mash_playbook_mariadb_managed_databases_auto_itemized` in a similar way. See the [service documentation](services/mariadb.md) for details about managing a MariaDB instance.

</details>

<details>
<summary>Wire the role to exim-relay (mailer)</summary>

This playbook implements [exim-relay](https://github.com/devture/exim-relay), a SMTP mailer service.

Various services need to send out email, and exim-relay gives you a centralized place for configuring email-sending.

To wire the role to exim-relay, add the configuration for it as below:

```yaml
[...]

# role-specific:YOUR-SERVICE
########################################################################
#                                                                      #
# YOUR-SERVICE                                                         #
#                                                                      #
########################################################################

[...]

YOUR-SERVICE_container_additional_networks_auto: |
  {{
	[...]
	+
    ([exim_relay_container_network | default('mash-exim-relay')] if (exim_relay_enabled | default(false) and YOUR-SERVICE_config_mailer_smtp_addr == exim_relay_identifier | default('mash-exim-relay') and YOUR-SERVICE_container_network != exim_relay_container_network) else [])
  }}

# role-specific:exim_relay
YOUR-SERVICE_config_mailer_enabled: "{{ exim_relay_enabled }}"
YOUR-SERVICE_config_mailer_smtp_addr: "{{ exim_relay_identifier if exim_relay_enabled else '' }}"
YOUR-SERVICE_config_mailer_smtp_port: 8025
YOUR-SERVICE_config_mailer_from: "{{ exim_relay_sender_address if exim_relay_enabled else '' }}"
YOUR-SERVICE_config_mailer_protocol: "{{ 'smtp' if exim_relay_enabled else '' }}"
# /role-specific:exim_relay

########################################################################
#                                                                      #
# /YOUR-SERVICE                                                        #
#                                                                      #
########################################################################
# /role-specific:YOUR-SERVICE
```
</details>

<details>
<summary>Wire the role to Hubsite (static site for services overview)</summary>

[Hubsite](https://github.com/moan0s/hubsite) is a service which provides you with a simple static site that shows an overview of the available services.

Adding the role to Hubsite is not a hard requirement to add the role to the playbook, but it is recommended to do so, so that you (and visitors of your services) can easily navigate to the services available on your server.

To wire the role to Hubsite, add the configuration for it as below:

```yaml
[...]
# role-specific:hubsite
########################################################################
#                                                                      #
# hubsite                                                              #
#                                                                      #
########################################################################
[...]

# Services
##########
[...]

# role-specific:YOUR-SERVICE
# YOUR-SERVICE
hubsite_service_YOUR-SERVICE_enabled: "{{ YOUR-SERVICE_enabled }}"
hubsite_service_YOUR-SERVICE_name: "YOUR-SERVICE Name"
hubsite_service_YOUR-SERVICE_url: "https://{{ YOUR-SERVICE_hostname }}{{ YOUR-SERVICE_path_prefix }}"
hubsite_service_YOUR-SERVICE_logo_location: "{{ role_path }}/assets/YOUR-SERVICE.svg"
hubsite_service_YOUR-SERVICE_description: "YOUR-SERVICE Description"
hubsite_service_YOUR-SERVICE_priority: 1000
# /role-specific:YOUR-SERVICE
[...]

mash_playbook_hubsite_service_list_auto_itemized:
  [...]
  # role-specific:YOUR-SERVICE
  - |-
    {{
      ({
        'name': hubsite_service_YOUR-SERVICE_name,
        'url': hubsite_service_YOUR-SERVICE_url,
        'logo_location': hubsite_service_YOUR-SERVICE_logo_location,
        'description': hubsite_service_YOUR-SERVICE_description,
        'priority': hubsite_service_YOUR-SERVICE_priority,
      } if hubsite_service_YOUR-SERVICE_enabled else omit)
    }}
  # /role-specific:YOUR-SERVICE
[...]
```

💡 **Notes**:
- Setting a logo is optional.
- If the service of your role distributes its logo under free licenses, you can add it to [`ansible-role-hubsite/assets`](https://github.com/mother-of-all-self-hosting/ansible-role-hubsite/tree/main/assets) via a pull request.

</details>

### Additional hints

Please consider to add a line like `# Project source code URL: YOUR-SERVICE-GIT-REPO` to your Ansible role's `defaults/main.yml` file, so that [`bin/feeds.py`](/bin/feeds.py) can automatically find the Atom/RSS feed for new releases.

If you have any questions, you are welcomed to join the Matrix room for the MASH playbook and free free to ask: https://matrix.to/#/%23mash-playbook:devture.com
