# Wordpress

[WordPress](https://wordpress.org/) is a widley used open source web content management system that this playbook can install, powered by the [mother-of-all-self-hosting/ansible-role-wordpress](https://github.com/mother-of-all-self-hosting/ansible-role-wordpress) Ansible role.

## Dependencies

This service requires the following other services:

- a [MariaDB](mariadb.md) database
- a [Traefik](traefik.md) reverse-proxy server

## Configuration

```yaml
########################################################################
#                                                                      #
# wordpress                                                            #
#                                                                      #
########################################################################

wordpress_enabled: true

wordpress_hostname: example.org

########################################################################
#                                                                      #
# /wordpress                                                           #
#                                                                      #
########################################################################
```

### Enable MariaDB as database

If not already done you need to enable MariaDB so Wordpress can use it as database.

```yaml
########################################################################
#                                                                      #
# mariadb                                                              #
#                                                                      #
########################################################################

mariadb_enabled: true

# Put a strong password below, generated with `pwgen -s 64 1` or in another way
mariadb_root_passsword: ''

########################################################################
#                                                                      #
# /mariadb                                                             #
#                                                                      #
########################################################################
```


## Usage

Navigate to the domain you set as `wordpress_hostname`, select a language and create an admin user.

> **Make sure to create a user with a strong password**

You can now log in and fill your website with content!


## Advanced

### Basic authentication

If you don't want to have your website accessible to everyone (e.g. you first want to present it to a client) you can use

```yaml
wordpress_container_labels_middleware_basic_auth_enabled: true
# Use `htpasswd -nb USERNAME PASSSWORD` to generate the users below.
# See: https://doc.traefik.io/traefik/middlewares/http/basicauth/#users
wordpress_container_labels_middleware_basic_auth_users: ''
```
