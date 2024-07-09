# writefreely

[writefreely](https://github.com/writefreely/writefreely) is a clean, minimalist publishing platform made for writers, federated via ActivityPub.


## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server


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

writefreely_instance_name: 'A Writefreely blog'
writefreely_instance_description: 'My Writefreely blog'

########################################################################
#                                                                      #
# /writefreely                                                         #
#                                                                      #
########################################################################
```

In the example above, we configure the service to be hosted at `writefreely.example.com`.

After installation, it is recommended to create an admin account with `just run-tags writefreely-add-admin --extra-vars=username=<username> --extra-vars=password=<password>`.
Note that the username "admin" is unavailable, as `writefreely.example.com/admin` will is already be serving as the admin dashboard.

Additional user accounts can be added with `just run-tags writefreely-add-user --extra-vars=username=<username> --extra-vars=password=<password>`.
Their respective blog can then be accessed on `writefreely.example.com/<username>`.

To customize your settings on first setup, you can adjust the `writefreely_env_*` default variables.
After installation, changes in environment variables will be ignored. But you can still change the settings at `writefreely.example.com/admin/settings` or by directly changing `/mash/writefreely/data/config.ini`.

In case you need to run maintenance tasks as documented in [Admin commands](https://writefreely.org/docs/main/admin/commands), you can use the following command:

```
sudo /usr/bin/docker exec mash-writefreely /writefreely/writefreely -c /data/config.ini [command]
```

For example, to delete an existing user, run:

```
sudo /usr/bin/docker exec mash-writefreely /writefreely/writefreely -c /data/config.ini user delete [username]
```
