# GoToSocial

[GoToSocial](https://gotosocial.org/) is a self-hosted [ActivityPub](https://activitypub.rocks/) social network server, that this playbook can install, powered by the [moan0s/role-gotosocial](https://github.com/moan0s/role-gotosocial) Ansible role.

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# gotosocial                                                           #
#                                                                      #
########################################################################

gotosocial_enabled: true
gotosocial_hostname: 'social.example.org'

########################################################################
#                                                                      #
# /gotosocial                                                          #
#                                                                      #
########################################################################
```

After installation, you can use `ansible-playbook -i inventory/hosts setup.yml --tags=gotosocial-add-user --extra-vars "username=<username> email=<email> password=<password>"`
to create your a user. Change `--tags=gotosocial-add-user` to `--tags=gotosocial-add-admin` to create an admin account.

### Usage

After [installing](../installing.md), you can visti at the URL specified in `firezone_hostname` and should see your instance.
Start to customize it at `social.example.org/admin`.

Use the [GtS CLI Tool](https://docs.gotosocial.org/en/latest/admin/cli/) to do admin & maintenance tasks. E.g. use 
```bash
docker exec -it mash-gotosocial /gotosocial/gotosocial admin account demote --username <username>
```
to demote a user from admin to normal user.

Refer to the [great official documentation](https://docs.gotosocial.org/en/latest/) for more information on GoToSocial.
