# GoToSocial

[Mobilizon](https://joinmobilizon.org/en/) is a ActivityPub/Fediverse server to create and share events here powered by the [mother-of-all-self-hosting/ansible-role-mobilizon](https://github.com/mother-of-all-self-hosting/ansible-role-mobilizon) Ansible role.

## Configuration

To enable this service, add the following configuration to your `vars.yml` file. Also you need to enable postgis which will serve as database for mobilizon.
After that you can re-run the [installation](../installing.md) process.

```yaml
########################################################################
#                                                                      #
# mobilizon                                                            #
#                                                                      #
########################################################################

mobilizon_enabled: true


# Hostname that this server will be reachable at.
# DO NOT change this after your server has already run once, or you will break things!
mobilizon_hostname: 'events.example.org'

# to open registrations uncomment the following line
# mobilizon_registrations_open: true

########################################################################
#                                                                      #
# /mobilizon                                                           #
#                                                                      #
########################################################################

########################################################################
#                                                                      #
# postgis                                                              #
#                                                                      #
########################################################################

postgis_enabled: true

# Put a strong password below, generated with `pwgen -s 64 1` or in another way
postgis_connection_password: ''

########################################################################
#                                                                      #
# /postgis                                                             #
#                                                                      #
########################################################################
```

After installation, you can use `just run-tags mobilizon-add-user --extra-vars=username=<username> --extra-vars=password=<password> --extra-vars=email=<email>"`
to create your a user. Change `--tags=mobilizon-add-user` to `--tags=mobilizon-add-admin` to create an admin account.

### Usage

After [installing](../installing.md), you can visit at the URL specified in `mobilizon_hostname` and should see your instance.

Refer to the [great official documentation](https://docs.gotosocial.org/en/latest/) for more information on GoToSocial.
