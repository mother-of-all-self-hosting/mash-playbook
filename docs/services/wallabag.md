# Wallabag

[Wallabag](https://wallabag.org) is a web application allowing you to save web pages for later reading. Click, save and read it when you want. It extracts content so that you won't be distracted by pop-ups and cie.

## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server
- a [Postgres](postgres.md) database


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# wallabag                                                             #
#                                                                      #
########################################################################

wallabag_enabled: true

wallabag_hostname: wallabag.example.com

# Put a strong password below, generated with `pwgen -s 64 1` or in another way.
# You will need to use this password in the setup wizard after installation.
wallabag_database_password: ''

########################################################################
#                                                                      #
# /wallabag                                                            #
#                                                                      #
########################################################################
```



## Usage

After installation, [you can import your existing database](#installing-a-server-into-which-youll-import-old-data), or you will have to populate the database first, run:

- either: `just run-tags wallabag-populate-database,start`
- when not using `just`: `ansible-playbook -i inventory/hosts setup.yml --tags=wallabag-populate-database`

Feel free to follow Wallabag [official documentation](https://doc.wallabag.org/) for other settings.
