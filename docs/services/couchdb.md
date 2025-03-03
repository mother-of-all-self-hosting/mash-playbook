# CouchDB

[CouchDB](https://couchdb.apache.org/) is a NoSQL database that uses JSON for documents.
This Ansible role is designed to install and configure CouchDB for using the [official CouchDB Docker image](https://github.com/apache/couchdb-docker) via the [ansible-role-couchdb](https://github.com/Bergruebe/ansible-role-couchdb).

> [!WARNING]
> - This role will not delete or modify existing databases or users. It will only create new databases and users if they do not already exist.
> - This role **does not automatically integrate with Traefik** yet (see details below). PRs are welcome!

## Features

- Sets up CouchDB in a Docker container.
- Creates necessary system tables, if `couchdb_config_single_node: true.
- Adds users as specified in the playbook.
- Sets database permissions.
- Integrates with the MASH playbook for easy deployment.

## Usage

To use this role with the MASH playbook, add following lines to your inventory file of your MASH playbook:

```yaml
########################################################################
#                                                                      #
# couchdb                                                              #
#                                                                      #
########################################################################

couchdb_enabled: true

couchdb_hostname: couchdb.example.com

# enable couchdb single node mode, to automatically create databases and users
couchdb_config_single_node: true

couchdb_admins_custom:
  - name: admin
    password: UseASecurePassword

couchdb_users_custom:
  - name: user1
    password: UseASecurePassword
    roles: []
    type: user

couchdb_tables_custom:
    - name: my_custom_table
      permission:
        admin:
          names:
            - user1
          roles: []
        member:
          names: []
          roles: []

########################################################################
#                                                                      #
# /couchdb                                                             #
#                                                                      #
########################################################################
```

You can customize the behavior of the role by setting the following variables in your playbook:

- `couchdb_environment_variables_extension`: to add additional environment variables to the CouchDB container.
- `couchdb_config_extension`: to add additional configuration to the CouchDB configuration
- `couchdb_config_peruser_enabled`: to enable per-user configuration in CouchDB | default is `true`.
- `couchdb_config_require_valid_user_except_for_up`: to require a valid user for all requests except for the `_up` endpoint | default is `true`.
- `couchdb_container_additional_networks_custom`: to add additional networks to the CouchDB container.
- `couchdb_version`: to specify the version of the CouchDB Docker image to use

For more information on possible configuration, refer to the comments in the [`defaults/main.yml`](https://github.com/Bergruebe/ansible-role-couchdb/blob/master/defaults/main.yml) file.

By default, this role **will not expose the CouchDB port** to the host machine. If you want to access CouchDB from outside the Docker container, you will need to expose the port in your playbook via the `couchdb_container_http_host_bind_port` variable. Or you can just add the container to another docker network via the `couchdb_container_additional_networks_custom` variable.
Please consider the use of a reverse proxy for secure access to CouchDB.

Currently, the [ansible-role-couchdb](https://github.com/Bergruebe/ansible-role-couchdb) Ansible role **does not automatically integrate with Traefik**. PRs are welcome!

## Contributing

Contributions are welcome! Please feel free to review the [ansible-role-couchdb](https://github.com/Bergruebe/ansible-role-couchdb) repository and submit a Pull Request.

