# Developer documentation

## Support a new service | Create your own role

### 1. Check if

- the role doesn't exist already in [`supported-services.md`](supported-services.md) and no one else is already [working on it](https://github.com/mother-of-all-self-hosting/mash-playbook/pulls)

- the service you wish to add can run in a Docker container

- a container image already exists

### 2. Create the Ansible role in a public git repository.
You can follow the structure of existing roles, like the [`ansible-role-gitea`](https://github.com/mother-of-all-self-hosting/ansible-role-gitea) or the [`ansible-role-gotosocial`](https://github.com/mother-of-all-self-hosting/ansible-role-gotosocial).

Some advice:
 - Your file structure will probably look something like this:

```
.
├── defaults/
│   └── main.yml
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
│   └── NEW-SERVICE.service.j2
├── .gitignore
├── LICENSE
└── README.md
```
- You will need to decide on a licence, without it, ansible-galaxy won't work. We recommend AGPLv3, like all of MASH.

### 3. Update the MASH-Playbook to support your created Ansible role

There are a few files that you need to adapt:
```
.
├── docs/
│   ├── supported-services.md  -> Add your service
│   └── services/
│       └── YOUR-SERVICE.md  -> document how to use it
├── templates/
│   ├── group_vars_mash_servers  -> Add default config
│   └── requirements.yml  -> add your Ansible role
│   └── setup.yml  -> add your Ansible role
```
<details>

<summary> file: templates / group_vars_mash_servers </summary>
In this file you wire your role with the rest of the playbook — integrating with the service manager or potentially with other roles.

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

<details>
<summary>Support Postgres</summary>

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

[...]

# role-specific:postgres
YOUR-SERVICE_database_hostname: "{{ postgres_identifier if postgres_enabled else '' }}"
YOUR-SERVICE_database_port: "{{ '5432' if postgres_enabled else '' }}"
YOUR-SERVICE_database_password: "{{ '%s' | format(mash_playbook_generic_secret_key) | password_hash('sha512', 'db.authentik', rounds=655555) | to_uuid }}"
YOUR-SERVICE_database_username: "{{ authentik_identifier }}"
# /role-specific:postgres

YOUR-SERVICE_container_additional_networks_auto: |
  {{
    ([postgres_identifier ~ '.service'] if postgres_enabled and YOUR-SERVICE_database_hostname == postgres_identifier else [])
  }}

########################################################################
#                                                                      #
# /YOUR-SERVICE                                                        #
#                                                                      #
########################################################################
# /role-specific:YOUR-SERVICE
```
</details><details>
<summary>Support exim-relay</summary>

The [exim-relay](https://github.com/devture/exim-relay) is an easy way to configure for all services a way for outgoing mail.
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
YOUR-SERVICE_config_mailer_enabled: "{{ 'true' if exim_relay_enabled else '' }}"
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
</details><details>

<summary>Support hubsite</summary>

- Add the logo of your Service to [`ansible-role-hubsite/assets`](https://github.com/mother-of-all-self-hosting/ansible-role-hubsite/tree/main/assets) via a pull request.
- configure the `group_vars_mash_servers` file:

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
hubsite_service_YOUR-SERVICE_name: Adguard Home
hubsite_service_YOUR-SERVICE_url: "https://{{ YOUR-SERVICE_hostname }}{{ YOUR-SERVICE_path_prefix }}"
hubsite_service_YOUR-SERVICE_logo_location: "{{ role_path }}/assets/YOUR-SERVICE.png"
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

</details>

### Additional hints

- Add a line like `# Project source code URL: YOUR-SERVICE-GIT-REPO` to your Ansible role's `defaults/main.yml` file, so that [`bin/feeds.py`](/bin/feeds.py) can automatically find the Atom/RSS feed for new releases.
