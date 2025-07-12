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

## Usage

Navigate to the domain you set as `wordpress_hostname`, select a language and create an admin user.

> **Make sure to create a user with a strong password**

You can now log in and fill your website with content!


## Advanced

### Basic authentication

If you don't want to have your website accessible to everyone (e.g. you first want to present it to a client) you can use

```yaml
wordpress_container_labels_middleware_basic_auth_enabled: true
# Use `htpasswd -nb USERNAME PASSWORD` to generate the users below.
# See: https://doc.traefik.io/traefik/middlewares/http/basicauth/#users
wordpress_container_labels_middleware_basic_auth_users: ''
```

### Increase upload limit

By default we set the upload limit to `64M`. Increasing or decreasing the upload limit can be done by adding the following to your `vars.yml`

```yaml
wordpress_max_upload_size: '64M'
```
