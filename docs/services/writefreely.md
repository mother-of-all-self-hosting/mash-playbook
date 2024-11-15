# WriteFreely

[WriteFreely](https://github.com/writefreely/writefreely) is a clean, minimalist publishing platform made for writers, federated via ActivityPub.


## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server

WriteFreely supports using a [MariaDB](./mariadb.md) database, but this Ansible role and playbook are not configured to make use of it.


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# writefreely                                                          #
#                                                                      #
########################################################################

writefreely_enabled: true

writefreely_hostname: writefreely.example.com

writefreely_instance_name: 'A Writefreely blog' # optional
writefreely_instance_description: 'My Writefreely blog' # optional

########################################################################
#                                                                      #
# /writefreely                                                         #
#                                                                      #
########################################################################
```

In the example above, we configure the service to be hosted at `writefreely.example.com`.

You can add the following variables to add an administrator user during the first setup process:

```yml
# You can use any username except "admin" (see below)
writefreely_env_admin_user: ''
writefreely_env_admin_password: ''
```

Alternatively you can add admins after [installation](../installing.md) with:

```sh
just run-tags writefreely-add-admin --extra-vars=username=<username> --extra-vars=password=<password>
```

**Note that the username `admin` is unavailable**, as `writefreely.example.com/admin` is already taken by the admin dashboard.

Additional user accounts can be added at any time once WriteFreely is running with:

```sh
just run-tags writefreely-add-user --extra-vars=username=<username> --extra-vars=password=<password>
```

Their respective blogs can then be accessed on `writefreely.example.com/<username>`.

## Settings

To customize your settings on first setup, you can adjust the `writefreely_env_*` default variables.
After installation, changes in environment variables will be ignored. But you can still change the settings at `writefreely.example.com/admin/settings` or by directly changing `/mash/writefreely/data/config.ini`.

## Maintenance

In case you need to run maintenance tasks as documented in [Admin commands](https://writefreely.org/docs/main/admin/commands), you can run the following commands on the server:

```sh
/usr/bin/docker exec mash-writefreely /writefreely/writefreely -c /data/config.ini [command]
```

For example, to delete an existing user, run:

```sh
/usr/bin/docker exec mash-writefreely /writefreely/writefreely -c /data/config.ini user delete [username]
```
