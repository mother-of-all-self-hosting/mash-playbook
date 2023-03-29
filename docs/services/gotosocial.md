# GoToSocial

[GoToSocial](https://gotosocial.org/) is a self-hosted [ActivityPub](https://activitypub.rocks/) social network server, that this playbook can install, powered by the [mother-of-all-self-hosting/ansible-role-gotosocial](https://github.com/mother-of-all-self-hosting/ansible-role-gotosocial) Ansible role.

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


## Migrate an existing instance

The following assumes you want to migrate from `serverA` to `serverB` (managed by mash) but you just cave to adjust the copy commands if you are on the same server.

Stop the initial instance on `serverA`

```bash
serverA$ systemctl stop gotosocial
```

Dump the database (depending on your existing setup you might have to adjust this)
```
serverA$ pg_dump gotosocial > latest.sql
```

Copy the files to the new server

```bash
serverA$ rsync -av -e "ssh" latest.sql root@serverB:/mash/gotosocial/
serverA$ rsync -av -e "ssh" data/* root@serverB:/mash/gotosocial/data/
```

Install (but don't start) the service and database on the server.

```bash
yourPC$ ansible-playbook -i inventory/hosts setup.yml --tags=install-all
yourPC$ just run-tags import-postgres --extra-vars=server_path_postgres_dump=/mash/gotosocial/latest.sql --extra-vars=postgres_default_import_database=mash-gotosocial
```

Start the services on the new server

```bash
yourPC$ ansible-playbook -i inventory/hosts setup.yml --tags=install-all
```

Done 🥳
